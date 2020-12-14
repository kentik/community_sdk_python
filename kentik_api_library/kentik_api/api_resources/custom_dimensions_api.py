from typing import List

from kentik_api.api_calls import custom_dimensions
from kentik_api.public.custom_dimension import CustomDimension
from kentik_api.requests_payload import custom_dimensions_payload, as_dict
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol


class CustomDimensionsAPI:
    """ Exposes Kentik API operations related to custom dimensions """

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def _send(self, api_call, payload=None):
        if payload is not None:
            payload = as_dict.as_dict(payload)
        return self._api_connector.send(api_call, payload)

    def get(self, custom_dimension_id: int) -> CustomDimension:
        apicall = custom_dimensions.get_custom_dimension_info(custom_dimension_id)
        response = self._send(apicall)
        return custom_dimensions_payload.GetResponse.from_json(response.text).to_custom_dimension()

    def get_all(self) -> List[CustomDimension]:
        apicall = custom_dimensions.get_custom_dimensions()
        response = self._send(apicall)
        return custom_dimensions_payload.GetAllResponse.from_json(response.text).to_custom_dimensions()

    def create(self, custom_dimension: CustomDimension) -> CustomDimension:
        assert custom_dimension.name is not None
        assert custom_dimension.display_name is not None
        assert custom_dimension.type is not None
        apicall = custom_dimensions.create_custom_dimension()
        payload = custom_dimensions_payload.CreateRequest(
            name=custom_dimension.name,
            display_name=custom_dimension.display_name,
            type=custom_dimension.type,
        )
        response = self._send(apicall, payload)
        return custom_dimensions_payload.CreateResponse.from_json(response.text).to_custom_dimension()

    def update(self, custom_dimension: CustomDimension) -> CustomDimension:
        assert custom_dimension.display_name is not None
        apicall = custom_dimensions.update_custom_dimension(custom_dimension.id)
        payload = custom_dimensions_payload.UpdateRequest(
            display_name=custom_dimension.display_name,
        )
        response = self._send(apicall, payload)
        return custom_dimensions_payload.UpdateResponse.from_json(response.text).to_custom_dimension()

    def delete(self, custom_dimension_id: int) -> bool:
        apicall = custom_dimensions.delete_custom_dimension(custom_dimension_id)
        response = self._send(apicall)
        return response.http_status_code == 204
