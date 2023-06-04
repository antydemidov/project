"""
BoD Settings
============
The module contains the class `BODSettings`.
"""

import json
import os
from urllib.parse import quote_plus


class Settings(object):
    """
    bod > settings > `Settings`
    ---------------------------
    The object used to store settings of the project.

    Attributes:
    -----------
    - `dgrad` : OBJECTID of Dimitrovgrad;
    - `actual_db` : the name of the actual database;
    - `actual_db_desc` : the name of the actual schema database;
    - `current_version` : the ID of current version in format "YYYYMMDD";
    - `update_link` : the link to the list of new versions of records for database;
    - `authmechanism` : Literal indicating mechanism to authentication;
    - `authsource` : the name of database for authentication;
    - `default_chunk_size` : default chunk size in items;
    - `default_chunk_size_mb` : default chunk size in megabytes;
    - `path_schema` : the name of the directory containing the XSD-files of schema;
    - `uri` : the connection URI for the database;
    - `true_values` : the list of true values;
    - `levels` : the mapping of levels IDs to name and attributes.

    Methods:
    --------
    - `load()` - Reads the settings.json file and put it into attributes of the BODSettings object.
    - `update(key, value)` - Reseives key and value of the attribute and put it into the attribute
    and update the settings.json.
    """

    UTF8 = 'utf-8'
    LEVELS = {
        '1': {'name': 'Субъект РФ',
              'attr': 'region',
              'collection': 'addrobj'},
        '2': {'name': 'Административный район',
              'attr': 'admarea',
              'collection': 'addrobj'},
        '3': {'name': 'Муниципальный район',
              'attr': 'munarea',
              'collection': 'addrobj'},
        '4': {'name': 'Сельское/городское поселение',
              'attr': 'settlement',
              'collection': 'addrobj'},
        '5': {'name': 'Город',
              'attr': 'city',
              'collection': 'addrobj'},
        '6': {'name': 'Населенный пункт',
              'attr': 'locality',
              'collection': 'addrobj'},
        '7': {'name': 'Элемент планировочной структуры',
              'attr': 'elplanstructure',
              'collection': 'addrobj'},
        '8': {'name': 'Элемент улично-дорожной сети',
              'attr': 'elroadnetwork',
              'collection': 'addrobj'},
        '9': {'name': 'Земельный участок',
              'attr': 'stead',
              'collection': 'steads'},
        '10': {'name': 'Здание (сооружение)',
               'attr': 'building',
               'collection': 'houses'},
        '11': {'name': 'Помещение',
               'attr': 'premice',
               'collection': 'apartments'},
        '12': {'name': 'Помещения в пределах помещения',
               'attr': 'premiceinpremice',
               'collection': 'rooms'},
        '13': {'name': 'Уровень автономного округа (устаревшее)',
               'attr': 'autodistrict',
               'collection': 'addrobj'},
        '14': {'name': 'Уровень внутригородской территории (устаревшее)',
               'attr': 'innercityterr',
               'collection': 'addrobj'},
        '15': {'name': 'Уровень дополнительных территорий (устаревшее)',
               'attr': 'addterr',
               'collection': 'addrobj'},
        '16': {'name': 'Уровень объектов на дополнительных территориях (устаревшее)',
               'attr': 'objaddterr',
               'collection': 'addrobj'},
        '17': {'name': 'Машино-место',
               'attr': 'carplace',
               'collection': 'carplaces'}
    }
    TRUE_VALUES = [1, '1', 'true', 'True']
    __data = {}

    def __init__(self) -> None:
        self.load()
        self.dgrad: int = int(self.__data.get('dgrad', 0))
        self.actual_db: str = self.__data.get('actual_db', '')
        self.actual_db_desc: str = self.__data.get('actual_db_desc', '')
        self.current_version: int = self.__data.get('current_version', 0)
        self.update_link: str = self.__data.get('update_link', '')
        self.default_chunk_size: int = self.__data.get('default_chunk_size', 0)
        self.default_chunk_size_mb: int = self.__data.get('default_chunk_size_mb', 0)
        self.default_timeout: int = self.__data.get('default_timeout', 0)
        self.path_schema: str = self.__data.get('path_schema', '')
        self.uri = self.__build_uri()

    def __build_uri(self):
        host: str = os.environ.get('MONGO_HOST', default='')
        port: str = os.environ.get('MONGO_PORT', default='')
        user: str = quote_plus(os.environ.get('MONGO_USERNAME', default=''))
        password: str = quote_plus(
            os.environ.get('MONGO_PASSWORD', default=''))
        authmechanism = None
        authsource = None
        return f'mongodb://{user}:{password}@{host}:{port}/?authMechanism=\
            {authmechanism}&authSource={authsource}'

    # Reads the settings.json file and put it into attributes of the Settings
    # object.
    @classmethod
    def load(cls):
        """Reads the settings.json file and put it into attributes of the
        Settings object."""
        try:
            with open('settings.json', 'r', encoding=cls.UTF8) as file:
                cls.__data.update(json.load(file))
        except NameError as error:
            error.add_note('Check the file settings.json')
            raise error

    # Reseives key and value of the attribute and put it into the attribute
    # and update the settings.json.
    def update(self, key, value):
        """Reseives key and value of the attribute and put it into the attribute
        and update the settings.json."""
        type(self).__data.update({key: value})
        setattr(self, key, value)

    @classmethod
    def dump(cls):
        """Dumps the settings data to the file."""
        with open('settings.json', 'w', encoding=cls.UTF8) as file:
            file.write(json.dumps(cls.__data))
