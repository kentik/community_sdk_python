# Standard library imports
import logging
from http import HTTPStatus
from typing import Any, Dict, Optional, Tuple, Union

# Third party imports
from requests import RequestException, Response, Timeout

# Local application imports
from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_connection.api_call_response import APICallResponse
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
from kentik_api.version import get_user_agent

from .retryable_session import Retry, prepare_kentik_api_http_session

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
        proxy: Optional[str] = None,
    ) -> None:
        self._api_url = api_url
        self._logger = logging.getLogger(__name__)
        self._session = prepare_kentik_api_http_session(auth_email, auth_token, retry_strategy, proxy)
        self._session.headers["User-Agent"] = get_user_agent()
        self._timeout = timeout
        if proxy:
            self._logger.debug("Using proxy: %s", proxy)

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
            f"HTTP request done: "
            f"request: {response.request.method} {response.request.url}, "
            f"response: {response.status_code} {len(response.text)} bytes, "
            f"elapsed: {response.elapsed}"
        )

    def _get_api_query_url(self, url_path: str) -> str:
        return self._api_url + url_path

    @staticmethod
    def _raise_on_error(response: Response) -> None:
        if response.status_code >= 400:
            raise new_api_error(response.text, response.status_code)


def new_api_error(message: str, http_status_code: int) -> KentikAPIError:
    # noinspection PyUnresolvedReferences
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
