# Standard library imports
import logging
from http import HTTPStatus
from typing import Union, Tuple, Optional, Dict, Any

# Third party imports
from requests import Timeout, RequestException, Response

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
from .retryable_session import RetryableSession, Retry

PROTOCOL_HTTP = "HTTP"


class APIConnector:
    """APIConnector implements APIConnectorProtocol. Allows sending authorized http requests to Kentik API"""

    def __init__(
        self,
        api_url: str,
        auth_email: str,
        auth_token: str,
        timeout: Union[float, Tuple[float, float]] = (10.0, 60.0),
        retry_strategy: Optional[Retry] = None,
    ) -> None:
        self._api_url = api_url
        self._logger = logging.getLogger(__name__)
        self._session = RetryableSession(retry_strategy=retry_strategy)
        self._session.auth = KentikAuth(auth_email, auth_token)
        self._session.headers.update({"Content-Type": "application/json"})
        self._timeout = timeout

    def send(self, api_call: APICall, payload: Optional[Dict[str, Any]] = None) -> APICallResponse:
        try:
            response = self._do_request(api_call, payload)
        except Timeout as e:
            raise TimedOutError(str(e)) from e
        except RequestException as e:
            raise KentikAPIError(str(e)) from e

        self._log_http_roundtrip(response)
        self._raise_on_error(response)

        return APICallResponse(response.status_code, response.text)

    def _do_request(self, api_call: APICall, payload: Optional[Dict[str, Any]] = None) -> Response:

        url = self._get_api_query_url(api_call.url_path)
        if api_call.method == APICallMethods.GET:
            response = self._session.get(url, params=payload, timeout=self._timeout)
        elif api_call.method == APICallMethods.POST:
            response = self._session.post(url, json=payload, timeout=self._timeout)
        elif api_call.method == APICallMethods.PUT:
            response = self._session.put(url, json=payload, timeout=self._timeout)
        elif api_call.method == APICallMethods.DELETE:
            response = self._session.delete(url, json=payload, timeout=self._timeout)
        else:
            raise ValueError(f"Improper API call method: {api_call.method}")
        return response

    def _log_http_roundtrip(self, response: Response) -> None:
        self._logger.debug(
            f"HTTP roundtrip finished - "
            f"request: {response.request.method} {response.request.url} {str(response.request.body)}, "
            f"response: {response.status_code} {response.text}, "
            f"elapsed: {response.elapsed}"
        )

    def _get_api_query_url(self, url_path: str) -> str:
        return self._api_url + url_path

    @staticmethod
    def _raise_on_error(response: Response) -> None:
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
