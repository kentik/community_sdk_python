from http import HTTPStatus
from typing import List

from kentik_api.api_calls import custom_dimensions
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.custom_dimension import CustomDimension, Populator
from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.types import ID
from kentik_api.requests_payload import custom_dimensions_payload, populators_payload
from kentik_api.requests_payload.conversions import convert, permissive_enum_to_str


class PopulatorsAPI(BaseAPI):
    """Exposes Kentik API operations related to populators (belong to custom dimensions)"""

    def create(self, populator: Populator) -> Populator:
        PopulatorsAPI.check_fields(populator, "Create")
        apicall = custom_dimensions.create_populator(populator.dimension_id)
        payload = populators_payload.CreateRequest(
            value=populator.value,
            direction=populator.direction.value,
            device_name=populator.device_name,
            interface_name=populator.interface_name,
            addr=populator.addr,
            port=populator.port,
            tcp_flags=populator.tcp_flags,
            protocol=populator.protocol,
            asn=populator.asn,
            nexthop_asn=populator.nexthop_asn,
            nexthop=populator.nexthop,
            bgp_aspath=populator.bgp_aspath,
            bgp_community=populator.bgp_community,
            device_type=populator.device_type,
            site=populator.site,
            lasthop_as_name=populator.lasthop_as_name,
            nexthop_as_name=populator.nexthop_as_name,
            mac=populator.mac,
            country=populator.country,
            vlans=populator.vlans,
        )
        response = self.send(apicall, payload)
        return populators_payload.CreateResponse.from_json(response.text).to_populator()

    def update(self, populator: Populator) -> Populator:
        PopulatorsAPI.check_fields(populator, "Update")
        apicall = custom_dimensions.update_populator(populator.dimension_id, populator.id)
        payload = populators_payload.UpdateRequest(
            value=populator.value,
            direction=convert(populator.direction, permissive_enum_to_str),
            device_name=populator.device_name,
            interface_name=populator.interface_name,
            addr=populator.addr,
            port=populator.port,
            tcp_flags=populator.tcp_flags,
            protocol=populator.protocol,
            asn=populator.asn,
            nexthop_asn=populator.nexthop_asn,
            nexthop=populator.nexthop,
            bgp_aspath=populator.bgp_aspath,
            bgp_community=populator.bgp_community,
            device_type=populator.device_type,
            site=populator.site,
            lasthop_as_name=populator.lasthop_as_name,
            nexthop_as_name=populator.nexthop_as_name,
            mac=populator.mac,
            country=populator.country,
            vlans=populator.vlans,
        )
        response = self.send(apicall, payload)
        return populators_payload.UpdateResponse.from_json(response.text).to_populator()

    def delete(self, custom_dimension_id: ID, populator_id: ID) -> bool:
        apicall = custom_dimensions.delete_populator(custom_dimension_id, populator_id)
        response = self.send(apicall)
        return response.http_status_code == HTTPStatus.NO_CONTENT

    @staticmethod
    def check_fields(populator: Populator, method: string):
        class_op = f"{method} Populator"
        if populator.value is None:
            raise IncompleteObjectError(class_op, "value is required")
        if populator.direction is None:
            raise IncompleteObjectError(class_op, "direction is required")
        if populator.dimension_id is None:
            raise IncompleteObjectError(class_op, "dimension_id is required")


class CustomDimensionsAPI(BaseAPI):
    """Exposes Kentik API operations related to custom dimensions"""

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        super(CustomDimensionsAPI, self).__init__(api_connector)
        self._populators = PopulatorsAPI(api_connector)

    def get(self, custom_dimension_id: ID) -> CustomDimension:
        apicall = custom_dimensions.get_custom_dimension_info(custom_dimension_id)
        response = self.send(apicall)
        return custom_dimensions_payload.GetResponse.from_json(response.text).to_custom_dimension()

    def get_all(self) -> List[CustomDimension]:
        apicall = custom_dimensions.get_custom_dimensions()
        response = self.send(apicall)
        return custom_dimensions_payload.GetAllResponse.from_json(response.text).to_custom_dimensions()

    def create(self, custom_dimension: CustomDimension) -> CustomDimension:
        class_op = "Create CustomDimensions"
        if custom_dimension.name is None:
            raise IncompleteObjectError(class_op, "name is required")
        if custom_dimension.display_name is None:
            raise IncompleteObjectError(class_op, "display_name is required")
        if custom_dimension.type is None:
            raise IncompleteObjectError(class_op, "type is required")
        apicall = custom_dimensions.create_custom_dimension()
        payload = custom_dimensions_payload.CreateRequest(
            name=custom_dimension.name,
            display_name=custom_dimension.display_name,
            type=custom_dimension.type,
        )
        response = self.send(apicall, payload)
        return custom_dimensions_payload.CreateResponse.from_json(response.text).to_custom_dimension()

    def update(self, custom_dimension: CustomDimension) -> CustomDimension:
        if custom_dimension.display_name is None:
            raise IncompleteObjectError("Update CustomDimensions", "display_name is required")
        apicall = custom_dimensions.update_custom_dimension(custom_dimension.id)
        payload = custom_dimensions_payload.UpdateRequest(
            display_name=custom_dimension.display_name,
        )
        response = self.send(apicall, payload)
        return custom_dimensions_payload.UpdateResponse.from_json(response.text).to_custom_dimension()

    def delete(self, custom_dimension_id: ID) -> bool:
        apicall = custom_dimensions.delete_custom_dimension(custom_dimension_id)
        response = self.send(apicall)
        return response.http_status_code == HTTPStatus.NO_CONTENT

    @property
    def populators(self) -> PopulatorsAPI:
        return self._populators
