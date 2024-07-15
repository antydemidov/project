"""Objects for MKRF."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Address(BaseModel):
    """Address"""
    model_config = ConfigDict(extra='ignore')

    comment: str
    # FIAS IDs
    fias_house_id: str = Field(alias='fiasHouseId')
    fias_aux_subobj_id: str = Field(alias='fiasAuxSubobjId')
    fias_aux_obj_id: str = Field(alias='fiasAuxObjId')
    fias_street_id: str = Field(alias='fiasStreetId')
    fias_town_id: str = Field(alias='fiasTownId')
    fias_district_id: str = Field(alias='fiasDistrictId')
    fias_city_id: str = Field(alias='fiasCityId')
    fias_settlement_id: str = Field(alias='fiasSettlementId')
    fias_area_id: str = Field(alias='fiasAreaId')
    fias_unit_id: str = Field(alias='fiasUnitId')
    fias_region_id: str = Field(alias='fiasRegionId')
    fias_country_id: str = Field(alias='fiasCountryId')
    full_address: str = Field(alias='fullAddress')
    map_position: dict = Field(alias='mapPosition')


class Document(BaseModel):
    """Document."""

    uid: int
    title: str
    description: str
    date: date


class Link(BaseModel):
    """Description."""

    title: str
    url: str
    description: str


class Contacts(BaseModel):
    """Contacts."""

    website: Optional[str]
    email: Optional[str]
    phone: Optional[list[str]]


class WorkingSchedule(BaseModel):
    """WorkingSchedule."""

    monday: dict = None
    tuesday: dict = None
    wednesday: dict = None
    thursday: dict = None
    friday: dict = None
    saturday: dict = None
    sunday: dict = None


class SocialGroup(BaseModel):
    """SocialGroup."""

    name: str
    network: str
    network_id: Optional[str] = Field(alias='networkId')
    posting_group_id: Optional[int] = Field(alias='postingGroupId')
    account_id: int = Field(alias='accountId')
    is_personal: bool = Field(default=False, alias='isPersonal')


class Organization(BaseModel):
    """Organization."""

    title: str
    address: Address
    tin: str  # tax identification number
    type: str
    social_groups: list[SocialGroup] = Field(alias='socialGroups')
    identifiers: dict[str, str] # ЕИПСК id


class Museum(BaseModel):
    """Museum."""

    uid: str
    name: str
    address: Address
    description: str
    contacts: Contacts
    image: Link
    gallery: list[Link]
    category: str
    organization: Organization
    tags: list[str]
    working_schedule: WorkingSchedule = Field(alias='workingSchedule')
    art_type: str = Field(alias='artType')
    audience_type: str = Field(alias='audienceType')
    languages: list[str]
    professional_level: str = Field(alias='professionalLevel')
    virtual_tour: str = Field(alias='virtualTour')
    types: list[str]
    identifiers: dict[str, str]
    external_info: list[Link] = Field(alias='externalInfo')


class Heritage(BaseModel):
    """Heritage."""

    uid: str
    name: str
    reg_number: str = Field(alias='regNumber')
    address: Address
    region: dict  # id, value -> regions
    con_number: str = Field(alias='conNumber')
    category_type: dict = Field(alias='categoryType')  # id, value -> constants 'category types'
    heritage_type: dict = Field(alias='heritageType')  # id, value -> constants 'heriatge types'
    object_type: dict = Field(alias='objectType')  # id, value -> constants 'object types'
    security_info: str = Field(alias='securityInfo')
    border_info: str = Field(alias='borderInfo')
    typologies: list
    status: dict  # id, value -> constants 'statuses'
    unesco: dict  # id, value -> constants 'unesco'
    parent_id: int = Field(alias='parentId')
    create_date: str = Field(alias='createDate')
    coords: dict
    documents: list[Document]
    image: Link
    regime_info: str = Field(alias='regimeInfo')
    id: int
    protection_year: int = Field(alias='protectionYear')
    restoration_year: int = Field(alias='restorationYear')
    restoration_inf: str = Field(alias='restorationInf')
    is_actual: bool = Field(alias='isActual')
    is_public: bool = Field(alias='isPublic')
