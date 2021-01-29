# Standard library imports
import logging
from http import HTTPStatus
from typing import Optional, Dict, Any

# Third party imports
import requests

# Local application imports
from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_connection.api_call_response import APICallResponse
from kentik_api.auth.auth import KentikAuth
from kentik_api.public.errors import (
    AuthError,
    BadRequestError,
    KentikAPIError,
    NotFoundError,
    ProtocolError,
    RateLimitExceededError,
    TimedOutError,
    UnavailabilityError,
)

PROTOCOL_HTTP = "HTTP"


class APIConnector:
    """ APIConnector implements APIConnectorProtocol. Allows sending authorized http requests to Kentik API """

    HEADERS = {"Content-Type": "application/json"}
    TIMEOUT = 30.0  # request timeout in seconds. Note: QueryAPI.chart easily takes 10 seconds to respond

    def __init__(self, api_url: str, auth_email: str, auth_token: str) -> None:
        self._api_url = api_url
        self._auth = KentikAuth(auth_email, auth_token)
        self._logger = logging.getLogger(__name__)

    def send(self, api_call: APICall, payload: Optional[Dict[str, Any]] = None) -> APICallResponse:
        try:
            response = self._do_request(api_call, payload)
        except requests.Timeout as e:
            raise TimedOutError(str(e)) from e
        except requests.RequestException as e:
            raise KentikAPIError(str(e)) from e

        self._log_http_roundtrip(response)
        self._raise_on_error(response)

        return APICallResponse(response.status_code, response.text)

    def _do_request(self, api_call: APICall, payload: Optional[Dict[str, Any]] = None) -> requests.Response:

        url = self._get_api_query_url(api_call.url_path)
        if api_call.method == APICallMethods.GET:
            response = requests.get(url, auth=self._auth, headers=self.HEADERS, params=payload, timeout=self.TIMEOUT)
        elif api_call.method == APICallMethods.POST:
            response = requests.post(url, auth=self._auth, headers=self.HEADERS, json=payload, timeout=self.TIMEOUT)
        elif api_call.method == APICallMethods.PUT:
            response = requests.put(url, auth=self._auth, headers=self.HEADERS, json=payload, timeout=self.TIMEOUT)
        elif api_call.method == APICallMethods.DELETE:
            response = requests.delete(url, auth=self._auth, headers=self.HEADERS, json=payload, timeout=self.TIMEOUT)
        else:
            raise ValueError(f"Improper API call method: {api_call.method}")
        return response

    def _log_http_roundtrip(self, response: requests.Response) -> None:
        self._logger.debug(
            f"HTTP roundtrip finished - "
            f"request: {response.request.method} {response.request.url} {str(response.request.body)}, "
            f"response: {response.status_code} {response.text}, "
            f"elapsed: {response.elapsed}"
        )

    def _get_api_query_url(self, url_path: str) -> str:
        return self._api_url + url_path

    @staticmethod
    def _raise_on_error(response: requests.Response) -> None:
        if response.status_code >= 400:
            raise new_api_error(response.text, response.status_code)


def new_api_error(message: str, http_status_code: int) -> KentikAPIError:
    common_errors = {
        HTTPStatus.BAD_REQUEST.value: BadRequestError,
        HTTPStatus.UNAUTHORIZED.value: AuthError,
        HTTPStatus.FORBIDDEN.value: AuthError,
        HTTPStatus.NOT_FOUND.value: NotFoundError,
        HTTPStatus.TOO_MANY_REQUESTS.value: RateLimitExceededError,
        HTTPStatus.SERVICE_UNAVAILABLE.value: UnavailabilityError,
        HTTPStatus.GATEWAY_TIMEOUT.value: UnavailabilityError,
    }
    try:
        error = common_errors[http_status_code](PROTOCOL_HTTP, http_status_code, message)
    except KeyError:
        return ProtocolError(PROTOCOL_HTTP, http_status_code, message)
    return error
