from http import HTTPStatus
from typing import List

from kentik_api.api_calls import custom_dimensions
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.custom_dimension import CustomDimension, Populator
from kentik_api.public.types import ID
from kentik_api.requests_payload import custom_dimensions_payload, populators_payload


class PopulatorsAPI(BaseAPI):
    """Exposes Kentik API operations related to populators (belong to custom dimensions)"""

    def create(self, populator: Populator) -> Populator:
        apicall = custom_dimensions.create_populator(populator.dimension_id)
        payload = populators_payload.CreateRequest.from_populator(populator)
        response = self.send(apicall, payload)
        return populators_payload.CreateResponse.from_json(response.text).to_populator()

    def update(self, populator: Populator) -> Populator:
        apicall = custom_dimensions.update_populator(populator.dimension_id, populator.id)
        payload = populators_payload.UpdateRequest.from_populator(populator)
        response = self.send(apicall, payload)
        return populators_payload.UpdateResponse.from_json(response.text).to_populator()

    def delete(self, custom_dimension_id: ID, populator_id: ID) -> bool:
        apicall = custom_dimensions.delete_populator(custom_dimension_id, populator_id)
        response = self.send(apicall)
        return response.http_status_code == HTTPStatus.NO_CONTENT


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
        apicall = custom_dimensions.create_custom_dimension()
        payload = custom_dimensions_payload.CreateRequest.from_custom_dimension(custom_dimension)
        response = self.send(apicall, payload)
        return custom_dimensions_payload.CreateResponse.from_json(response.text).to_custom_dimension()

    def update(self, custom_dimension: CustomDimension) -> CustomDimension:
        apicall = custom_dimensions.update_custom_dimension(custom_dimension.id)
        payload = custom_dimensions_payload.UpdateRequest.from_custom_dimension(custom_dimension)
        response = self.send(apicall, payload)
        return custom_dimensions_payload.UpdateResponse.from_json(response.text).to_custom_dimension()

    def delete(self, custom_dimension_id: ID) -> bool:
        apicall = custom_dimensions.delete_custom_dimension(custom_dimension_id)
        response = self.send(apicall)
        return response.http_status_code == HTTPStatus.NO_CONTENT

    @property
    def populators(self) -> PopulatorsAPI:
        return self._populators
