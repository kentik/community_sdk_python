from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from kentik_api.public.types import ID
from kentik_api.public.custom_dimension import Populator
from kentik_api.requests_payload.conversions import convert, from_dict, dict_from_json


# pylint: disable=too-many-instance-attributes


@dataclass
class _Populator:
    id: int
    dimension_id: int
    company_id: str
    value: str
    direction: str
    user: str
    mac_count: int
    addr_count: int
    created_date: str
    updated_date: str

    device_name: Optional[str] = None
    interface_name: Optional[str] = None
    addr: Optional[str] = None
    port: Optional[str] = None
    tcp_flags: Optional[str] = None
    protocol: Optional[str] = None
    asn: Optional[str] = None
    nexthop_asn: Optional[str] = None
    nexthop: Optional[str] = None
    bgp_aspath: Optional[str] = None
    bgp_community: Optional[str] = None
    device_type: Optional[str] = None
    site: Optional[str] = None
    lasthop_as_name: Optional[str] = None
    nexthop_as_name: Optional[str] = None
    mac: Optional[str] = None
    country: Optional[str] = None
    vlans: Optional[str] = None

    def to_populator(self) -> Populator:
        return Populator(
            dimension_id=convert(self.dimension_id, ID),
            value=self.value,
            direction=convert(self.direction.upper(), Populator.Direction),
            device_name=self.device_name,
            interface_name=self.interface_name,
            addr=self.addr,
            port=self.port,
            tcp_flags=self.tcp_flags,
            protocol=self.protocol,
            asn=self.asn,
            nexthop_asn=self.nexthop_asn,
            nexthop=self.nexthop,
            bgp_aspath=self.bgp_aspath,
            bgp_community=self.bgp_community,
            device_type=self.device_type,
            site=self.site,
            lasthop_as_name=self.lasthop_as_name,
            nexthop_as_name=self.nexthop_as_name,
            mac=self.mac,
            country=self.country,
            vlans=self.vlans,
            id=convert(self.id, ID),
            company_id=convert(self.company_id, ID),
            user=self.user,
            mac_count=self.mac_count,
            addr_count=self.addr_count,
            created_date=self.created_date,
            updated_date=self.updated_date,
        )


# pylint: enable=too-many-instance-attributes


class PopulatorArray(List[_Populator]):
    @classmethod
    def from_list(cls, items: List[Dict[str, Any]]):
        populators = cls()
        for item in items:
            p = from_dict(data_class=GetResponse, data=item)
            populators.append(p)
        return populators

    def to_populators(self) -> List[Populator]:
        return [p.to_populator() for p in self]


class GetResponse(_Populator):
    @classmethod
    def from_json(cls, json_string: str):
        # payload is embeded under "populator" key
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string, root="populator")
        return from_dict(data_class=cls, data=dic)


class CreateRequest:
    # pylint: disable=too-many-instance-attributes
    @dataclass
    class _Populator:
        # dimension_id: int # this id goes as url param
        value: str
        direction: str
        device_name: Optional[str]
        interface_name: Optional[str]
        addr: Optional[str]
        port: Optional[str]
        tcp_flags: Optional[str]
        protocol: Optional[str]
        asn: Optional[str]
        nexthop_asn: Optional[str]
        nexthop: Optional[str]
        bgp_aspath: Optional[str]
        bgp_community: Optional[str]
        device_type: Optional[str]
        site: Optional[str]
        lasthop_as_name: Optional[str]
        nexthop_as_name: Optional[str]
        mac: Optional[str]
        country: Optional[str]
        vlans: Optional[str]

    # pylint: enable=too-many-instance-attributes

    def __init__(self, **kwargs) -> None:
        self.populator = from_dict(data_class=CreateRequest._Populator, data=kwargs)


CreateResponse = GetResponse


@dataclass
class UpdateRequest:
    # pylint: disable=too-many-instance-attributes
    @dataclass
    class _Populator:
        # id: int # this id goes as url param
        # dimension_id: int # this id goes as url param
        value: str
        direction: str
        device_name: Optional[str]
        interface_name: Optional[str]
        addr: Optional[str]
        port: Optional[str]
        tcp_flags: Optional[str]
        protocol: Optional[str]
        asn: Optional[str]
        nexthop_asn: Optional[str]
        nexthop: Optional[str]
        bgp_aspath: Optional[str]
        bgp_community: Optional[str]
        device_type: Optional[str]
        site: Optional[str]
        lasthop_as_name: Optional[str]
        nexthop_as_name: Optional[str]
        mac: Optional[str]
        country: Optional[str]
        vlans: Optional[str]

    # pylint: enable=too-many-instance-attributes

    def __init__(self, **kwargs) -> None:
        self.populator = from_dict(data_class=UpdateRequest._Populator, data=kwargs)


UpdateResponse = GetResponse


# @dataclass()
# class DeleteResponse:
#     """ Currently custom dimension delete response carries no body data just http code 204 for succcess """
