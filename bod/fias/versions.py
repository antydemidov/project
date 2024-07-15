"""
Versions
========
This module provides functionality to manage and install updates for a dataset,
specifically using the Federal Information Address System (FIAS) dataset. The
module defines two main classes:

Classes
-------
- `Versions`: Handles the retrieval and installation of multiple new versions
    of the dataset.
- `Version`: Represents a single version of the dataset and provides methods to
    download, extract, and update the dataset.
"""


import json
import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

import requests as rq
from pydantic_core import ValidationError
from pymongo.database import Database

from bod.fias.utils import unique_field_by_coll, validator_by_coll
from bod.logging import get_logger
from bod.settings import Settings

__all__ = [
    'Versions',
    'Version'
]
logger = get_logger(__name__)


class Version:
    """
    Represents a new version.

    Paramaters
    ----------
    version_id : int
        The number of the version in format YYYYMMDD.
    url : str
        The URL to download the version.
    database : Database
        A pymongo Database object.
    settings : Settings
        A settings object for configuration.
    """

    def __init__(self, version_id: int, url: str, database: Database, settings: Settings):
        self.version_id = version_id
        self.url = url
        self.database = database
        self.settings = settings
        self.file_size = 0
        self.installed = False
        self.download_path = f'source/{version_id}.zip'
        self.extract_path = f'source/extracted/{version_id}/'

    def parse_data(self, coll_name: str, data: list[dict]) -> list[dict] | None:
        """Parses data from raw list of dictionaries and transforms them into
        the correct data types."""

        result = []
        validator_class = validator_by_coll(coll_name)
        errors = []
        if not validator_class:
            return None

        for item in data:
            try:
                obj = validator_class(**item)
                result.append(obj.model_dump())
            except ValidationError as e:
                errors.append(item['id'])
                logger.error(e)

        return result

    def get_version(self):
        """Returns the version from delta file."""

        version_path = os.path.join(self.extract_path, 'version.txt')
        with open(version_path, 'r', encoding='utf-8') as f:
            version = f.readline().strip().replace('.', '')

        return int(version)

    def _download(self):
        """Downloads the delta file of the version."""

        logger.info('Downloading version %s...', self.version_id)

        try:
            with rq.get(self.url, stream=True, timeout=self.settings.default_timeout
                        ) as response:
                response.raise_for_status()
                self.file_size = int(response.headers.get('Content-Length', 0))
                chunk_size = self.settings.default_chunk_size_mb * 1024 * 1024

                with open(self.download_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size):
                        if chunk:
                            file.write(chunk)
            logger.info('Downloaded version %s successfully. File size: %s bytes.',
                        self.version_id, self.file_size)
            return True
        except rq.RequestException as e:
            logger.error('Error downloading version %s: %s', self.version_id, e)
            return False

    def _extract(self):
        """Extracts the delta-file of the version."""

        file_size = 0
        logger.info('Extracting version %s...', self.version_id)

        if not zipfile.is_zipfile(self.download_path):
            logger.error('The file for version %s is not a zip file.',
                         str(self.version_id))
            return False

        with zipfile.ZipFile(self.download_path, 'r') as file:
            needed_files = []
            for key, value in file.NameToInfo.items():
                if key.startswith(f'{self.settings.fias.region_code}/'):
                    needed_files.append(value)
                    file_size += value.file_size
            if needed_files:
                needed_files += ['version.txt']
                file.extractall(self.extract_path, members=needed_files)
        os.remove(self.download_path)

        for item in os.scandir(self.extract_path):
            dir_name = os.path.dirname(item.path)
            new_path = os.path.join(dir_name, ''.join(item.name.lower().split('_')[
                                    1:-2]) + '.' + item.name.split('.')[-1].lower())
            os.rename(item.path, new_path)

        logger.info('Extracted version %s successfuly.', self.version_id)
        return True

    def _update(self):
        """Updates the database with the new version."""

        # deleted_count, updated_count = 0, 0
        chunk_size = self.settings.default_chunk_size
        path = os.path.join(self.extract_path, self.settings.fias.region_code)

        for file in os.scandir(path):
            coll_name = ''.join(file.name.lower().split('_')[1:-2])
            root = ET.parse(os.path.abspath(file.path)).getroot()
            data = [item.attrib for item in list(root)]

            if not data:
                logger.info('The collection "%s" was skipped.', coll_name)
                continue

            collection = self.database.get_collection(coll_name)
            id_column = unique_field_by_coll(coll_name)

            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                validated_data = self.parse_data(coll_name, chunk)
                if not validated_data:
                    continue

                new_rec_ids = [item[id_column] for item in validated_data]
                collection.delete_many({id_column: {'$in': new_rec_ids}})
                collection.insert_many(validated_data)

        logger.info('Installed version %s successfully.', self.version_id)
        self.installed = True
        return True

    def install(self):
        """Installs the new version."""

        if self.installed:
            logger.info('Version %s is already installed.', self.version_id)
            return True

        logger.info('Installing version %s...', self.version_id)
        if self._download() and self._extract() and self._update():
            shutil.rmtree(self.extract_path)
            logger.info('Installed version %s and cleaned up.', self.version_id)
            self.settings.fias.current_version = self.version_id
            return True
        logger.warning('Failed to install version %s.', self.version_id)
        return False


class Versions:
    """
    Returns an object of new versions.

    Paramaters
    ----------
    current_version : int
        The number of the version in format YYYYMMDD.
    database : pymongo.database.Database
        A pymongo Database object.
    settings : Settings
        A settings object for configuration.

    Attributes
    ----------
    total_size : int
        The sum of file sizes for new versions.
    versions : list
        A list of Version objects representing new versions.
    """

    def __init__(self, current_version: int, database: Database, settings: Settings):
        self.current_version = current_version
        self.database = database
        self.settings = settings
        self.total_size = 0
        self.versions = self.__get_versions()

    def __get_versions(self) -> list[Version] | None:
        """
        Fetches a list of new versions from the update link.

        Returns
        -------
        list[Version], optional
            A list of new Version objects or None if an error occurred.
        """

        total_size = 0
        versions = []

        try:
            response = rq.get(self.settings.fias.update_link,
                              timeout=self.settings.default_timeout)
            response.raise_for_status()
            data = response.json()
        except (rq.RequestException, json.JSONDecodeError) as e:
            logger.error('Failed to fetch versions: %s', e)
            return None

        if not data:
            logger.error('No data received.')
            return None

        for item in data:
            version_id = item.get('VersionId', 0)
            url = item.get('GarXMLDeltaURL', None)

            if version_id > self.current_version and url:
                version = Version(version_id, url, self.database, self.settings)
                total_size += version.file_size
                versions.append(version)
            else:
                logger.warning('Version %s was skipped.', version_id)

        if not versions:
            logger.info('No new versions found.')
            return None

        self.total_size = total_size
        return versions[::-1]

    def list_version_ids(self):
        """Returns a list of versions ids."""

        if not self.versions:
            return []
        return [version.version_id for version in self.versions]

    def install(self, limit: int = 10):
        """
        Installs new versions and updates the database.

        Parameters
        ----------
        limit : int, optional
            The maximum number of versions to install. Default is 10.

        Returns
        -------
        bool
            True if all versions were installed successfully, otherwise False.
        """

        if not self.versions:
            logger.info('No versions found to install.')
            return False

        status = True
        for version in self.versions[:limit]:
            if not version.install():
                status = False

        return status
