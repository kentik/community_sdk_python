from typing import Any

from kentik_api.api_calls.api_call import APICall
from kentik_api.api_connection.api_call_response import APICallResponse


class StubAPIConnector:
    """StubAPIConnector allows for stubbed responses for api requests"""

    def __init__(self, response_text: str, response_code: int):
        self.last_url = None
        self.last_method = None
        self.last_payload = None
        self.response_text = response_text
        self.response_code = response_code

    def send(self, api_call: APICall, payload: Any = None) -> APICallResponse:
        self.last_url = api_call.url_path
        self.last_method = api_call.method
        self.last_payload = payload
        return APICallResponse(self.response_code, self.response_text)
