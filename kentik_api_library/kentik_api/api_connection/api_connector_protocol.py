from typing import Protocol, Optional, Dict, Any

from kentik_api.api_calls.api_call import APICall
from kentik_api.api_connection.api_call_response import APICallResponse

class APIConnectorProtocol(Protocol):
    def send(self, api_call: APICall, payload: Optional[Dict[str, Any]] = None) -> APICallResponse:
        pass
