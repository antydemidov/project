"""
This is a collection of objects in Building of Dimitrovgrad project
"""

# import math
# from dataclasses import dataclass
# from tqdm import tqdm
# import pandas as pd

from datetime import datetime
import shutil
from typing import Any, Literal
from pymongo import MongoClient


from .bod_schema import Schema, CollectionSchema
from .results import UpdaterResult
from .settings import Settings
from .utils import (get_level_name, FIASVersions, UpdatingFile)


class Client:
    """Description"""
    def __init__(self):
        self.settings = Settings()
        self.fias = FiasClient()
        self.osm = OsmClient()

    def exit(self) -> None:
        self.settings.dump()
        self.fias.exit()


class FiasClient:
    """Description"""
    def __init__(self, settings: Settings = None) -> None:
        if not settings:
            settings = Settings()
        self.settings = settings
        self.mongo = MongoClient(self.settings.uri)

    def get_database(self, name: str):
        """Description"""
        return Database(self, name)

    def exit(self) -> None:
        self.mongo.close()


class OsmClient:
    """Description"""
    def __init__(self, settings: Settings = None) -> None:
        if not settings:
            settings = Settings()
        self.settings = settings

    def exit(self) -> None: ...


class Database:
    """Description"""
    def __init__(self, client: FiasClient, name: str):
        self.name = name
        self.mongo = client.mongo.get_database(name)
        self.client = client
        self.schema = Schema(client)
        # self.list_collections = self.mongo.list_collection_names()
        for coll_name in self.mongo.list_collection_names():
            schema = self.schema.find_coll(coll_name)
            setattr(self, coll_name, Collection(
                self, name=coll_name, schema=schema))

    @property
    def list_collections(self):
        return self.mongo.list_collection_names()

    def get_collection(self, name: str):
        """Description"""
        return Collection(database=self, name=name,
                          schema=self.schema.find_coll(name))

    def update_db(self, version_id: int, limit: int = 1):
        versions = FIASVersions(version_id).versions
        if not versions:
            return UpdaterResult(status='Where are no updates')
        current_version = version_id
        update_history = []
        total_size = 0.0
        i = 0
        for version in tqdm(versions, desc='Processing'):
            if (i == limit and limit != 0):
                break
            version_id, url = version['version_id'], version['url']
            file = UpdatingFile(version_id, url, self)
            updater_result = {}
            file.download()
            extract_result = file.extract()
            extr_path = getattr(extract_result, 'extr_path')
            file_size_add = getattr(extract_result, 'file_size')
            if extr_path is not None:
                total_size += file_size_add
                updater_result = file.update().details
            shutil.rmtree(extr_path)
            current_version = version_id
            update_history.append({'version_id': version_id,
                                   'file_size': file_size_add,
                                   'details': updater_result})
            i += 1
        return UpdaterResult(current_version, update_history, total_size, 'Done')


class Collection:
    """Description"""
    def __init__(self, database: Database, name: str, schema: CollectionSchema):
        self.name = name
        self.mongo = database.mongo.get_collection(database, name)
        self.database = database
        self.schema = schema

        self.insert_one = self.mongo.insert_one
        self.insert_many = self.mongo.insert_many

    def delete_all(self) -> int:
        """Deletes all records in the collection.

        Returns:
            int: number of deleted records.
        """
        return self.mongo.delete_many({}).deleted_count

    # def get_records(self, fltr: dict = {}, skip: int = 0, limit: int = 0):
    #     records = []
    #     data = self.find(fltr, skip=skip, limit=limit)
    #     for item in data:
    #         records.append(BODRecord(self, data=item))
    #     return records


class Record:
    """Description"""
    def __init__(self, collection: Collection, data: dict[str, Any]):
        self.data = data
        schema = collection.schema
        for key, value in data.items():
            field_schema = schema.find_field(key)
            if field_schema is not None:
                if field_schema.type == int:
                    value = int(value)
                elif field_schema.type == str:
                    value = str(value)
                elif field_schema.type == datetime:
                    value = datetime.fromisoformat(value)
            if key in ['ISACTIVE', 'ISACTUAL']:
                value = value in collection.database.client.settings.TRUE_VALUES
            self.__setattr__(key.lower(), value)

    def is_active(self):
        return getattr(self, 'isactive') in settings.true_values

    def is_actual(self):
        return getattr(self, 'isactual') in settings.true_values

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if key != 'data':
                result.update({key: value})
        return result


class Object:
    """Description"""
    def __init__(self, objectid: str | int):
        self.object_id: int = int(objectid)
        self.data: dict = self._find_all_docs_by_id()
        self.database = Connection(settings.actual_db)

    def _find_all_docs_by_id(self):
        result = {}
        for coll in self.database.ls_colls:
            from_coll = []
            for item in self.database.get_coll(coll).find({'OBJECTID': str(self.object_id)}):
                from_coll.append(Record(item))
            result.update({coll: from_coll})
        return result

    def build_tree(self):
        tree = {'parents': [], 'children': []}
        full_path_data = self.get_path_data()
        for part_path in full_path_data.keys():
            if part_path != str(self.object_id):
                tree['parents'].append(Object(part_path))
        children = self.database.get_coll('admhierarchy').find({
            'PARENTOBJID': str(self.object_id),
            'ISACTIVE': {'$in': settings.true_values},
        })
        for child in children:
            tree['children'].append(Object(child['OBJECTID']))
        return tree

    def get_full_address(self) -> str:
        full_address = []
        path_data = self.get_path_data()

        for path_part in path_data:
            part_path_keys = path_part.data.keys()
            if 'addrobj' in part_path_keys:
                for item in path_part.data['addrobj']:
                    try:
                        if item['ISACTIVE'] in settings.true_values:
                            full_address.append(
                                '. '.join([item['TYPENAME'], item['NAME']]))
                    except:
                        pass

            if 'houses' in part_path_keys:
                for item in path_part.data['houses']:
                    try:
                        if item['ISACTIVE'] in settings.true_values:
                            house_type = self.database.get_coll('housetypes').find_one({
                                'ID': item['HOUSETYPE'],
                                'ISACTIVE': {'$in': settings.true_values},
                            })
                            full_address.append(
                                ' '.join([house_type['SHORTNAME'], item['HOUSENUM']]))
                    except:
                        pass

            if 'apartments' in part_path_keys:
                for item in path_part.data['apartments']:
                    try:
                        if item['ISACTIVE'] in settings.true_values:
                            apart_type = self.database.get_coll('apartmenttypes').find_one({
                                'ID': item['APARTTYPE'],
                                'ISACTIVE': {'$in': settings.true_values},
                            })
                            full_address.append(
                                ' '.join([apart_type['SHORTNAME'], item['NUMBER']]))
                    except:
                        pass

        return ', '.join(full_address)

    def get_path(self) -> list:
        path = []
        for item in self.data['admhierarchy']:
            if (item.isactual() and item.isactive()):
                path = item.path.split('.')
        return path

    def get_path_data(self) -> tuple:
        path_data = (Object(path_part) for path_part in self.get_path())
        return path_data

    def get_params(self) -> list:
        full_params = []

        for item in self.data['admhierarchy']:
            if item['ISACTIVE'] in settings.true_values:
                full_path_data = {}
                for key in item['PATH'].split('.'):
                    full_path_data.update(
                        {key: self._find_all_docs_by_id(key)})

        for key, value in full_path_data.items():
            part_path_keys = value.keys()

            if 'apartmentsparams' in part_path_keys:
                for item in value['apartmentsparams']:
                    try:
                        param_type = self.database.get_coll('paramtypes').find_one({
                            'ID': item['TYPEID'],
                            'ISACTIVE': {'$in': settings.true_values},
                        })
                        for elem in value['reestrobjects']:
                            if elem['ISACTIVE'] in settings.true_values:
                                object_level_name = self.database.get_coll('objectlevels').find_one({
                                    'LEVEL': elem['LEVELID'],
                                    'ISACTIVE': {'$in': settings.true_values},
                                })['NAME']
                        full_params.append({
                            'ObjectID': key,
                            'Object Level Name': object_level_name,
                            'Param Type': param_type['NAME'],
                            'Param Value': item['VALUE'],
                            'Param Type Description': param_type['DESC']})
                    except:
                        pass

            if 'housesparams' in part_path_keys:
                for item in value['housesparams']:
                    try:
                        param_type = self.database.get_coll('paramtypes').find_one({
                            'ID': item['TYPEID'],
                            'ISACTIVE': {'$in': settings.true_values},
                        })
                        for elem in value['reestrobjects']:
                            if elem['ISACTIVE'] in settings.true_values:
                                object_level_name = self.database.get_coll('objectlevels').find_one({
                                    'LEVEL': elem['LEVELID'],
                                    'ISACTIVE': {'$in': settings.true_values},
                                })['NAME']
                        full_params.append({
                            'ObjectID': key,
                            'Object Level Name': object_level_name,
                            'Param Type': param_type['NAME'],
                            'Param Value': item['VALUE'],
                            'Param Type Description': param_type['DESC'],
                        })
                    except:
                        pass

            if 'addrobjparams' in part_path_keys:
                for item in value['addrobjparams']:
                    if item["CHANGEIDEND"] == "0":
                        try:
                            param_type = self.database.get_coll('paramtypes').find_one({
                                'ID': item['TYPEID'],
                                'ISACTIVE': {'$in': settings.true_values},
                            })
                            for elem in value['reestrobjects']:
                                if elem['ISACTIVE'] in settings.true_values:
                                    object_level_name = self.database.get_coll('objectlevels').find_one({
                                        'LEVEL': elem['LEVELID'],
                                        'ISACTIVE': {'$in': settings.true_values},
                                    })['NAME']
                            full_params.append({
                                'ObjectID': key,
                                'Object Level Name': object_level_name,
                                'Param Type': param_type['NAME'],
                                'Param Value': item['VALUE'],
                                'Param Type Description': param_type['DESC'],
                            })
                        except:
                            pass

        return full_params


# ========================================


# class GeoObject:
#     def __init__(self, type: Literal['Point', 'LineString', 'Polygon', 'MultiPolygon'], coordinates: list | tuple):
#         self.type = type
#         if self.type == 'Point':
#             if not isinstance(coordinates, (list, tuple)) or len(coordinates) != 2:
#                 raise ValueError(
#                     coordinates, 'must be a list or tuple of two floats')
#         elif self.type == 'LineString':
#             pass  # TODO:
#         self.coordinates = coordinates

#     def to_dict(self) -> dict:
#         return {
#             "type": self.type,
#             "coordinates": self.coordinates
#         }

#     def cacl(self, ndigit: int = None):
#         """
#         Returns the area (for polygons) or length (for lines) of the geo object.
#         """
#         if self.type == "line":
#             length = 0
#             for i in range(len(self.coordinates) - 1):
#                 point1 = self.coordinates[i]
#                 point2 = self.coordinates[i+1]
#                 length += math.sqrt((point1[0]-point2[0])
#                                     ** 2 + (point1[1]-point2[1])**2)
#                 if ndigit is not None:
#                     length = round(length, ndigit)
#                 return length


# @dataclass
# class BaseObject:
#     id: int
#     name: str
#     geoobject: GeoObject

#     def full_data_by_id(self, id: int) -> dict:
#         """Returns all the data for a specific object, given its ID"""
#         pass

#     def name_by_id(self, id: int) -> str:
#         """Returns the name of a specific object, given its ID"""
#         pass

#     def id_by_name(self, name: str) -> int:
#         """Returns the ID of a specific object, given its name"""
#         pass

#     def geo_object_by_id(self, id: int) -> GeoObject:
#         """Returns the geographic object that describes the object's location,
#         represented as a point, line, or polygon, for a specific object,
#         given its ID."""
#         pass


# bod_client = BODClient()


# class BODObject:
#     """Represents the city"""

#     def __init__(self, object_id: int):
#         self.object_id = object_id
#         self.parent_obj = BODObject() # add parent_id
#         self.level_id, self.type = self._get_level_name()
#         fltr = {'OBJECTID': str(self.object_id),
#                 'ISACTUAL': {'$in': settings.true_values}}
#         collection = settings.levels.get(str(self.level_id)).get('collection')
#         if self.level_id < 9:
#             self.name = bod_client.get_db('BoD').get_coll(collection).find(fltr)

#     def _get_level_name(self):
#         fltr = {'OBJECTID': str(self.object_id),
#                 'ISACTUAL': {'$in': settings.true_values}}
#         level_id = bod_client.get_db('BoD').get_coll('reestrobjects').find_one(fltr)['LEVELID']
#         name = settings.levels.get(str(level_id)).get('attr')
#         return int(level_id), str(name)


# # =================================================================


# class BODCity:
#     """Represents the city"""

#     def __init__(self, object_id: int):
#         self.object_id = object_id
#         fltr = {'OBJECTID': str(object_id),
#                 'ISACTUAL': {'&in': settings.true_values}}
#         data = bod_client.get_db('BoD').get_coll('addrobj').find_one(fltr)
#         if data is None:

#         self.name = ''  # find the name of the city

#     def get_street(self, object_id: int = None, name: str = None):
#         """Returns Street object by its id or name"""
#         if object_id is not None:
#             pass
#         elif name is not None:
#             fltr = {'NAME'}
#             bod_client.get_db('BoD').get_coll('addrobj').find_one(fltr)
#         else:
#             raise ValueError()

#     def get_streets(self):
#         """Returns the list of Streets objects related to the city"""
#         streets_ids = set(pd.DataFrame(bod_client.get_db('BoD').get_coll(
#             'reestrobjects').find({'LEVELID': '8', 'ISACTIVE': '1'}))['OBJECTID'])
#         related_objects = set(pd.DataFrame(bod_client.get_db('BoD').get_coll(
#             'admhierarchy').find({'PATH': {'$regex': self.object_id + r'\.\d+$'},
#                                   'ISACTIVE': '1'}))['OBJECTID'])
#         source = list(streets_ids & related_objects)
#         streets = [BODStreet(int(item), city=self) for item in source]
#         return streets

#     def get_houses(self):
#         """Returns the list of Houses objects related to the city"""
#         streets = self.get_streets()
#         houses = []
#         for street in streets:
#             houses.append(*(street.get_houses()))
#         return houses


# class BODStreet:
#     """Represents the street"""

#     def __init__(self, object_id: int, city: BODCity = None) -> None:
#         self.object_id = object_id
#         self.name = ''
#         if city is not None:
#             self.city = city
#         else:
#             city_id = 0
#             self.city = BODCity(city_id)

#     def find_house(self, object_id: int):
#         """Returns House object by its id"""
#         return BODHouse(object_id, street=self)

#     def get_houses(self):
#         """Returns the list of Houses objects related to the city"""
#         houses = []

#         return houses


# class BODHouse:
#     """Represents the house"""

#     def __init__(self, object_id: int, street: BODStreet = None) -> None:
#         fltr = {'OBJECTID': str(object_id),
#                 'ISACTIVE': {'$in': settings.true_values}}
#         data: dict = bod_client.get_db('BoD').get_coll('objectlevels').find_one(fltr)
#         if data is not None:
#             if int(data.get('LEVELID')) == 10:
#                 self.object_id = object_id
#             else:
#                 raise ValueError(object_id, 'object must have level equal to 10')
#         if street is not None:
#             self.street = street
#         else:
#             fltr = {'OBJECTID': object_id,
#                     'ISACTIVE': {'$in': settings.true_values}}
#             data: dict = bod_client.get_db('BoD').get_coll('munhierarchy').find_one(fltr)
#             if data is not None:
#                 street_id = data.get('PARENTOBJID')
#                 if street_id is not None:
#                     street_id = int(street_id)
#                     self.street = BODStreet(street_id)

#     def get_address(self) -> str:
#         pass

    # def get_
