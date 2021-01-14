# pylint: disable=too-few-public-methods
from typing import Any, Dict, Optional

from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_connection.api_call_response import APICallResponse


class StubAPIConnector:
    """StubAPIConnector implements APIConnectorProtocol. Allows for stubbed responses for api requests."""

    def __init__(self, response_text: Optional[str] = None, response_code: Optional[int] = None):
        self.last_url_path: Optional[str] = None
        self.last_method: Optional[APICallMethods] = None
        self.last_payload: Optional[Dict[str, Any]] = None
        self.response_text = response_text
        self.response_code = response_code

    def send(self, api_call: APICall, payload: Any = None) -> APICallResponse:
        assert self.response_code is not None
        assert self.response_text is not None
        self.last_url_path = api_call.url_path
        self.last_method = api_call.method
        self.last_payload = payload
        return APICallResponse(self.response_code, self.response_text)
