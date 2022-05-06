from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.tag import Tag
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, dict_from_json, from_dict, list_from_json
from kentik_api.requests_payload.validation import validate_fields

# pylint: disable=too-many-instance-attributes


# Note: for Tag create, only flow_tag is required
@dataclass
class TagPayload:
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
    id: Optional[int] = None
    company_id: Optional[str] = None
    addr_count: Optional[int] = None
    user: Optional[str] = None  # this is actually ID of user that created the tag
    mac_count: Optional[int] = None
    edited_by: Optional[str] = None
    created_date: Optional[str] = None
    updated_date: Optional[str] = None

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        # recreate GET/POST/PUT response payload: fill all available fields
        required_fields = [
            "id",
            "company_id",
            "flow_tag",
            "created_date",
        ]
        validate_fields(class_name=cls.__name__, required_fields=required_fields, dic=dic)
        return from_dict(data_class=cls, data=dic)

    @classmethod
    def from_tag(cls, tag: Tag):
        # prepare POST/PUT request payload: fill only the user-provided fields
        return cls(
            flow_tag=tag.flow_tag,
            device_name=tag.device_name,
            interface_name=tag.interface_name,
            addr=tag.addr,
            port=tag.port,
            tcp_flags=tag.tcp_flags,
            protocol=tag.protocol,
            asn=tag.asn,
            nexthop=tag.nexthop,
            nexthop_asn=tag.nexthop_asn,
            bgp_aspath=tag.bgp_aspath,
            bgp_community=tag.bgp_community,
            device_type=tag.device_type,
            site=tag.site,
            lasthop_as_name=tag.lasthop_as_name,
            nexthop_as_name=tag.nexthop_as_name,
            mac=tag.mac,
            country=tag.country,
            vlans=tag.vlans,
        )

    def to_tag(self) -> Tag:
        return Tag(
            flow_tag=self.flow_tag,
            device_name=self.device_name,
            interface_name=self.interface_name,
            addr=self.addr,
            port=self.port,
            tcp_flags=self.tcp_flags,
            protocol=self.protocol,
            asn=self.asn,
            nexthop=self.nexthop,
            nexthop_asn=self.nexthop_asn,
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
            addr_count=self.addr_count,
            user_id=convert(self.user, ID),
            mac_count=self.mac_count,
            edited_by=self.edited_by,
            created_date=self.created_date,
            updated_date=self.updated_date,
        )


@dataclass()
class GetResponse:
    tag: TagPayload  # tags api payload is embedded under "tag" key

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string, "tag")
        return cls(tag=TagPayload.from_dict(dic))

    def to_tag(self) -> Tag:
        return self.tag.to_tag()


@dataclass
class GetAllResponse:
    responses: List[GetResponse]

    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string, "tags")
        responses = [GetResponse(TagPayload.from_dict(item)) for item in items]
        return cls(responses)

    def to_tags(self) -> List[Tag]:
        return [t.to_tag() for t in self.responses]


@dataclass
class CreateRequest:
    tag: TagPayload

    @classmethod
    def from_tag(cls, tag: Tag):
        CreateRequest.validate(tag)
        return cls(tag=TagPayload.from_tag(tag))

    @staticmethod
    def validate(tag: Tag) -> None:
        if tag.flow_tag is None:
            raise IncompleteObjectError("Create", tag.__class__.__name__, "flow_tag is required")


CreateResponse = GetResponse


@dataclass
class UpdateRequest:
    tag: TagPayload

    @classmethod
    def from_tag(cls, tag: Tag):
        return cls(tag=TagPayload.from_tag(tag))


UpdateResponse = GetResponse


# @dataclass()
# class DeleteResponse:
#     """ Currently tag delete response carries no body data just http code 204 for succcess """
