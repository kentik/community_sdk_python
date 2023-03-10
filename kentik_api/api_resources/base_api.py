from typing import Any, Optional

from kentik_api.api_calls.api_call import APICall
from kentik_api.api_connection.api_call_response import APICallResponse
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol
from kentik_api.requests_payload.conversions import as_dict


class BaseAPI:
    """Base class containing attributes common to all API handlers."""

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def send(self, api_call: APICall, payload: Optional[Any] = None) -> APICallResponse:
        if payload is not None:
            payload = as_dict(payload)
        return self._api_connector.send(api_call, payload)
