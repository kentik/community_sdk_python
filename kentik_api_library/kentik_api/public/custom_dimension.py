from enum import Enum
from typing import List, Optional

from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.types import ID, PermissiveEnumMeta

# pylint: disable=too-many-instance-attributes


class Populator:
    class Direction(Enum, metaclass=PermissiveEnumMeta):
        SRC = "SRC"
        DST = "DST"
        EITHER = "EITHER"

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        value: str,
        direction: Direction,
        device_name: Optional[str] = None,
        interface_name: Optional[str] = None,
        addr: Optional[str] = None,
        port: Optional[str] = None,
        tcp_flags: Optional[str] = None,
        protocol: Optional[str] = None,
        asn: Optional[str] = None,
        nexthop_asn: Optional[str] = None,
        nexthop: Optional[str] = None,
        bgp_aspath: Optional[str] = None,
        bgp_community: Optional[str] = None,
        device_type: Optional[str] = None,
        site: Optional[str] = None,
        lasthop_as_name: Optional[str] = None,
        nexthop_as_name: Optional[str] = None,
        mac: Optional[str] = None,
        country: Optional[str] = None,
        vlans: Optional[str] = None,
        id: Optional[ID] = None,
        company_id: Optional[ID] = None,
        user: Optional[str] = None,
        dimension_id: Optional[ID] = None,
        mac_count: Optional[int] = None,
        addr_count: Optional[int] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
    ) -> None:
        # read-write
        self.value = value
        self.direction = direction
        self.device_name = device_name
        self.interface_name = interface_name
        self.addr = addr
        self.port = port
        self.tcp_flags = tcp_flags
        self.protocol = protocol
        self.asn = asn
        self.nexthop_asn = nexthop_asn
        self.nexthop = nexthop
        self.bgp_aspath = bgp_aspath
        self.bgp_community = bgp_community
        self.device_type = device_type
        self.site = site
        self.lasthop_as_name = lasthop_as_name
        self.nexthop_as_name = nexthop_as_name
        self.mac = mac
        self.country = country
        self.vlans = vlans

        # read-only
        self._id = id
        self._company_id = company_id
        self._dimension_id = dimension_id
        self._user = user
        self._mac_count = mac_count
        self._addr_count = addr_count
        self._created_date = created_date
        self._updated_date = updated_date

    # pylint: enable=too-many-arguments

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_id is required")
        return self._id

    @property
    def company_id(self) -> Optional[ID]:
        return self._company_id

    @property
    def dimension_id(self) -> ID:
        if self._dimension_id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_dimension_id is required")
        return self._dimension_id

    @property
    def user(self) -> Optional[str]:
        return self._user

    @property
    def mac_count(self) -> Optional[int]:
        return self._mac_count

    @property
    def addr_count(self) -> Optional[int]:
        return self._addr_count

    @property
    def created_date(self) -> Optional[str]:
        return self._created_date

    @property
    def updated_date(self) -> Optional[str]:
        return self._updated_date


# pylint: enable=too-many-instance-attributes


class CustomDimension:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name: Optional[str] = None,
        display_name: Optional[str] = None,
        type: Optional[str] = None,
        populators: Optional[List[Populator]] = None,
        id: Optional[ID] = None,
        company_id: Optional[ID] = None,
    ) -> None:
        # read-write
        # name must start with c_ and be unique even against deleted dimensions
        # (deleted names are retained for 1 year)
        self.name = name
        self.display_name = display_name
        self.type = type
        self.populators = populators

        # read-only
        self._id = id
        self._company_id = company_id

    # pylint: enable=too-many-arguments

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_id is required")
        return self._id

    @property
    def company_id(self) -> Optional[ID]:
        return self._company_id
