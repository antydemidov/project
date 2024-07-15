"""
Clients
-------
The module for the client of data sources.
"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from bod.logging import get_logger
from bod.settings import build_settings

logger = get_logger(__name__)


def get_client(uri: str):
    """
    Gets the database by the given name.
    
    Parameters
    ----------
    uri : str
        The URI to the database.
    database_name : str
        The name of needed database.
    """

    client = None
    try:
        logger.info('Connecting to MongoDB...')
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        assert client.server_info().get('ok', False) == 1
        logger.info('Connection is established.')
    except (ServerSelectionTimeoutError, AssertionError) as err:
        logger.error(err)
    return client


# def get_database(client: MongoClient, database_name: str):
#     database = None
#     try:
#         logger.info('Getting the database "%s"...', database_name)
#         assert database_name in client.list_database_names()
#         database = client.get_database(database_name)
#         logger.info('Database "%s" is accessed.', database_name)
#     except AssertionError as err:
#         logger.error(err)
#     return database


class Client:
    """
    The main client to interract with databases.

    Attributes
    ----------
    database : pymongo.database.Database
        desc
    settings : Settings
        desc

    Methods
    -------
    exit()
        Closes the client, disconnects MongoDB.
    """

    def __init__(self) -> None:
        logger.info('Initializing Client...')
        self.settings = build_settings()
        self.client = get_client(self.settings.mongo_uri)
        # self.houses = IHouses(self.database, self.settings)
        # self.streets = IStreets(self.database, self.settings)
        # self.places = IPlaces(self.database, self.settings)
        # self.internal = IInternal(self.database, self.settings)

    def exit(self):
        """Closes the client, dumps the settings to json-file."""

        self.client.close()
        self.settings.dump()
