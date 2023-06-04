# from werkzeug.security import generate_password_hash, check_password_hash
#
# class User(users):
#
#    def set_password(self, password):
#        self.password_hash = generate_password_hash(password)
#
#    def check_password(self, password):
#        return check_password_hash(self.password_hash, password)

import bod.mongodb_connection as mc

__all__ = [
    'Addrobj_list',
    'Addrobj',
    'House_list',
    'House',
]


# ADDRESS OBJECT


class Addrobj_list:

    def get_data(limit: int, skip: int):
        main_keys = {
            'addrobj': ['NAME', 'TYPENAME', 'LEVEL']
        }

        addrobj_list = {}

        data = list(mc.addrobj.mongo.find(
            filter={'ISACTIVE': '1'}, limit=limit, skip=skip))

        for item in data:
            item = dict(item)
            addrobj_list.update({item['OBJECTID']: {}})
            objectid = item['OBJECTID']
            for key, value in item.items():
                if key in main_keys['addrobj']:
                    addrobj_list[objectid].update({key: value})

        return addrobj_list


class Addrobj:

    def get_data(objectid: str):
        main_keys = {
            'addrobj': ['OBJECTID', 'NAME', 'TYPENAME', 'LEVEL', 'PARENTOBJID', 'PATH'],
            'munhierarchy': ['OKTMO', 'PATH'],
            'addrobjparams': ['TYPEID', 'VALUE'],
            'paramtypes': ['NAME', 'DESC', 'CODE'],
            'houses': ['OBJECTID', 'HOUSENUM', 'HOUSETYPE'],
            'housesparams': ['TYPEID', 'VALUE'],
            'housetypes': ['NAME', 'SHORTNAME', 'DESC']
        }

        obj = {}

        for key, value in mc.addrobj.mongo.find_one({'OBJECTID': objectid, 'ISACTIVE': '1'}).items():
            if key in main_keys['addrobj']:
                obj.update({str(key): str(value)})
        obj.update({'LEVEL_NAME': mc.objectlevels.find_one(
            {'LEVEL': obj['LEVEL']})['NAME']})

        for key, value in mc.munhierarchy.mongo.find_one({'OBJECTID': objectid, 'ISACTIVE': '1'}).items():
            if key in main_keys['munhierarchy']:
                obj.update({str(key): str(value)})

        parentobjid = mc.munhierarchy.mongo.find_one(
            {'OBJECTID': objectid, 'ISACTIVE': '1'}).get('PARENTOBJID')
        for key, value in mc.addrobj.find_one({'OBJECTID': parentobjid, 'ISACTIVE': '1'}).items():
            if key in main_keys['addrobj']:
                obj.update({'PARENT_' + str(key): str(value)})
        obj.update({'PARENT_LEVEL_NAME': mc.objectlevels.mongo.find_one(
            {'LEVEL': obj['PARENT_LEVEL']})['NAME']})

        addrobjparams = list(mc.addrobjparams.mongo.find(
            {'OBJECTID': objectid}))
        paramtypes = mc.paramtypes
        for i in range(len(addrobjparams)):
            for key, value in dict(addrobjparams[i]).items():
                if key in main_keys['addrobjparams']:
                    obj.update(
                        {'PARAM_' + str(i+1) + '_' + str(key): str(value)})
            for key, value in paramtypes.mongo.find_one({'ID': dict(addrobjparams[i])['TYPEID']}).items():
                if key in main_keys['paramtypes']:
                    obj.update(
                        {'PARAM_' + str(i+1) + '_' + str(key): str(value)})

        children = list(mc.munhierarchy.mongo.find(
            {'PARENTOBJID': objectid}))
        children_list = []
        for item in children:
            children_list.append(dict(item)['OBJECTID'])
        obj.update({'CHILDREN': children_list})

        return obj


class House_list:

    def get_data():
        pass


class House:

    def get_data(objectid: str):
        main_keys = {
            'addrobj': ['OBJECTID', 'NAME', 'TYPENAME', 'LEVEL', 'PARENTOBJID', 'PATH'],
            'munhierarchy': ['OKTMO', 'PATH'],
            'addrobjparams': ['TYPEID', 'VALUE'],
            'paramtypes': ['NAME', 'DESC', 'CODE'],
            'houses': ['OBJECTID', 'HOUSENUM', 'HOUSETYPE'],
            'housesparams': ['TYPEID', 'VALUE'],
            'housetypes': ['NAME', 'SHORTNAME', 'DESC']
        }
        obj = {}

        for key, value in mc.houses.mongo.find_one({'OBJECTID': objectid, 'ISACTIVE': '1'}).items():
            if key in main_keys['houses']:
                obj.update({str(key): str(value)})

        for key, value in mc.housetypes.mongo.find_one({'ID': obj['HOUSETYPE'], 'ISACTIVE': 'true'}).items():
            if key in main_keys['housetypes']:
                obj.update({'HOUSETYPES_' + str(key): str(value)})

        for key, value in mc.munhierarchy.mongo.find_one({'OBJECTID': objectid, 'ISACTIVE': '1'}).items():
            if key in main_keys['munhierarchy']:
                obj.update({str(key): str(value)})

        parentobjid = mc.munhierarchy.mongo.find_one(
            {'OBJECTID': objectid, 'ISACTIVE': '1'}).get('PARENTOBJID')
        for key, value in mc.addrobj.mongo.find_one({'OBJECTID': parentobjid, 'ISACTIVE': '1'}).items():
            if key in main_keys['addrobj']:
                obj.update({'PARENT_1_' + str(key): str(value)})
        obj.update({'PARENT_1_LEVEL_NAME': mc.objectlevels.mongo.find_one(
            {'LEVEL': obj['PARENT_1_LEVEL']})['NAME']})

        parentobjid = mc.munhierarchy.mongo.find_one(
            {'OBJECTID': parentobjid, 'ISACTIVE': '1'}).get('PARENTOBJID')
        for key, value in mc.addrobj.mongo.find_one({'OBJECTID': parentobjid, 'ISACTIVE': '1'}).items():
            if key in main_keys['addrobj']:
                obj.update({'PARENT_2_' + str(key): str(value)})
        obj.update({'PARENT_2_LEVEL_NAME': mc.objectlevels.mongo.find_one(
            {'LEVEL': obj['PARENT_2_LEVEL']})['NAME']})

        parentobjid = mc.munhierarchy.mongo.find_one(
            {'OBJECTID': parentobjid, 'ISACTIVE': '1'}).get('PARENTOBJID')
        for key, value in mc.addrobj.find_one({'OBJECTID': parentobjid, 'ISACTIVE': '1'}).items():
            if key in main_keys['addrobj']:
                obj.update({'PARENT_3_' + str(key): str(value)})
        obj.update({'PARENT_3_LEVEL_NAME': mc.objectlevels.find_one(
            {'LEVEL': obj['PARENT_3_LEVEL']})['NAME']})

        housesparams = list(mc.housesparams.find({'OBJECTID': objectid}))
        paramtypes = mc.paramtypes
        for i in range(len(housesparams)):
            for key, value in dict(housesparams[i]).items():
                if key in main_keys['housesparams']:
                    obj.update(
                        {'PARAM_' + str(i+1) + '_' + str(key): str(value)})
            for key, value in paramtypes.find_one({'ID': dict(housesparams[i])['TYPEID']}).items():
                if key in main_keys['paramtypes']:
                    obj.update(
                        {'PARAM_' + str(i+1) + '_' + str(key): str(value)})

        obj.update({'FULL_ADDRESS': obj['HOUSETYPES_SHORTNAME'] + ' ' + obj['HOUSENUM'] + ', ' + obj['PARENT_1_NAME'] +
                   ' ' + obj['PARENT_1_TYPENAME'] + '., ' + obj['PARENT_3_NAME'] + ', Российская Федерация'})

        return obj
