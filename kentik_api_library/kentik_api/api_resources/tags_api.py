from typing import List

from kentik_api.api_calls import tags
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.types import ID
from kentik_api.public.tag import Tag
from kentik_api.requests_payload import tags_payload


class TagsAPI(BaseAPI):
    """ Exposes Kentik API operations related to tags """

    def get_all(self) -> List[Tag]:
        apicall = tags.get_tags()
        response = self.send(apicall)
        return tags_payload.GetAllResponse.from_json(response.text).to_tags()

    def get(self, tag_id: ID) -> Tag:
        apicall = tags.get_tag_info(tag_id)
        response = self.send(apicall)
        return tags_payload.GetResponse.from_json(response.text).to_tag()

    def create(self, tag: Tag) -> Tag:
        assert tag.flow_tag is not None
        apicall = tags.create_tag()
        payload = tags_payload.CreateRequest(
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
        response = self.send(apicall, payload)
        return tags_payload.CreateResponse.from_json(response.text).to_tag()

    def update(self, tag: Tag) -> Tag:
        apicall = tags.update_tag(tag.id)
        payload = tags_payload.UpdateRequest(
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
        response = self.send(apicall, payload)
        return tags_payload.UpdateResponse.from_json(response.text).to_tag()

    def delete(self, tag_id: ID) -> bool:
        apicall = tags.delete_tag(tag_id)
        response = self.send(apicall)
        return response.http_status_code == 204
