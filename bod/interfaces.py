"""
bod > `interfaces`
------------------
The module for spacial objects.
"""

# from typing import Any, Optional

from pymongo.database import Database

from bod.fias.versions import Versions
from bod.logging import get_logger
from bod.objects import House, KeysType, KeyType, Place, Street
from bod.settings import Settings

logger = get_logger(__name__)


class BaseInterface:
    """
    Base class for interfaces.

    Paramaters
    ----------
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, database: Database, settings: Settings) -> None:
        self._settings = settings
        self._database = database

    def _find_one(self, key: KeyType, coll_name: str): ...

    def _find(self, keys: KeysType, coll_name: str): ...

    def _insert_one(self, data: dict, coll_name: str): ...

    def _insert(self, data: list[dict], coll_name: str): ...


class IPlaces(BaseInterface):
    """
    Interface for countries, provinces, states, localities, cities and districts.

    Paramaters
    ----------
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, database: Database, settings: Settings) -> None:
        logger.info('Places interface initializing...')
        super().__init__(database, settings)

    def get_place(self, key: KeyType) -> Place:
        """Returns the place with the given key."""
        self._find_one(key, 'places')

    def get_places(self, keys: KeysType) -> list[Place]:
        """Returns the list of places with the given keys."""
        self._find(keys, 'places')


class IStreets(BaseInterface):
    """
    Interface for streets.

    Paramaters
    ----------
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, database: Database, settings: Settings) -> None:
        logger.info('Streets interface initializing...')
        super().__init__(database, settings)

    def get_street(self, key: KeyType) -> Street:
        """Returns the street with the given key."""
        self._find_one(key, 'streets')

    def get_streets(self, keys: KeysType) -> list[Street]:
        """Returns the list of streets with the given keys."""
        self._find(keys, 'streets')


class IHouses(BaseInterface):
    """
    Interface for houses.

    Paramaters
    ----------
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, database: Database, settings: Settings) -> None:
        logger.info('Houses interface initializing...')
        super().__init__(database, settings)

    def get_house(self, key: KeyType) -> House:
        """Returns the house with the given key."""
        self._find_one(key, 'houses')

    def get_houses(self, keys: KeysType) -> list[House]:
        """Returns the list of houses with the given keys."""
        self._find(keys, 'houses')


class IConstants(BaseInterface):
    """
    Allows to manage the constants in the database.

    Paramaters
    ----------
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, database: Database, settings: Settings) -> None:
        logger.info('Constants interface initializing...')
        super().__init__(database, settings)

    def get_constant(self, uid: str): ...

    def get_constant_by_title(self, title: str): ...


class IInternal(BaseInterface):
    """
    Interface for internal processes.

    Paramaters
    ----------
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, database: Database, settings: Settings) -> None:
        super().__init__(database, settings)


class FiasInterface:
    """
    Interface for FIAS.

    Paramaters
    ----------
    database : pymongo.database.Database
        Database object, must be provided from parent object.
    settings : Settings
        Settings object, must be provided from parent object.
    """

    def __init__(self, database: Database, settings: Settings) -> None:
        self.database = database
        self.settings = settings
        self.versions = Versions(
            current_version=self.settings.fias.current_version,
            database=self.database,
            settings=self.settings
        )
