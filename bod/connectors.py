"""
bod > `connectors`
==================
Description.
"""

import requests as rq

from bod.settings import Settings


class BasicConnector:
    """Basic subclass for connectors connector."""

    def __init__(self, settings: Settings, timeout: int = None):
        if not timeout:
            timeout = settings.default_timeout
        self.timeout = timeout
        self.headers = {'user-agent': ' '.join(['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)',
                        'AppleWebKit/537.36 (KHTML, like Gecko)',
                        'Chrome/53.0.2785.143 Safari/537.36'])}


class FiasConnector(BasicConnector):
    """
    Connector for Federal Information Address System.

    Parameters
    ----------
    timeout : int, optional
        Timeout in seconds for requests.

    Attributes
    ----------
    api : str
        URL for Ministry of Culture API.
    headers : dict
        Headers for requests.
    """

    def __init__(self, settings: Settings, timeout: int = None):
        super().__init__(settings, timeout)
        self.url = ''


class FrtConnector(BasicConnector):
    """
    Connector for FRT.

    Parameters
    ----------
    timeout : int, optional
        Timeout in seconds for requests.

    Attributes
    ----------
    api : str
        URL for Ministry of Culture API.
    """

    def __init__(self, settings: Settings, timeout: int = None):
        super().__init__(settings, timeout)
        self.api = 'https://аис.фрт.рф/opendata'

    def _get_data(self):
        page = 1
        url = f'{self.api}?page={page}&pageSize=12'


class OsmConnector(BasicConnector):
    """
    Connector for Open Street Maps API.

    Parameters
    ----------
    timeout : int, optional
        Timeout in seconds for requests.

    Attributes
    ----------
    api : str
        URL for Ministry of Culture API.
    """

    def __init__(self, settings: Settings, timeout: int = None) -> None:
        super().__init__(settings, timeout)
        self.url = ''


class MkrfConnector(BasicConnector):
    """
    Connector for Ministry of Culture API.
    
    Parameters
    ----------
    timeout : int, optional
        Timeout in seconds for requests.

    Attributes
    ----------
    api : str
        URL for Ministry of Culture API.
    headers : dict
        Headers for requests.
    """

    def __init__(self, settings: Settings, timeout: int = None):
        super().__init__(settings, timeout)
        self.api = 'https://opendata.mkrf.ru/v2'
        self.headers.update({'X-API-KEY': settings.mkrf.mkrf_key})

    def _get_data(self, url_add: str, path: str, query: str) -> list[dict]:
        url = f'{self.api}/{url_add}/$'
        start = 0
        chunk = 100  # from 1 to 100
        records = []
        while True:
            params = {'f': {path: {'$search': query}},
                      's': start, 'l': chunk}
            with rq.get(url, headers=self.headers, params=params,
                        timeout=self.timeout) as req:
                if req.status_code != 200:
                    break
                data = req.json()
                records.append(data['data'])
            start += chunk
        return records

    def get_museums(self, query: str):
        """Loads museums from Ministry of Culture."""
        return self._get_data('museums', 'data.general.locale.name', query)

    def get_cinemas(self, query: str):
        """Loads cinemas from Ministry of Culture."""
        return self._get_data('cinema', 'data.general.locale.name', query)

    def get_concert_halls(self, query: str):
        """Loads concert halls from Ministry of Culture."""
        return self._get_data('concert_halls', 'data.general.locale.name', query)

    def get_circuses(self, query: str):
        """Loads circuses from Ministry of Culture."""
        return self._get_data('circuses', 'data.general.locale.name', query)

    def get_culture_palaces_clubs(self, query: str):
        """Loads culture palaces and clubs from Ministry of Culture."""
        return self._get_data('culture_palaces_clubs', 'data.general.locale.name', query)

    def get_education(self, query: str):
        """Loads educations from Ministry of Culture."""
        return self._get_data('education', 'data.general.locale.name', query)

    def get_egrkn(self, query: str):
        """Loads culture objects from Ministry of Culture."""
        return self._get_data('egrkn', 'data.general.locale.name', query)

    def get_libraries(self, query: str):
        """Loads libraries from Ministry of Culture."""
        return self._get_data('libraries', 'data.general.locale.name', query)

    def get_organizations(self, query: str):
        """Loads organizations from Ministry of Culture."""
        return self._get_data('organizations', 'data.address', query)

    def get_parks(self, query: str):
        """Loads parks from Ministry of Culture."""
        return self._get_data('parks', 'data.general.locale.name', query)

    def get_philarmonic(self, query: str):
        """Loads philharmonic from Ministry of Culture."""
        return self._get_data('philharmonic', 'data.general.locale.name', query)

    def get_theaters(self, query: str):
        """Loads theaters from Ministry of Culture."""
        return self._get_data('theaters', 'data.general.locale.name', query)
