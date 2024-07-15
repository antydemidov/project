"""
Utilities
---------
The collection of functions used in the project.
"""

from pymongo.database import Database

from bod.fias.objects import (Addrobj, Addrobjdivision, Admhierarchy,
                              Apartments, Carplaces, Changehistory,
                              Houses, Munhierarchy, Normativedocs,
                              Normativedocskinds, Objectlevels, Params,
                              Reestrobjects, Rooms, Steads, Types)
from bod.settings import Settings


def find_related_objects(db: Database, settings: Settings, object_id: int | str = None):
    """Finds all related objects."""

    if not object_id:
        object_id = settings.fias.city_code
    filter_adm = {'PATH': {'$regex': str(object_id)}}
    filter_mun = {'PATH': {'$regex': str(object_id)}}
    projection = {'_id': False, 'OBJECTID': True}

    objects_adm = db.get_collection('admhierarchy').find(
        filter_adm, projection=projection)
    objects_mun = db.get_collection('munhierarchy').find(
        filter_mun, projection=projection)
    objects_ids = objects_adm + objects_mun

    related_object = []
    for item in objects_ids:
        related_object.append(item['OBJECTID'])
    related_object = list(set(related_object))

    return related_object


# def cut_tree(db: Database, coll_name: str, chosen_ids: list):
#     """
#     Cuts the tree.
#     """
#     collection = db.get_collection(coll_name)

#     id_column = 'ID'
#     if coll_name != 'addrobjdivision':
#         id_column = 'OBJECTID'
#     _filter = {id_column: {'$not': {'$in': chosen_ids}}}

#     collection.delete_many(_filter)


def coll_by_level(_key: int | str):
    """Returns the collection name for a given level."""

    _map = {
        1: 'addrobj',
        2: 'addrobj',
        3: 'addrobj',
        4: 'addrobj',
        5: 'addrobj',
        6: 'addrobj',
        7: 'addrobj',
        8: 'addrobj',
        9: 'steads',
        10: 'houses',
        11: 'apartments',
        12: 'rooms',
        13: 'addrobj',
        14: 'addrobj',
        15: 'addrobj',
        16: 'addrobj',
        17: 'carplaces'
    }

    if isinstance(_key, str) and _key.isdigit():
        _key = int(_key)
    if _key in _map:
        return _map[_key]
    return None


def params_by_level(_key: int | str):
    """Returns the collection name for a given level."""

    coll = coll_by_level(_key)
    if not coll:
        return None
    return coll + 'params'


def validator_by_coll(coll_name: str):
    """Returns the class to validate and transform the raw data."""

    if 'params' in coll_name:
        return Params
    if 'types' in coll_name:
        return Types

    _map = {
        'addrobj': Addrobj,
        'addrobjdivision': Addrobjdivision,
        'admhierarchy': Admhierarchy,
        'apartments': Apartments,
        'carpaces': Carplaces,
        'changehistory': Changehistory,
        'houses': Houses,
        'munhierarchy': Munhierarchy,
        'normativedocs': Normativedocs,
        'normativedocskinds': Normativedocskinds,
        'objectlevels': Objectlevels,
        'reestrobjects': Reestrobjects,
        'rooms': Rooms,
        'steads': Steads
    }
    return _map.get(coll_name, None)


def unique_field_by_coll(coll_name: str) -> str:
    """Returns unique field by collection name."""

    _map = {
        'changehistory': 'CHANGEID',
        'objectlevels': 'LEVEL',
        'reestrobjects': 'OBJECTID'
    }

    if coll_name in _map:
        return _map[coll_name]
    return 'ID'
