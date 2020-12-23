from http import HTTPStatus
from typing import List

from kentik_api.api_calls import plan
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.public.plan import Plan
from kentik_api.requests_payload import plans_payload


class PlansAPI:
    """Exposes Kentik API operations related to plans. """

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def get_all(self) -> List[Plan]:
        api_call = plan.get_plans()
        response = self._api_connector.send(api_call)
        return plans_payload.GetAllResponse.from_json(response.text).to_plans()
