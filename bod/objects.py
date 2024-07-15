"""
Objects
-------
Data models for the project.
"""


from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


KeyType = str | int
KeysType = list[KeyType] | set[KeyType]

# Geometry
PointCoords = Annotated[list[float], Field(min_length=2)]
MultiPointCoords = Annotated[list[PointCoords], Field()]
LineStringCoords = Annotated[list[PointCoords], Field(min_length=2)]
MultiLineStringCoords = Annotated[list[LineStringCoords], Field()]
PolygonCoords = Annotated[list[LineStringCoords], Field()]
MultiPolygonCoords = Annotated[list[PolygonCoords], Field()]


class Geometry(BaseModel):
    """Geometry."""

    type: str
    geo_json: dict
    centroid: list[float]


class Translation(BaseModel):
    """Translation."""

    lang: str  # ISO 639 set 1
    value: str


class Constant(BaseModel):
    """Constant."""

    uid: str
    title: str  # unique string
    translations: list[Translation]


class Identifiers(BaseModel):
    """Identifiers."""

    wikipedia: Optional[str]
    wikidata: Optional[str]
    openstreetmaps: Optional[str]
    fias: Optional[str]


class Address(BaseModel):
    """Address"""

    model_config = ConfigDict(extra='ignore')

    comment: str
    # FIAS IDs
    fias_house_id: str
    fias_aux_subobj_id: str
    fias_aux_obj_id: str
    fias_street_id: str
    fias_town_id: str
    fias_district_id: str
    fias_city_id: str
    fias_settlement_id: str
    fias_area_id: str
    fias_unit_id: str
    fias_region_id: str
    fias_country_id: str
    full_address: str
    map_position: Geometry

    # Real address
    country: str
    country_code: str  # RU
    country_code_3: str  # RUS
    ISO3166_2: str  # RU-ULY
    state: str = None
    province: str = None
    locality: str = None
    city: str = None
    district: str = None
    village: str = None
    street: str = None
    house_number: str = None
    house_name: str = None
    flat: str = None
    postcode: str = None


class Image(BaseModel):
    """Description."""

    title: str
    url: str
    description: str
    preview: str


class Link(BaseModel):
    """Description."""

    title: str
    url: str
    description: str


class Person(BaseModel):
    """Description."""
    model_config = ConfigDict(extra='allow')

    uid: int
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    death_date: Optional[date]
    gender: str
    profession: str
    biography: str
    links: list[Link]


class Document(BaseModel):
    """Document."""

    uid: int
    title: str
    description: str
    date: date


class Place(BaseModel):
    """Represents a place like a country, state, province, etc."""
    model_config = ConfigDict(extra='allow')

    uid: int
    name: str
    address: Address
    external_ids: Identifiers
    fias_id: str  # identifier
    country_id: str  # identifier
    region_id: str  # identifier
    city_id: str  # identifier
    district_id: str  # identifier


class Street(BaseModel):
    """Description"""
    model_config = ConfigDict(extra='allow')

    uid: int
    name: str
    address: Address
    geometry: Geometry
    external_ids: Identifiers
    object_type: str  # -> constants 'street types'
    region_id: Place  # identifier
    city_id: Place  # identifier
    district_id: Place  # identifier
    fias_id: str
    # flags
    is_public: bool


class Attraction(BaseModel):
    """Description"""
    model_config = ConfigDict(extra='allow')

    uid: str
    name: str
    type_id: int  # -> constants 'attraction types'
    geometry: Geometry
    description: str
    date: date
    rubrics: list[int]  # -> constants 'attraction rubrics'
    authors: list[Person]
    is_public: bool


class Contacts(BaseModel):
    """Contacts."""

    website: Optional[str]
    email: Optional[str]
    phone: Optional[list[str]]


class WorkingSchedule(BaseModel):
    """WorkingSchedule."""

    monday: dict
    tuesday: dict
    wednesday: dict
    thursday: dict
    friday: dict
    saturday: dict
    sunday: dict


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


class Heritage(BaseModel):
    """Heritage."""

    uid: str
    name: str
    reg_number: str
    address: Address
    region: dict  # id, value -> regions
    con_number: str
    category_type: dict  # id, value -> constants 'category types'
    heritage_type: dict  # id, value -> constants 'heriatge types'
    object_type: dict  # id, value -> constants 'object types'
    security_info: str
    border_info: str
    typologies: list
    status: dict  # id, value -> constants 'statuses'
    unesco: dict  # id, value -> constants 'unesco'
    parent_id: int
    create_date: str
    coords: dict
    documents: list[Document]
    image: Link
    regime_info: str
    id: int
    protection_year: int
    restoration_year: int
    restoration_inf: str
    is_actual: bool
    is_public: bool


class Museum(BaseModel):
    """Museum."""
    model_config = ConfigDict(extra='ignore')

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
    art_type: str
    audience_type: str
    languages: list[str]
    professional_level: str
    virtual_tour: str
    types: list[str]
    identifiers: dict[str, str]
    external_info: list[Link] = Field(alias='externalInfo')


class House(BaseModel):
    """Description"""
    model_config = ConfigDict(extra='allow')

    # IDs
    uid: int
    fias_id: int
    fias_guid: str
    egrkn_id: int
    # Address
    address: Address
    # Civic data
    architects: list[Person] # or identifiers
    styles: list[str]
    type: str
    description: str
    heritages: list[Heritage]  # identifier
    attractions: list[Attraction]  # identifier
    access_type: Constant
    religions: list[Constant]
    # Technical data
    geometry: dict
    level_minimal: int  # I should think about levels
    levels_count: int  # I should think about levels
    levels_underground: int  # I should think about levels
    levels_by_blocks: list[int]  # Number of floors by blocks of the building
    heating_type: Constant # or identifiers
    fire_resistance: Constant # or identifiers
    materials: list[Constant] # or identifiers
    colours: list[Constant] # or identifiers
    construction_date: date
    start_date: date
    end_date: date
    height: float
    condition: Constant
    foundation_height: float
    flat_count: int
    entrance_count: int
    balcony_count: int
    porch_count: int
    lift_count: int
    roof_materials: list[Constant] # or identifiers
    roof_shapes: list[Constant] # or identifiers
    roof_colours: list[Constant] # or identifiers
    links: list[Link]
    tags: list[Constant] # or identifiers
    images: list[Link]
    documents: list[Document] # or identifiers
    project_type: str
    floor_type: str
    external_ids: Identifiers
    # Flags
    is_emergency: bool  # the building needs to be set under control
    is_public: bool  # the building is available for the people
    is_guarded: bool  # the building is inder guard
    is_ruins: bool  # the buidling was destroyed by any influence
    is_abandoned: bool  # the building is abandoned
    is_histroric: bool  # the building is recognized as historical
