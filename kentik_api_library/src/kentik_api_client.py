# Standard library imports
from typing import Optional

# Third party imports
import requests

# Local application imports
from auth import auth
from api_calls.api_call import APICall
from api_calls.api_call import APICallMethods


class KentikAPIClient:
    DEFAULT_HEADERS = {"Content-Type": "application/json"}

    def __init__(self, api_url: str, auth_email: str, auth_token: str):
        self._api_url = api_url
        self._auth = auth.KentikAuth(auth_email, auth_token)

    def send_query(self, query: APICall, payload: Optional[type] = None):

        _payload: Optional[dict] = payload if isinstance(payload, dict) else None
        url = self._get_api_query_url(query.url_path)
        if query.method == APICallMethods.GET:
            return requests.get(url, auth=self._auth, headers=self.DEFAULT_HEADERS, params=_payload)
        if query.method == APICallMethods.POST:
            return requests.get(url, auth=self._auth, headers=self.DEFAULT_HEADERS, data=payload)
        if query.method == APICallMethods.PUT:
            return requests.get(url, auth=self._auth, headers=self.DEFAULT_HEADERS, data=payload)
        if query.method == APICallMethods.DELETE:
            return requests.get(url, auth=self._auth, headers=self.DEFAULT_HEADERS, data=payload)

    def _get_api_query_url(self, api_method: str):
        return self._api_url + api_method

