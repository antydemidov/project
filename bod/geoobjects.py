"""
bod > geoobjects
================
The module for spacial objects.
"""

from shapely import (LinearRing, LineString, MultiLineString, MultiPoint,
                     MultiPolygon, Point, Polygon)


_geoobject_type = Point | LineString | LinearRing | Polygon | MultiLineString | MultiPoint | MultiPolygon


class Geoobject:
    ru_class_name = "Геообъект"

    def __init__(self, object: _geoobject_type):
        self.geom_type = object.geom_type
        self.coords = object.coords
        self.object = object


class BaseObject:
    """Базовый объект, использующийся для определения общих методов"""
    ru_class_name = "Базовый объект"

    def __init__(self, id: int, name: str, geo: Geoobject):
        self.id = id
        self.name = name
        self.geo = geo


class District(BaseObject):
    ru_class_name = "Район"

    def __init__(self, id: int, name: str, geo: Geoobject, parent_id: int, childs: list):
        super().__init__(id, name, geo)
        self.parent_id = parent_id
        self.childs = childs


class Street(BaseObject):
    ru_class_name = "Улица"

    def __init__(self, id: int, name: str, geo: Geoobject, parent_id: int, childs: list):
        super().__init__(id, name, geo)
        self.parent_id = parent_id
        self.childs = childs


class House(BaseObject):
    ru_class_name = "Дом"

    def __init__(self, id: int, name: str, geo: Geoobject, parent_id: int, number, zip, full_address, year: int, architector: str, style: str, **kwargs):
        super().__init__(id, name, geo)
        self.parent_id = parent_id
        self.number = number
        self.zip = zip
        self.full_address = full_address
        # culture
        self.year = year
        self.architector = architector
        self.style = style
        for kwarg_name, kwarg_value in kwargs:
            self.__setattr__(kwarg_name, kwarg_value)
        self.data = self.__dict__
