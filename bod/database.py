"""
Database
--------
Description.
"""

from abc import abstractmethod
from uuid import UUID

from pymongo import MongoClient

from bod.fias.utils import unique_field_by_coll
from bod.fias.versions import Versions
from bod.logging import get_logger
from bod.settings import Settings


logger = get_logger(__name__)

def get_database(client: MongoClient, database_name: str):
    """
    Gets the database by the given name.

    Parameters
    ----------
    client : pymongo.MongoClient
        The object of MongoClient.
    database_name : str
        The name of needed database.
    """

    database = None

    try:
        logger.info('Getting the database "%s"...', database_name)
        assert database_name in client.list_database_names()
        database = client.get_database(database_name)
        logger.info('Database "%s" is accessed.', database_name)
    except AssertionError as err:
        logger.error(err)
    return database


class BaseDatabase:
    """Base class for database classes."""

    def __init__(self, client: MongoClient, settings: Settings):
        self.client = client
        self.settings = settings

    @abstractmethod
    def update_database(self): ...


class FiasDatabase(BaseDatabase):
    """
    Description.

    Parameters
    ----------
    database : pymongo.database.Database
        desc.
    settings : Settings
        desc.
    """

    def __init__(self, client: MongoClient, settings: Settings):
        super().__init__(client, settings)
        self.database = get_database(client, settings.fias.database_name)
        self.versions: Versions = None

    def get_versions(self):
        """Loads versions and returns them."""

        if self.versions:
            return self.versions
        version_id = self.settings.fias.current_version
        if not version_id:
            version_id = 0
        versions = Versions(version_id, self.database, self.settings)
        return versions

    def check_updates(self):
        """Checks updates."""

        self.versions = self.get_versions()
        return self.versions.list_version_ids()

    def update_database(self):
        """Description."""

        self.versions = self.get_versions()
        logger.info('Installing all new versions.')
        self.versions.install()
        logger.info('Installation complete. Total size: %d.',
                    self.versions.total_size)

    # def get_record(self, coll_name: str, fltr: dict):
    #     """Returns a record from a given collection using the given filter."""

    #     if coll_name not in self.database.list_collection_names():
    #         logger.error('The collection "%s" does not exist', coll_name)
    #         return None

    #     return self.database.get_collection(coll_name).find_one(fltr)

    # def get_records(self, coll_name: str, fltr: dict):
    #     """Returns a record from a given collection using the given filter."""

    #     if coll_name not in self.database.list_collection_names():
    #         logger.error('The collection "%s" does not exist', coll_name)
    #         return None

    #     return self.database.get_collection(coll_name).find(fltr)

    def delete_duplicates(self):
        """Deletes duplicates from the database."""

        chunk_size = self.settings.default_chunk_size

        for coll_name in self.database.list_collection_names():
            uniq_field = unique_field_by_coll(coll_name)

            # Find all docs with duplicates
            coll = self.database.get_collection(coll_name)
            pipeline = [
                {
                    '$group': {
                        '_id': [f'${uniq_field}'],
                        'dups': {'$addToSet': '$_id'},
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$match': {
                        'count': {'$gt': 1}
                    }
                }
            ]

            logger.info('Searching duplicates in collection "%s"...', coll_name)
            dups = coll.aggregate(pipeline, allowDiskUse=True)

            # Create a list of ObjectIDs to remove
            delete_this = [obj for dup in dups for obj in dup['dups'][1:]]
            j = len(delete_this)

            if j == 0:
                logger.info('Found no duplicates')
            else:
                logger.info('Found %d duplicates in "%s". Processing deletions...', j, coll_name)
                for i in range(0, j, chunk_size):
                    chunk = delete_this[i:i + chunk_size]
                    coll.delete_many({'_id': {'$in': chunk}})
                logger.info('Completed processing of "%s"', coll_name)

    def id_by_guid(self, guid: str):
        """Returns the object id by given fias identifier."""

        try:
            UUID(guid)
        except ValueError:
            logger.error('%s is not a valid UUID.', guid)
            return None
        data = self.database.get_collection('reestrobjects').find_one({
            'object_guid': guid,
            'is_active': True
        })
        if not data:
            return None
        return data.get('object_id', None)


class MkrfDatabase(BaseDatabase):
    """
    Description.

    Parameters
    ----------
    database : pymongo.database.Database
        desc.
    settings : Settings
        desc.
    """

    def __init__(self, client: MongoClient, settings: Settings):
        super().__init__(client, settings)
        self.database = get_database(client, settings.mkrf.database_name)

    def update_database(self):
        pass
