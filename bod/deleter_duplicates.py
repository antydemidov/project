"""Description"""

from .utils import sort_dict

# Map for unique fields of each collection
map_of_unique_fields = {
    'addrobj': 'ID',
    'carplacesparams': 'ID',
    'objectlevels': 'LEVEL',
    'paramtypes': 'ID',
    'normativedocs': 'ID',
    'apartmentsparams': 'ID',
    'addhousetypes': 'ID',
    'apartmenttypes': 'ID',
    'steads': 'ID',
    'roomsparams': 'ID',
    'addrobjtypes': 'ID',
    'operationtypes': 'ID',
    'housetypes': 'ID',
    'addrobjdivision': 'ID',
    'apartments': 'ID',
    'changehistory': 'CHANGEID',
    'carplaces': 'ID',
    'housesparams': 'ID',
    'normativedocskinds': 'ID',
    'rooms': 'ID',
    'roomtypes': 'ID',
    'steadsparams': 'ID',
    'reestrobjects': 'OBJECTID',
    'addrobjparams': 'ID',
    'houses': 'ID',
    'normativedocstypes': 'ID',
    'munhierarchy': 'ID',
    'admhierarchy': 'ID'
}

map_of_unique_fields = sort_dict(map_of_unique_fields)

def delete_duplicates_v2(db: "Database", uniq_map: dict):
    def internal_func(coll_name: str, uniq_field: str):
        # Find all docs with duplicates
        uniq_field = "$" + uniq_field
        coll = db.get_coll(coll_name)
        pipeline = [
            {'$group': {
                '_id': [uniq_field],
                'dups': {'$addToSet': '$_id'},
                'count': {'$sum': 1}
            }},
            {'$match': {
                'count': {'$gt': 1}
            }}
        ]
        print('Searching duplicates in "' + coll_name + '"')
        dups = coll.aggregate(pipeline, allowDiskUse=True)

        # Create a list of ObjectIDs to remove
        delete_this = []
        for dup in dups:
            for obj in dup['dups'][1:]:
                delete_this.append(obj)

        j = len(delete_this)
        if j != 0:
            if j > 100:
                chunk = j // 100
            else:
                chunk = j
            i = 0
            print('"' + coll_name + '" in processing')
            count_chunks = j // chunk
            itr = 1
            while i < j:
                tmp = delete_this[i:i+chunk]
                coll.delete_many({'_id': {'$in': tmp}})
                i += chunk
                print('\r|' + '.' * itr + ' ' *
                      (count_chunks - itr) + '|', end='')
                itr += 1
            print('"' + coll_name + '" is done')
        else:
            print("Found no duplicates")

    for coll_name in uniq_map.keys():
        uniq_field = uniq_map[coll_name]
        if uniq_field is not None:
            internal_func(coll_name, uniq_field)
