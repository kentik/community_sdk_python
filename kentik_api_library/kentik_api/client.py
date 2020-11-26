# Standard library imports
from typing import Optional

# Third party imports
import requests

# Local application imports
from kentik_api.auth.auth import KentikAuth
from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.api_call import APICallMethods


class API:
    DEFAULT_HEADERS = {"Content-Type": "application/json"}

    def __init__(self, api_url: str, auth_email: str, auth_token: str):
        self._api_url = api_url
        self._auth = KentikAuth(auth_email, auth_token)

    def send_query(self, api_call: APICall, payload: Optional[type] = None):

        # print("#"*80)
        # print(api_call.method)
        # print("#"*80)

        _payload: Optional[dict] = payload if isinstance(payload, dict) else None
        url = self._get_api_query_url(api_call.url_path)
        if api_call.method == APICallMethods.GET:
            return requests.get(url, auth=self._auth, headers=self.DEFAULT_HEADERS, params=_payload)
        if api_call.method == APICallMethods.POST:
            # print("HERE "*5)
            return requests.post(url, auth=self._auth, headers=self.DEFAULT_HEADERS, json=_payload)
        if api_call.method == APICallMethods.PUT:
            return requests.put(url, auth=self._auth, headers=self.DEFAULT_HEADERS, data=_payload)
        if api_call.method == APICallMethods.DELETE:
            return requests.delete(url, auth=self._auth, headers=self.DEFAULT_HEADERS, data=payload)
        raise ValueError("Improper API call method")

    def _get_api_query_url(self, api_method: str):
        return self._api_url + api_method

# Third party imports
from python_http_client import Client  # type: ignore

BASE_API_COM_URL = "https://api.kentik.com/api"
BASE_API_EU_URL = "https://api.kentik.eu/api"

GLOBAL_HEADERS_TEMPLATE = {
    "X-CH-Auth-Email": None,
    "X-CH-Auth-API-Token": None,
    "Content-Type": "application/json"
}


def get_kentik_client(base_url, auth_email, auth_api_token):
    global_headers = GLOBAL_HEADERS_TEMPLATE
    global_headers["X-CH-Auth-Email"] = auth_email
    global_headers["X-CH-Auth-API-Token"] = auth_api_token
    return Client(host=base_url, request_headers=global_headers)


def get_kentik_com_client(auth_email, auth_api_token):
    return get_kentik_client(BASE_API_COM_URL, auth_email, auth_api_token)


def get_kentik_eu_client(auth_email, auth_api_token):
    return get_kentik_client(BASE_API_EU_URL, auth_email, auth_api_token)

