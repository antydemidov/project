"""
Address objects
---------------
This is a collection of objects in Building of Dimitrovgrad project.
"""


from pymongo.database import Database

from bod.fias.objects import (
    FiasObject,
    Hierarchy,
    Params,
    Reestrobjects
)
from bod.fias.utils import coll_by_level, params_by_level, validator_by_coll
from bod.settings import Settings


class Object:
    """
    Description.

    Parameters
    ----------
    object_id : str | int
        desc
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, object_id: int, database: Database, settings: Settings):
        self._is_loaded = False
        self.object_id = object_id
        self.database = database
        self.settings = settings
        self.obj = None

    def new(self, object_id: int):
        """Builds a new object by its ID."""

        return Object(object_id, self.database, self.settings)

    def load(self):
        """Loads the information from the database."""

        source = self.database.get_collection(
            'reestrobj').find_one({'object_id': self.object_id})
        data = Reestrobjects(**source)
        obj = FiasObject()
        obj.object_id = self.object_id
        obj.object_guid = data.object_guid
        obj.level_id = data.level_id

        coll = coll_by_level(obj.level_id)
        source = self.database.get_collection(coll).find_one({'object_id': obj.object_id})
        data = validator_by_coll(coll)(**source)
        obj.type_id = data.type_id
        obj.title = data.name or data.number

        source = self.database.get_collection('admhierarchy').find_one({'object_id': obj.object_id})
        data = Hierarchy(**source)
        obj.parent_obj_id_adm = data.parent_obj_id
        obj.path_adm = data.path
        source = self.database.get_collection('munhierarchy').find_one({'object_id': obj.object_id})
        data = Hierarchy(**source)
        obj.parent_obj_id_mun = data.parent_obj_id
        obj.path_mun = data.path

        obj.params = self.get_params()

        self.obj = obj
        self._is_loaded = True

    def get_parent(self, hierarchy: int = 0) -> "Object" | None:
        """
        Returns the parent object of the current object.

        Parameters
        ----------
        hierarchy : int
            0 - admhierarchy, 1 - munhierarchy

        Returns
        -------
        Object
        """
        hierarchy = 'admhierarchy' if not hierarchy else 'munhierarchy'
        data = self.database.get_collection(hierarchy).find_one({
            'object_id': self.object_id,
            'is_active': True
        }, projection={'_id': False, 'object_id': True})

        if not data:
            return None
        obj = Hierarchy(**data)
        return self.new(obj.parent_obj_id)

    def get_children(self, hierarchy: int = 0) -> list["Object" | None]:
        """
        Description.

        Parameters
        ----------
        hierarchy : int
            0 - admhierarchy, 1 - munhierarchy.
        """
        children = []
        hierarchy = 'admhierarchy' if not hierarchy else 'munhierarchy'

        with self.database.get_collection(hierarchy).find({
            'parentobjid': self.object_id,
            'is_active': True,
        }, projection={'_id': False, 'object_id': True}) as data:
            for item in data:
                try:
                    obj = Hierarchy(**item)
                    children.append(obj.object_id)
                except Exception as e:
                    pass  # TODO: handle exception
        return children

    def get_parents(self): ...

    def get_full_address(self): ...

    def get_path(self, hierarchy: int = 0):
        """
        Description.

        Parameters
        ----------
        hierarchy : int
            0 - admhierarchy, 1 - munhierarchy.

        Returns
        -------
        list[int]
            A list of object IDs.
        """

        hierarchy = 'admhierarchy' if not hierarchy else 'munhierarchy'
        data = self.database.get_collection(hierarchy).find_one({
            'id': self.object_id,
            'is_active': True
        })
        validator = validator_by_coll(hierarchy)
        if not validator:
            return None

        obj = validator(**data)
        return [int(object_id) for object_id in obj.path.split('.')]

    def get_path_data(self) -> tuple:
        """Description."""

        return ([self.new(object_id) for object_id in self.get_path()])

    def get_params(self) -> list:
        """Description."""

        coll = params_by_level(self.obj.level_id)
        params = self.database.get_collection(coll).find(
            {'object_id': self.object_id})
        full_params = []

        for param in params:
            obj = Params(**param)
            # type_src = self.database.get_collection('paramtypes').find_one({
            #     'id': obj.type_id,
            #     'is_active': True
            # })
            # param_type = Types(**type_src)
            full_params.append({
                'type_id': obj.type_id,
                'value': obj.value
            })

        return full_params
