"""
Settings
--------
The module contains the class `Settings`. Use `build_settings()` function to
build the `Settings` object. You can also use `Settings()` to create it from
the data you got outside the settings.
"""

import json
import os
from typing import Any, Optional
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic import (
    BaseModel,
    ConfigDict,
    DirectoryPath,
    Field,
    ValidationError
)

from bod.logging import get_logger

__all__ = [
    'build_settings'
]

logger = get_logger(__name__)


class FiasSettings(BaseModel):
    """Internal part of Settings."""
    model_config = ConfigDict(extra='allow', validate_assignment=True)

    database_name: str
    database_desc: Optional[str] = None
    database_raw_db: Optional[str] = None
    database_clean_db: Optional[str] = None
    database_final: Optional[str] = None
    region_code: str
    city_code: int
    current_version: int
    update_link: str


class MkrfSettings(BaseModel):
    """Internal part of Settings."""
    model_config = ConfigDict(extra='allow', validate_assignment=True)

    database_name: Optional[str] = None
    mkrf_key: Optional[str] = os.environ.get('MKRF_KEY', default=None)


class FrtSettings(BaseModel):
    """Internal part of Settings."""
    model_config = ConfigDict(extra='allow', validate_assignment=True)


class Settings(BaseModel):
    """
    The object used to store settings of the project.

    Attributes
    ----------
    authmechanism : str
        Literal indicating mechanism to authentication.
    authsource : str
        The name of database for authentication.
    default_timeout : int
        The default timeout for the connection.
    default_chunk_size : int
        Default chunk size in items.
    default_chunk_size_mb : int
        Default chunk size in megabytes.
    path_schema : str
        The name of the directory containing the XSD-files of schema.

    Methods
    -------
    get(key='host', default=None)
        Returns the value by the given key or default. 
    dump()
        Dumps the settings values to the .json-file.
    """

    model_config = ConfigDict(extra='ignore', validate_assignment=True)

    authmechanism: str = 'DEFAULT'
    authsource: str = 'admin'
    default_chunk_size: int = 1000
    default_chunk_size_mb: int = 10
    default_timeout: int = 300
    path_schema: Optional[DirectoryPath] = None
    database_name: str = 'BoD'
    true_values: list = [1, '1', 'true', 'True']

    fias: FiasSettings = Field(defailt_factory=dict)
    mkrf: MkrfSettings = Field(defailt_factory=dict)
    frt: FrtSettings = Field(defailt_factory=dict)

    @property
    def mongo_uri(self):
        """Returns the URI for connection to database."""

        host: str = os.environ.get('MONGO_HOST', default=None)
        port: str = os.environ.get('MONGO_PORT', default=None)
        user: str = quote_plus(os.environ.get('MONGO_USERNAME', default=None))
        password: str = quote_plus(os.environ.get('MONGO_PASSWORD', default=None))

        return (f'mongodb://{user}:{password}@{host}:{port}/'
                + f'?authmechanism={self.authmechanism}'
                + f'&authsource={self.authsource}')

    def get(self, key: str, default: Any = None):
        """Returns the value of the given key, or default if key does not exist."""
        return getattr(self, key, default)

    def dump(self):
        """Saves the settings as json to the file."""

        with open('settings.json', 'w', encoding='utf-8') as f:
            f.write(self.model_dump_json(
                exclude=['host', 'port', 'user', 'password', 'mkrf_key'],
                exclude_defaults=True,
                exclude_none=True,
                indent=2
            ))


def build_settings():
    """Builds the settings object."""

    dotenv_path = os.path.join('.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    settings = None
    with open('settings.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    try:
        settings = Settings(**data)
    except ValidationError as e:
        logger.error(e)
    return settings
