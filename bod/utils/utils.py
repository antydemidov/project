"""
Utilities for managing the database.
"""

from typing import Optional
from uuid import UUID

import pandas as pd
import requests as rq
import shapely

from bod.logging import get_logger

__all__ = [
    'build_geometry',
    'CountryCodes'
]

logger = get_logger(__name__)

shapely_mapping = {
    'Point': shapely.Point,
    'MultiPoint': shapely.MultiPoint,
    'LineString': shapely.LineString,
    'LinearRing': shapely.LinearRing,
    'MultiLineString': shapely.MultiLineString,
    'Polygon': shapely.Polygon,
    'MultiPolygon': shapely.MultiPolygon
}
geometry_types = list(shapely_mapping.keys())


def build_geometry(obj: dict):
    """Builds a geometry object from a given dictionary."""
    try:
        assert isinstance(obj.get('type', None), str)
        if obj['type'] not in geometry_types:
            geom_type = None
            for item in geometry_types:
                if obj['type'].lower() == item.lower():
                    geom_type = item
            assert geom_type is not None
            obj['type'] = geom_type
        assert obj['type'] in geometry_types
        assert obj.get('coordinates', None) is not None
    except AssertionError as err:
        logger.error(err)
    geo = shapely_mapping[obj['type']](obj['coordinates'])
    centroid = list(list(geo.centroid.coords)[0])
    data = {
        'type': obj['type'],
        'geo_json': obj,
        'centroid': centroid
    }
    return data


class CountryCodes:
    """ISO-3166-1"""

    def __init__(self) -> None:
        path = 'source/iso-3166-country-codes.csv'
        columns = ['alpha_2', 'alpha_3', 'short_name_en']
        self.data = pd.read_csv(path, encoding='utf-8')[columns]

    def get(self, column: str, value: str):
        """
        Returns a dictionary by given column and value:
        - `alpha_2`: ISO 3166-1 alpha-2 code of country;
        - `alpha_3`: ISO 3166-1 alpha-2 code of country;
        - `short_name_en`: short name of country.
        """
        fltr = self.data[column] == value
        return self.data[fltr].to_dict('records')[0]

    def get_by_alpha_2(self, alpha_2: str):
        """
        Returns a dictionary by given alpha_2 code:
        - `alpha_2`: ISO 3166-1 alpha-2 code of country;
        - `alpha_3`: ISO 3166-1 alpha-2 code of country;
        - `short_name_en`: short name of country.
        """
        return self.get('alpha_2', alpha_2)

    def get_by_alpha_3(self, alpha_3: str):
        """
        Returns a dictionary by given alpha_3 code:
        - `alpha_2`: ISO 3166-1 alpha-2 code of country;
        - `alpha_3`: ISO 3166-1 alpha-2 code of country;
        - `short_name_en`: short name of country.
        """
        return self.get('alpha_3', alpha_3)


class LanguageCodes:
    """Description."""

    def __init__(self) -> None:
        path = 'source/iso-639-language-codes.csv'
        url = 'https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt'
        with rq.get(url, timeout=10) as req:
            with open(path, 'wb') as f:
                f.write(req.content)

        df = pd.read_csv(path, sep='|', header=None)
        df.columns = ['alpha_3', 'alpha_3_term',
                      'alpha_2', 'name', 'french_name']
        df = df.drop(['alpha_3_term', 'french_name'], axis=1)
        self.data = df
        df.to_csv(path, index=False)

    def get(self, column: str, value: str):
        """
        Returns a dictionary by given column and value:
        - `alpha_2`: ISO 639 alpha-2 code of language;
        - `alpha_3`: ISO 639 alpha-3 code of language;
        - `name`: short name of language in English.
        """
        fltr = self.data[column] == value
        return self.data[fltr].to_dict('records')[0]

    def get_by_alpha_2(self, alpha_2: str):
        """
        Returns a dictionary by given alpha_2:
        - `alpha_2`: ISO 639 alpha-2 code of language;
        - `alpha_3`: ISO 639 alpha-3 code of language;
        - `name`: short name of language in English.
        """
        return self.get('alpha_2', alpha_2)

    def get_by_alpha_3(self, alpha_3: str):
        """
        Returns a dictionary by given alpha_3:
        - `alpha_2`: ISO 639 alpha-2 code of language;
        - `alpha_3`: ISO 639 alpha-3 code of language;
        - `name`: short name of language in English.
        """
        return self.get('alpha_3', alpha_3)

    def get_by_name(self, name: str):
        """
        Returns a dictionary by given name:
        - `alpha_2`: ISO 639 alpha-2 code of language;
        - `alpha_3`: ISO 639 alpha-3 code of language;
        - `name`: short name of language in English.
        """
        return self.get('name', name)


# sorts dicts by keys
def sort_dict(unsorted_dict: dict) -> dict:
    """
    Sort dicts by keys in ascending order.

    Parameters
    ----------
    unsorted_dict : dict
        description.

    Returns
    -------
    dict
    """

    sorted_dict = {}
    for key in sorted(list(unsorted_dict.keys())):
        value = unsorted_dict[key]
        if isinstance(unsorted_dict[key], dict):
            value = sort_dict(value)
        sorted_dict.update({key: value})
    return sorted_dict
