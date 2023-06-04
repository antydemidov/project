"""
The module is responsible for creating the schema for the databases.
"""

import datetime
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from .results import CommonResult

try:
    from .bod_api import Client
except ImportError:
    pass


@dataclass
class FieldSchema:
    """
    Minimal class containing name, string, type, required of the field of
    collections' records.
    
    Attributes
    ----------
    -   `name` : The name of the field
    -   `string` : The string describing the field
    -   `type` : The type of the field
    -   `required` : The bool indicating whether the field should be required
    """
    name: str
    string: str
    type: str
    required: bool


@dataclass
class CollectionSchema:
    """
    Minimal class containing name, string, element_name, element_string and the
    list of FieldSchema objects.

    Attributes
    ----------
    -   `name` : The name of the collection
    -   `string` : The string describing the collection
    -   `element_name` : The name of the element
    -   `element_string` : The description of the element
    -   `fields` : The list of FieldSchema objects
    """

    name: str
    string: str
    element_name: str
    element_string: str
    fields: list[FieldSchema]

    def find_field(self, name) -> FieldSchema:
        """Search for a field in the schema by its name."""

        for field in self.fields:
            if getattr(field, name) == name:
                return field
        return None


class Schema:
    """The `Schema` class represents a schema of the database."""

    def __init__(self, client: "Client") -> None:
        self.client = client
        self.database = client.get_database(client.settings.actual_db_desc)
        source: list[dict] = list(self.database.get_collection('Schema').mongo.find({}))
        self.list_collections = self.database.list_collections
        _map = {'Int32': int,
                'string': str,
                'datetime64': datetime.datetime}

        for item in source:
            name = item['name']
            string = item['string']
            element_name = item['element_name']
            element_string = item['element_string']
            fields: list[dict] = item['fields']
            fields_cl = []
            for field in fields:
                field_cl = FieldSchema(name=field.get('name'),
                                       string=field.get('string'),
                                       type=_map.get(field.get('type')),
                                       required=field.get('required'))
                fields_cl.append(field_cl)
            coll_schema = CollectionSchema(name=name,
                                           string=string,
                                           element_name=element_name,
                                           element_string=element_string,
                                           fields=fields_cl)
            setattr(self, name, coll_schema)

    def find_coll(self, name: str) -> CollectionSchema:
        """Resieves a name of a collection and returns a `CollectionSchema`."""

        try:
            if name in self.list_collections:
                coll_schema = getattr(self, name)
            else:
                coll_schema = getattr(self, 'housetypes')
        except AttributeError:
            coll_schema = None
        return coll_schema

    @staticmethod
    def _get_coll_schema_from_file(file_name: str):
        """Returns the collection schema by XSD-file name"""

        if not os.path.exists(file_name):
            raise ValueError(file_name, 'Invalid value, must be a string')
        _map = {'xs:long': 'Int32',
                'xs:string': 'string',
                'xs:integer': 'Int32',
                'xs:date': 'datetime64',
                'xs:boolean': 'string'}
        coll_schema = []
        coll_name = ''.join([s.lower() for s in file_name.split('_')[1:-1] if not s.isdigit()])
        root = ET.parse(file_name).getroot()
        namespaces = {'xs': root.tag.split('}')[0][1:]}

        docs = root.findall('.//xs:documentation', namespaces)
        coll_string = docs[0].text
        element_string = docs[1].text
        elements = root.findall('.//xs:element', namespaces)
        element_name = elements[1].attrib.get('name') or elements[1].attrib.get('ref')
        attrs = root.findall('.//xs:attribute', namespaces)

        for attr in attrs:
            if attr is not None:
                if attr.find('.//xs:restriction', namespaces) is not None:
                    restriction = attr.find('.//xs:restriction', namespaces).attrib.get('base')
                else: restriction = None
                type_source = attr.attrib.get('type') or restriction
                if type_source is None:
                    _type = 'string'
                else: _type = _map[type_source]
                field = FieldSchema(
                    name=attr.attrib.get('name'),
                    type=_type,
                    required=(attr.attrib.get('use') == 'required'),
                    string=attr.find('.//xs:documentation', namespaces).text)
                coll_schema.append(field)

        return CollectionSchema(name=coll_name,
                                string=coll_string,
                                element_name=element_name,
                                element_string=element_string,
                                fields=coll_schema)

    def update_schema(self, to_db: bool = True):
        """
        Updates schema.

        Parameters
        ----------
        -   to_db: `bool` - Load schema to db or don't load.
        """
        if os.path.exists(self.client.settings.path_schema):
            list_schema_files_source = os.listdir(self.client.settings.path_schema)
            list_schema_files = [os.path.join(
                self.client.settings.path_schema, file) for file in list_schema_files_source]
        else:
            raise FileNotFoundError
        schema = []
        updated_collections = []
        details = {}

        for file in list_schema_files:
            coll_schema = self._get_coll_schema_from_file(file)
            details.update({coll_schema.name: coll_schema})
            updated_collections.append(coll_schema.name)
            schema.append(dict(coll_schema))

        if to_db:
            self.database.get_collection('Schema').delete_many({})
            self.database.get_collection('Schema').insert_many(schema)

        return CommonResult(status='Schema of BoD was updated',
                            details=details,
                            updated_collections=updated_collections,
                            source = schema)
