# Standard library imports
import logging
from typing import Optional, Dict, Any

# Third party imports
import requests

# Local application imports
from kentik_api.auth.auth import KentikAuth
from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_connection.api_call_response import APICallResponse
 
class APIConnector:
    """ Allows sending authorized http requests to Kentik API """

    DEFAULT_HEADERS = {"Content-Type": "application/json"}
    BASE_API_COM_URL = "https://api.kentik.com/api"
    BASE_API_EU_URL = "https://api.kentik.eu/api"

    def __init__(self, api_url: str, auth_email: str, auth_token: str) -> None:
        self._api_url = api_url
        self._auth = KentikAuth(auth_email, auth_token)
        self._logger = logging.getLogger(__name__)


    def send(self, api_call: APICall, payload: Optional[Dict[str, Any]] = None) -> APICallResponse:
        if payload is not None:
            payload = remove_keys_with_empty_values(payload)

        url = self._get_api_query_url(api_call.url_path)
        response : requests.Response
 
        if api_call.method == APICallMethods.GET:
            response = requests.get(url, auth=self._auth, headers=self.DEFAULT_HEADERS, params=payload)
        elif api_call.method == APICallMethods.POST:
            response =  requests.post(url, auth=self._auth, headers=self.DEFAULT_HEADERS, json=payload)
        elif api_call.method == APICallMethods.PUT:
            response =  requests.put(url, auth=self._auth, headers=self.DEFAULT_HEADERS, json=payload)
        elif api_call.method == APICallMethods.DELETE:
            response =  requests.delete(url, auth=self._auth, headers=self.DEFAULT_HEADERS, json=payload)
        else:
            raise ValueError(f"Improper API call method: {api_call.method}")
            
        self._validate_response(response)

        return APICallResponse(response.status_code, response.text)


    def _get_api_query_url(self, api_method: str) -> str:
        return self._api_url + api_method

    def _validate_response(self, response : requests.Response) -> None:
        # http error handling can be implemented here eg with exceptions, Expected[return, error] or error codes
        if response.status_code >= 400:
            self._logger.error("code: %d, body: %s", response.status_code, response.text)


def remove_keys_with_empty_values(d : Dict[str, Any]) -> Dict[str, Any]:
    result = dict()
    for k, v in d.items():
        if v is not None:
            result[k] = v
    return result
