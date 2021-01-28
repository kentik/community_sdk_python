import json
from typing import Optional, List
from dataclasses import dataclass

from kentik_api.requests_payload.conversions import convert
from kentik_api.public.types import ID
from kentik_api.public.tag import Tag

# pylint: disable=too-many-instance-attributes


@dataclass
class _RequestTag:
    flow_tag: Optional[str] = None
    device_name: Optional[str] = None
    interface_name: Optional[str] = None
    addr: Optional[str] = None
    port: Optional[str] = None
    tcp_flags: Optional[str] = None
    protocol: Optional[str] = None
    asn: Optional[str] = None
    nexthop: Optional[str] = None
    nexthop_asn: Optional[str] = None
    bgp_aspath: Optional[str] = None
    bgp_community: Optional[str] = None
    device_type: Optional[str] = None
    site: Optional[str] = None
    lasthop_as_name: Optional[str] = None
    nexthop_as_name: Optional[str] = None
    mac: Optional[str] = None
    country: Optional[str] = None
    vlans: Optional[str] = None


# pylint: enable=too-many-instance-attributes

# pylint: disable=too-many-instance-attributes


@dataclass
class _ResponseTag:
    flow_tag: str
    device_name: str
    interface_name: str
    addr: str
    port: str
    tcp_flags: str
    protocol: str
    asn: str
    nexthop: str
    nexthop_asn: str
    bgp_aspath: str
    bgp_community: str
    device_type: str
    site: str
    lasthop_as_name: str
    nexthop_as_name: str
    mac: str
    country: str
    vlans: str
    id: int
    company_id: str
    addr_count: int
    user: str  # this is actually ID of user that created the tag
    mac_count: int
    edited_by: str
    created_date: str
    updated_date: str


# pylint: enable=too-many-instance-attributes


@dataclass()
class GetResponse:
    tag: _ResponseTag  # tags api payload is embedded under "tag" key

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(_ResponseTag(**dic["tag"]))

    # pylint: disable=too-many-arguments
    @classmethod
    def from_fields(
        cls,
        flow_tag: str,
        device_name: str,
        interface_name: str,
        addr: str,
        port: str,
        tcp_flags: str,
        protocol: str,
        asn: str,
        nexthop: str,
        nexthop_asn: str,
        bgp_aspath: str,
        bgp_community: str,
        device_type: str,
        site: str,
        lasthop_as_name: str,
        nexthop_as_name: str,
        mac: str,
        country: str,
        vlans: str,
        id: int,
        company_id: str,
        addr_count: int,
        user: str,
        mac_count: int,
        edited_by: str,
        created_date: str,
        updated_date: str,
    ):
        tag = _ResponseTag(
            flow_tag=flow_tag,
            device_name=device_name,
            interface_name=interface_name,
            addr=addr,
            port=port,
            tcp_flags=tcp_flags,
            protocol=protocol,
            asn=asn,
            nexthop=nexthop,
            nexthop_asn=nexthop_asn,
            bgp_aspath=bgp_aspath,
            bgp_community=bgp_community,
            device_type=device_type,
            site=site,
            lasthop_as_name=lasthop_as_name,
            nexthop_as_name=nexthop_as_name,
            mac=mac,
            country=country,
            vlans=vlans,
            id=id,
            company_id=company_id,
            addr_count=addr_count,
            user=user,
            mac_count=mac_count,
            edited_by=edited_by,
            created_date=created_date,
            updated_date=updated_date,
        )
        return cls(tag)

    # pylint: enable=too-many-arguments

    def to_tag(self) -> Tag:
        return Tag(
            flow_tag=self.tag.flow_tag,
            device_name=self.tag.device_name,
            interface_name=self.tag.interface_name,
            addr=self.tag.addr,
            port=self.tag.port,
            tcp_flags=self.tag.tcp_flags,
            protocol=self.tag.protocol,
            asn=self.tag.asn,
            nexthop=self.tag.nexthop,
            nexthop_asn=self.tag.nexthop_asn,
            bgp_aspath=self.tag.bgp_aspath,
            bgp_community=self.tag.bgp_community,
            device_type=self.tag.device_type,
            site=self.tag.site,
            lasthop_as_name=self.tag.lasthop_as_name,
            nexthop_as_name=self.tag.nexthop_as_name,
            mac=self.tag.mac,
            country=self.tag.country,
            vlans=self.tag.vlans,
            id=convert(self.tag.id, ID),
            company_id=convert(self.tag.company_id, ID),
            addr_count=self.tag.addr_count,
            user_id=convert(self.tag.user, ID),
            mac_count=self.tag.mac_count,
            edited_by=self.tag.edited_by,
            created_date=self.tag.created_date,
            updated_date=self.tag.updated_date,
        )


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        tags = cls()
        for item in dic["tags"]:
            s = GetResponse.from_fields(**item)
            tags.append(s)
        return tags

    def to_tags(self) -> List[Tag]:
        return [t.to_tag() for t in self]


class CreateRequest:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        flow_tag: str,
        device_name: Optional[str] = None,
        interface_name: Optional[str] = None,
        addr: Optional[str] = None,
        port: Optional[str] = None,
        tcp_flags: Optional[str] = None,
        protocol: Optional[str] = None,
        asn: Optional[str] = None,
        nexthop: Optional[str] = None,
        nexthop_asn: Optional[str] = None,
        bgp_aspath: Optional[str] = None,
        bgp_community: Optional[str] = None,
        device_type: Optional[str] = None,
        site: Optional[str] = None,
        lasthop_as_name: Optional[str] = None,
        nexthop_as_name: Optional[str] = None,
        mac: Optional[str] = None,
        country: Optional[str] = None,
        vlans: Optional[str] = None,
    ) -> None:
        self.tag = _RequestTag(
            flow_tag=flow_tag,
            device_name=device_name,
            interface_name=interface_name,
            addr=addr,
            port=port,
            tcp_flags=tcp_flags,
            protocol=protocol,
            asn=asn,
            nexthop=nexthop,
            nexthop_asn=nexthop_asn,
            bgp_aspath=bgp_aspath,
            bgp_community=bgp_community,
            device_type=device_type,
            site=site,
            lasthop_as_name=lasthop_as_name,
            nexthop_as_name=nexthop_as_name,
            mac=mac,
            country=country,
            vlans=vlans,
        )

    # pylint: enable=too-many-arguments


CreateResponse = GetResponse


class UpdateRequest:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        flow_tag: Optional[str] = None,
        device_name: Optional[str] = None,
        interface_name: Optional[str] = None,
        addr: Optional[str] = None,
        port: Optional[str] = None,
        tcp_flags: Optional[str] = None,
        protocol: Optional[str] = None,
        asn: Optional[str] = None,
        nexthop: Optional[str] = None,
        nexthop_asn: Optional[str] = None,
        bgp_aspath: Optional[str] = None,
        bgp_community: Optional[str] = None,
        device_type: Optional[str] = None,
        site: Optional[str] = None,
        lasthop_as_name: Optional[str] = None,
        nexthop_as_name: Optional[str] = None,
        mac: Optional[str] = None,
        country: Optional[str] = None,
        vlans: Optional[str] = None,
    ) -> None:
        self.tag = _RequestTag(
            flow_tag=flow_tag,
            device_name=device_name,
            interface_name=interface_name,
            addr=addr,
            port=port,
            tcp_flags=tcp_flags,
            protocol=protocol,
            asn=asn,
            nexthop=nexthop,
            nexthop_asn=nexthop_asn,
            bgp_aspath=bgp_aspath,
            bgp_community=bgp_community,
            device_type=device_type,
            site=site,
            lasthop_as_name=lasthop_as_name,
            nexthop_as_name=nexthop_as_name,
            mac=mac,
            country=country,
            vlans=vlans,
        )

    # pylint: enable=too-many-arguments


UpdateResponse = GetResponse


# @dataclass()
# class DeleteResponse:
#     """ Currently tag delete response carries no body data just http code 204 for succcess """
