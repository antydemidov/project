"""
Heritage
--------
Description.
"""

from bod.objects import Heritage


def get_heritage(data: dict) -> Heritage:
    """Builds and returns a Heritage object."""

    address = data['address']

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

    return Heritage(
        d
    )
