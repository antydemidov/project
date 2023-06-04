"""The collection of functions used in the project"""

import json
import os
import xml.etree.ElementTree as ET
import zipfile

import pandas as pd
from datetime import datetime
import requests as rq

from .results import CommonResult
from .settings import Settings

from typing import Literal


settings = Settings()

# client = Connection()
# bod = Connection('BoD')
# bod_v2 = Connection('BoD_v2')
# bod_desc = Connection(settings.actual_db_desc)
# actual_db = Connection(settings.actual_db)

# Creation pandas dataframe from 1. XML file; 2. dict- or array-like object
def get_dataframe(path: str = None, source = None, orient: str = None) -> pd.DataFrame:
    """
    Creates Pandas DataFrame from 1. XML-file; 2. dict- or array-like object.

    Parameters
    ---
    -   `path` : str - A string path to XML-file.
    -   `object` : dict- or array-like - Read more in Pandas Documentation for
        pd.DataFrame.from_dict.
    -   `orient` : str - Read more in Pandas Documentation for pd.DataFrame.from_dict
    """

    if (path is not None and source is not None):
        raise ValueError('Use the only one mode of this method')
    if path is not None:
        if not os.path.exists(path):
            raise FileExistsError
        element_tree = ET.parse(path)
        root = element_tree.getroot()
        dataframe = pd.DataFrame.from_dict(data=[x.attrib for x in root if x.attrib != {}])
        return dataframe
    if (source is not None and orient is not None):
        dataframe = pd.DataFrame.from_dict(data=source, orient=orient)
        return dataframe
    raise ValueError

# sorts dicts by keys
def sort_dict(unsorted_dict: dict) -> dict:
    """
    Sort dicts by keys in ascending order

    Parameters
    ---
    -   `unsorted_dict`: dict
    """

    sorted_dict = {}
    for key in sorted(list(unsorted_dict.keys())):
        value = unsorted_dict[key]
        if isinstance(unsorted_dict[key], dict):
            value = sort_dict(value)
        sorted_dict.update({key: value})
    return sorted_dict


# CONVERT_DATABASE
# def convert_database(fillna: bool = False):
#     converted_collections = []
#     error_collections = []
#     for coll_name in bod.ls_colls:
#         source = get_dataframe(coll_name, fillna)
#         chunk_size = settings.default_chunk_size
#         i, length = 0, len(source)
#         if length > 0:
#             try:
#                 bod_v2.db.create_collection(coll_name)
#             except:
#                 bod_v2.get_coll(coll_name).delete_many({})
#             coll = bod_v2.get_coll(coll_name)
#             while i < length:
#                 coll.insert_many(
#                     source[i:i+chunk_size].to_dict(orient='records'))
#                 i += chunk_size
#             converted_collections.append(coll_name)
#         else:
#             error_collections.append(coll_name)
#     details = {
#         'converted_collections': converted_collections,
#         'error_collections': error_collections
#     }
#     return CommonResult(status='Done',
#                         details=details,
#                         coll_name=coll_name)


# def get_coll_schema(coll_name):
#     schema = {}
#     _map = {
#         'Int64': 0,
#         'Int32': 0,
#         'string': '',
#         'boolean': None,
#         'datetime64': '',
#     }

#     if 'params' in coll_name:
#         coll_name = 'param'
#     elif 'housetypes' in coll_name:
#         coll_name = 'housetypes'

#     coll = bod_desc.get_coll('Schema')
#     for key, value in coll.find_one({'coll_name': coll_name})['fields'].items():
#         if 'Int' in value['type']:
#             schema.update({key: {'type': int, 'none': 0}})
#         else:
#             schema.update({key: {'type': value['type'], 'none': _map[value['type']]}})

#     return schema


# def get_dataframe(coll_name: str, fillna: bool) -> pd.DataFrame:
#     d = get_coll_schema(coll_name)
#     dtype = {}
#     for key, value in d.items():
#         if key in list(pd.DataFrame(bod.get_coll(coll_name).find(
#                 {}, limit=2)).columns):
#             dtype.update({key: value['type']})
#     nonetype = {}
#     for key, value in d.items():
#         if key in list(pd.DataFrame(bod.get_coll(coll_name).find(
#                 {}, limit=2)).columns):
#             nonetype.update({key: value['none']})
#     source = pd.DataFrame(bod.get_coll(coll_name).find({}))
#     if fillna:
#         source = source.fillna(value=nonetype, inplace=False).astype(
#             dtype=dtype, errors='ignore')
#     return source


# def find_dgrad_objects():
#     filter_adm = {'PATH': {'$regex': str(settings.dgrad)}}
#     filter_mun = {'PATH': {'$regex': str(settings.dgrad)}}

#     objects_in_dgrad = list(set(list(pd.DataFrame(bod.get_coll('admhierarchy').find(
#         filter_adm))['OBJECTID']) + list(pd.DataFrame(bod.get_coll('munhierarchy').find(
#             filter_mun))['OBJECTID'])))

#     return objects_in_dgrad


# def cut_tree(coll_name: str,
#              chosen_ids: list,
#              mode: Literal[1, 2] = 1):
#     """
#     Cut the tree
#     ---
#     :Modes:
#     - 1 - Upload data to the BoD_v2
#     - 2 - Returns data
#     """
#     src_coll = bod.get_coll(coll_name)
#     try:
#         dst_coll = bod_v2.get_coll(coll_name)
#     except:
#         dst_coll = bod_v2.db.create_collection(coll_name)

#     if coll_name != 'addrobjdivision':
#         _filter = {'OBJECTID': {'$in': chosen_ids}}
#     else:
#         _filter = {'ID': {'$in': chosen_ids}}

#     data = list(src_coll.find(_filter))

#     if mode == 1:
#         i = 0
#         chunk_size = settings.default_chunk_size
#         length = len(data)
#         while i < length:
#             dst_coll.insert_many(data[i:i+chunk_size])
#             i += chunk_size
#     elif mode == 2:
#         return data


class FIASVersions:
    """
    Returns an object of new versions.
    
    Parameters
    ----------
    current_version : `int`
        >>> FIAS_Versions(current_version=20211125)
    Format is YYYYMMDD.

    Attributes
    ----------
    total_size : `int`
        sum of files size

    versions : `list`
        [{
            'VersionID': `int`,
            'URL': `str`,
            'file_size': `int`
        }, ...]

    status_code: `int`: request status code
    """
    def __init__(self, current_version: int):
        result = []
        total_size = 0
        if rq.head(settings.update_link, timeout=5).status_code == 200:
            r = rq.get(settings.update_link, timeout=settings.default_timeout)
            source = json.loads(r.text)
            for version in source:
                if (version['VersionId'] > current_version and version['GarXMLDeltaURL'] != ''):
                    r = rq.head(version['URL'], timeout=5)
                    if r.status_code == 200:
                        file_size = int(r.headers['Content-Length'])
                        total_size += file_size
                    result.append({
                        'version_id': version['VersionId'],
                        'url': version['GarXMLDeltaURL'],
                        'file_size': file_size
                    })
        self.total_size = total_size
        self.versions = result[::-1]
        self.status_code = r.status_code


class UpdatingFile:
    def __init__(self, version_id: int, url: str, database: Connection) -> None:
        self.url = url
        self.version_id = version_id
        self.download_path = f'source/{version_id}.zip'
        self.extr_path = f'extracted_{version_id}'
        self.db = database

    def download(self):
        r = rq.get(self.url, stream=True, timeout=settings.default_timeout)
        if r.status_code == 200:
            chunk_size = 1024 * 1024 * settings.default_chunk_size_mb
            with open(self.download_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size, False):
                    if chunk:
                        f.write(chunk)
            result = CommonResult(status='Done',
                                  status_bool=True,
                                  request_status_code=r.status_code,
                                  file_size=int(r.headers['Content-Length']))
        else:
            result = CommonResult(status='Not available',
                                  status_bool=False,
                                  request_status_code=r.status_code,
                                  file_size=0)
        r.close()
        return result

    def extract(self):
        details = {}
        if zipfile.is_zipfile(self.download_path):
            z = zipfile.ZipFile(self.download_path, 'r')
            needed_files, file_size = [], 0
            zip_info = z.NameToInfo
            for key, value in zip_info.items():
                if key[:3] == '73/':
                    needed_files.append(value)
                    file_size += value.file_size
                    details.update({key: {'file_size': value.file_size}})
            if needed_files:
                z.extractall(self.extr_path, members=needed_files)
            z.close()
            os.remove(self.download_path)
            result = CommonResult(status='Extracted',
                                  extr_path=self.extr_path,
                                  file_size=file_size,
                                  details=details)
        else:
            result = CommonResult(status='Error',
                                  extr_path=None,
                                  file_size=None)
        return result

    def update(self):
        details = {}
        _map = {
            'changehistory': 'CHANGEID',
            'objectlevels': 'LEVEL',
            'reestrobjects': 'OBJECTID'
        }
        chunk_size = settings.default_chunk_size

        if os.path.exists(self.extr_path + '/73'):
            deleted_count, updated_count = 0, 0
            for name in os.listdir(self.extr_path + '/73'):
                coll_name = ''.join(name.lower().split('_')[1:-2])
                full_path = self.extr_path + '/73/' + name
                root = ET.parse(full_path).getroot()
                source = list(root)
                collection = self.db.get_coll(coll_name)
                deleted, updated = 0, 0

                if len(source) != 0:
                    data = [item.attrib for item in source]
                    length = len(data)
                    i = 0
                    while i < length:
                        if coll_name in list(_map.keys()):
                            new_recs = [item[_map[coll_name]]
                                        for item in data[i:i+chunk_size]]
                            deleted += collection.delete_many(
                                {_map[coll_name]: {'$in': new_recs}}).deleted_count
                        else:
                            new_recs = [item['ID']
                                        for item in data[i:i+chunk_size]]
                            deleted += collection.delete_many(
                                {'ID': {'$in': new_recs}}).deleted_count
                        i += chunk_size
                    i = 0
                    while i < length:
                        updated += len(collection.insert_many(
                            data[i:i+chunk_size]).inserted_ids)
                        i += chunk_size
                details.update(
                    {coll_name: {'deleted_count': deleted, 'updated_count': updated}})
                deleted_count += deleted
                updated_count += updated

        result = CommonResult(status='Done',
                              deleted_count=deleted_count,
                              updated_count=updated_count,
                              details=details)
        return result
