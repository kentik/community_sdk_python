# Standard library imports
from typing import Optional

# Third party imports
import requests

# Local application imports
from auth.auth import KentikAuth
from api_calls.api_call import APICall
from api_calls.api_call import APICallMethods


class KentikAPIClient:
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

