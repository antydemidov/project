"""
Schema
------
Description.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    'Addrobj',
    'Addrobjdivision',
    'Admhierarchy',
    'Apartments',
    'Carplaces',
    'Changehistory',
    'Houses',
    'Hierarchy',
    'Munhierarchy',
    'Normativedocs',
    'Normativedocskinds',
    'Objectlevels',
    'Params',
    'Reestrobjects',
    'Rooms',
    'Steads',
    'Params',
    'Types',
    'Objects',
    # FIAS Objects
    'FiasObject',
    'FiasParam',
    'FiasParams'
]


class FiasParams(BaseModel):
    ifnsfl: Optional[str] = None
    ifnsul: Optional[str] = None
    territorial_ifnsfl_code: Optional[str] = None
    territorial_ifnsul_code: Optional[str] = None
    post_index: Optional[str] = None
    okato: Optional[str] = None
    oktmo: Optional[str] = None
    cadastr_num: Optional[str] = None
    code: Optional[str] = None
    plain_code: Optional[str] = None
    region_code: Optional[str] = None
    reestr_num: Optional[str] = None
    division_type: Optional[str] = None
    counter: Optional[str] = None
    official: Optional[str] = None
    post_status: Optional[str] = None


class FiasParam(BaseModel):
    type_id: int
    value: str


class FiasObject(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    object_id: Optional[int]
    object_guid: Optional[str]
    level_id: Optional[int]  # ref to Level
    title: Optional[str]  # name or number
    type_id: Optional[int]  # ref to Type
    params: Optional[list[FiasParam]]
    parent_obj_id: Optional[int]  # ref to self
    parent_obj_id_adm: Optional[int]
    parent_obj_id_mun: Optional[int]
    path: Optional[str]
    path_adm: Optional[int]
    path_mun: Optional[int]


class Params(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    change_id: int = Field(alias='CHANGEID')
    change_id_end: int = Field(alias='CHANGEIDEND')
    type_id: int = Field(alias='TYPEID')
    value: str = Field(alias='VALUE')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')


class Types(BaseModel):
    id: int = Field(alias='ID')
    name: str = Field(alias='NAME')
    short_name: str = Field(alias='SHORTNAME', default=None)
    desc: str = Field(alias='DESC', default=None)
    is_active: bool = Field(alias='ISACTIVE', default=None)
    start_date: datetime = Field(alias='STARTDATE', default=None)
    end_date: datetime = Field(alias='ENDDATE', default=None)
    update_date: datetime = Field(alias='UPDATEDATE', default=None)


class Objects(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    object_guid: str = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')

    oper_type_id: int = Field(alias='OPERTYPEID')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_actual: bool = Field(alias='ISACTUAL')
    is_active: bool = Field(alias='ISACTIVE')

    # number: int = Field(alias='NUMBER', default=None)
    # type_id: int = Field(alias='HOUSENUM', default=None)

    # Addrobj
    name: str = Field(alias='NAME', default=None)
    type_name: str = Field(alias='TYPENAME', default=None)
    level_id: int = Field(alias='LEVEL', default=None)
    # Houses
    house_num: int = Field(alias='HOUSENUM', default=None)
    house_type: int = Field(alias='HOUSETYPE', default=None)
    # Apartments
    apart_type: int = Field(alias='APARTTYPE', default=None)
    # Rooms
    room_type: int = Field(alias='ROOMTYPE', default=None)
    # Steads or Rooms or Apartments or Carplaces
    number: int = Field(alias='NUMBER', default=None)


class Addrobj(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    object_guid: str = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')
    name: str = Field(alias='NAME')
    type_name: str = Field(alias='TYPENAME')
    level_id: int = Field(alias='LEVEL')
    oper_type_id: int = Field(alias='OPERTYPEID')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_actual: bool = Field(alias='ISACTUAL')
    is_active: bool = Field(alias='ISACTIVE')


class Addrobjdivision(BaseModel):
    id: int = Field(alias='ID')
    parent_id: int = Field(alias='PARENTID')
    child_id: int = Field(alias='CHILDID')
    change_id: int = Field(alias='CHANGEID')


class Admhierarchy(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    parent_obj_id: int = Field(alias='PARENTOBJID')
    change_id: int = Field(alias='CHANGEID')
    region_code: int = Field(alias='REGIONCODE')
    area_code: int = Field(alias='AREACODE')
    city_code: int = Field(alias='CITYCODE')
    place_code: int = Field(alias='PLACECODE')
    street_code: int = Field(alias='STREETCODE')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_active: bool = Field(alias='ISACTIVE')
    path: str = Field(alias='PATH')


class Apartments(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    object_guid: int = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')
    number: int = Field(alias='NUMBER')
    # apart_type: int = Field(alias='APARTTYPE')
    type_id: int = Field(alias='APARTTYPE')
    oper_type_id: int = Field(alias='OPERTYPEID')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_actual: bool = Field(alias='ISACTUAL')
    is_active: bool = Field(alias='ISACTIVE')


class Carplaces(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    object_guid: int = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')
    number: int = Field(alias='NUMBER')
    oper_type_id: int = Field(alias='OPERTYPEID')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_actual: bool = Field(alias='ISACTUAL')
    is_active: bool = Field(alias='ISACTIVE')


class Changehistory(BaseModel):
    change_id: int = Field(alias='CHANGEID')
    object_id: int = Field(alias='OBJECTID')
    adr_object_id: int = Field(alias='ADROBJECTID')
    oper_type_id: int = Field(alias='OPERTYPEID')
    ndocid: int = Field(alias='NDOCID')
    change_date: datetime = Field(alias='CHANGEDATE')


class Houses(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    object_guid: int = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')
    # house_num: int = Field(alias='HOUSENUM')
    number: int = Field(alias='HOUSENUM')
    # house_type: int = Field(alias='HOUSETYPE')
    type_id: int = Field(alias='HOUSETYPE')
    oper_type_id: int = Field(alias='OPERTYPEID')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_actual: bool = Field(alias='ISACTUAL')
    is_active: bool = Field(alias='ISACTIVE')


class Hierarchy(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    parent_obj_id: int = Field(alias='PARENTOBJID')
    is_active: bool = Field(alias='ISACTIVE')
    path: str = Field(alias='PATH')


class Munhierarchy(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    parent_obj_id: int = Field(alias='PARENTOBJID')
    change_id: int = Field(alias='CHANGEID')
    oktmo: int = Field(alias='OKTMO')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_active: bool = Field(alias='ISACTIVE')
    path: str = Field(alias='PATH')


class Normativedocs(BaseModel):
    id: int = Field(alias='ID')
    name: str = Field(alias='NAME')
    date: datetime = Field(alias='DATE')
    number: str = Field(alias='NUMBER')
    type: int = Field(alias='TYPE')
    kind: int = Field(alias='KIND')
    update_date: datetime = Field(alias='UPDATEDATE')
    org_name: str = Field(alias='ORGNAME')
    acc_date: datetime = Field(alias='ACCDATE')


class Normativedocskinds(BaseModel):
    id: int = Field(alias='ID')
    name: str = Field(alias='NAME')


class Objectlevels(BaseModel):
    id: int = Field(alias='LEVEL')
    name: str = Field(alias='NAME')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_active: bool = Field(alias='ISACTIVE')


class Reestrobjects(BaseModel):
    model_config = ConfigDict(extra='ignore')

    object_id: int = Field(alias='OBJECTID')
    object_guid: str = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')
    level_id: int = Field(alias='LEVELID')
    create_date: datetime = Field(alias='CREATEDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_active: bool = Field(alias='ISACTIVE')


class Rooms(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    object_guid: int = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')
    number: int = Field(alias='NUMBER')
    # room_type: int = Field(alias='ROOMTYPE')
    type_id: int = Field(alias='ROOMTYPE')
    oper_type_id: int = Field(alias='OPERTYPEID')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_actual: bool = Field(alias='ISACTUAL')
    is_active: bool = Field(alias='ISACTIVE')


class Steads(BaseModel):
    id: int = Field(alias='ID')
    object_id: int = Field(alias='OBJECTID')
    object_guid: int = Field(alias='OBJECTGUID')
    change_id: int = Field(alias='CHANGEID')
    number: int = Field(alias='NUMBER')
    oper_type_id: int = Field(alias='OPERTYPEID')
    prev_id: int = Field(alias='PREVID')
    next_id: int = Field(alias='NEXTID')
    start_date: datetime = Field(alias='STARTDATE')
    end_date: datetime = Field(alias='ENDDATE')
    update_date: datetime = Field(alias='UPDATEDATE')
    is_actual: bool = Field(alias='ISACTUAL')
    is_active: bool = Field(alias='ISACTIVE')


# class Addhousetypes(BaseModel):
#     id: int = Field(alias='ID')
#     name: str = Field(alias='NAME')
#     short_name: str = Field(alias='SHORTNAME')
#     desc: str = Field(alias='DESC')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')
#     is_active: bool = Field(alias='ISACTIVE')


# class Addrobjparams(BaseModel):
#     id: int = Field(alias='ID')
#     object_id: int = Field(alias='OBJECTID')
#     change_id: int = Field(alias='CHANGEID')
#     change_id_end: int = Field(alias='CHANGEIDEND')
#     type_id: int = Field(alias='TYPEID')
#     value: str = Field(alias='VALUE')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')


# class Addrobjtypes(BaseModel):
#     id: int = Field(alias='ID')
#     level: int = Field(alias='LEVEL')
#     name: str = Field(alias='NAME')
#     short_name: str = Field(alias='SHORTNAME')
#     desc: str = Field(alias='DESC')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')
#     is_active: bool = Field(alias='ISACTIVE')


# class Apartmentsparams(BaseModel):
#     id: int = Field(alias='ID')
#     object_id: int = Field(alias='OBJECTID')
#     change_id: int = Field(alias='CHANGEID')
#     change_id_end: int = Field(alias='CHANGEIDEND')
#     typeid: int = Field(alias='TYPEID')
#     value: int = Field(alias='VALUE')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')


# class Apartmenttypes(BaseModel):
#     id: int = Field(alias='ID')
#     name: str = Field(alias='NAME')
#     short_name: str = Field(alias='SHORTNAME')
#     desc: str = Field(alias='DESC')
#     startdate: datetime = Field(alias='STARTDATE')
#     enddate: datetime = Field(alias='ENDDATE')
#     updatedate: datetime = Field(alias='UPDATEDATE')
#     is_active: bool = Field(alias='ISACTIVE')


# class Carplacesparams(BaseModel):
#     id: int = Field(alias='ID')
#     object_id: int = Field(alias='OBJECTID')
#     change_id: int = Field(alias='CHANGEID')
#     change_id_end: int = Field(alias='CHANGEIDEND')
#     typeid: int = Field(alias='TYPEID')
#     value: int = Field(alias='VALUE')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')


# class Housesparams(BaseModel):
#     id: int = Field(alias='ID')
#     object_id: int = Field(alias='OBJECTID')
#     change_id: int = Field(alias='CHANGEID')
#     change_id_end: int = Field(alias='CHANGEIDEND')
#     typeid: int = Field(alias='TYPEID')
#     value: int = Field(alias='VALUE')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')


# class Housetypes(BaseModel):
#     id: int = Field(alias='ID')
#     name: str = Field(alias='NAME')
#     short_name: str = Field(alias='SHORTNAME')
#     desc: str = Field(alias='DESC')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')
#     is_active: bool = Field(alias='ISACTIVE')


# class Normativedocstypes(BaseModel):
#     id: int = Field(alias='ID')
#     name: str = Field(alias='NAME')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')


# class Operationtypes(BaseModel):
#     id: int = Field(alias='ID')
#     name: str = Field(alias='NAME')
#     startdate: datetime = Field(alias='STARTDATE')
#     enddate: datetime = Field(alias='ENDDATE')
#     updatedate: datetime = Field(alias='UPDATEDATE')
#     is_active: bool = Field(alias='ISACTIVE')


# class Paramtypes(BaseModel):
#     id: int = Field(alias='ID')
#     name: str = Field(alias='NAME')
#     desc: str = Field(alias='DESC')
#     code: str = Field(alias='CODE')
#     startdate: datetime = Field(alias='STARTDATE')
#     enddate: datetime = Field(alias='ENDDATE')
#     updatedate: datetime = Field(alias='UPDATEDATE')
#     is_active: bool = Field(alias='ISACTIVE')


# class Roomsparams(BaseModel):
#     id: int = Field(alias='ID')
#     object_id: int = Field(alias='OBJECTID')
#     change_id: int = Field(alias='CHANGEID')
#     change_id_end: int = Field(alias='CHANGEIDEND')
#     typeid: int = Field(alias='TYPEID')
#     value: int = Field(alias='VALUE')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')


# class Roomtypes(BaseModel):
#     id: int = Field(alias='ID')
#     name: str = Field(alias='NAME')
#     desc: str = Field(alias='DESC')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')
#     is_active: bool = Field(alias='ISACTIVE')


# class Steadsparams(BaseModel):
#     id: int = Field(alias='ID')
#     object_id: int = Field(alias='OBJECTID')
#     change_id: int = Field(alias='CHANGEID')
#     change_id_end: int = Field(alias='CHANGEIDEND')
#     type_id: int = Field(alias='TYPEID')
#     value: str = Field(alias='VALUE')
#     start_date: datetime = Field(alias='STARTDATE')
#     end_date: datetime = Field(alias='ENDDATE')
#     update_date: datetime = Field(alias='UPDATEDATE')
