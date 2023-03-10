from http import HTTPStatus

import httpretty
import pytest
from requests.packages.urllib3.util.retry import Retry

from kentik_api import KentikAPI
from kentik_api.public.errors import (
    AuthError,
    BadRequestError,
    DeserializationError,
    KentikAPIError,
    NotFoundError,
    ProtocolError,
    RateLimitExceededError,
    UnavailabilityError,
)

AUTH_EMAIL_KEY: str = "X-CH-Auth-Email"
AUTH_API_TOKEN_KEY: str = "X-CH-Auth-API-Token"
DUMMY_AUTH_EMAIL: str = "email@example.com"
DUMMY_TOKEN: str = "api-test-token"
DUMMY_USER_ID: int = 1337
FAKE_API_HOST: str = "api.fakekentik.com"
FAKE_API_V5_URL: str = KentikAPI.make_api_v5_url(FAKE_API_HOST)


@httpretty.activate
def test_get_user_fails_when_uncommon_http_error_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=418,
        body='{"error":"I\'m a Teapot"}',
    )

    # when
    with pytest.raises(ProtocolError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert exc_info.value.protocol == "HTTP"
    assert exc_info.value.status_code == 418
    assert str(exc_info.value) == '{"error":"I\'m a Teapot"}'


@httpretty.activate
def test_get_user_fails_when_status_bad_request_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.BAD_REQUEST.value,
        body='{"error":"Bad Request"}',
    )

    # when
    with pytest.raises(BadRequestError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Bad Request"}'


@httpretty.activate
def test_get_user_fails_when_status_unauthorized_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.UNAUTHORIZED.value,
        body='{"error":"Unauthorized"}',
    )

    # when
    with pytest.raises(AuthError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Unauthorized"}'


@httpretty.activate
def test_get_user_fails_when_status_forbidden_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.FORBIDDEN.value,
        body='{"error":"Forbidden"}',
    )

    # when
    with pytest.raises(AuthError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Forbidden"}'


@httpretty.activate
def test_get_user_fails_when_status_not_found_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.NOT_FOUND.value,
        body='{"error":"Not Found"}',
    )

    # when
    with pytest.raises(NotFoundError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Not Found"}'


@httpretty.activate
def test_get_user_fails_when_status_too_many_requests_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.TOO_MANY_REQUESTS.value,
        body='{"error":"Too Many Requests"}',
    )

    # when
    with pytest.raises(RateLimitExceededError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Too Many Requests"}'


@httpretty.activate
def test_get_user_fails_when_status_internal_server_error_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        body='{"error":"Internal Server Error"}',
    )

    # when
    with pytest.raises(KentikAPIError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Internal Server Error"}'


@httpretty.activate
def test_get_user_fails_when_status_service_unavailable_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.SERVICE_UNAVAILABLE.value,
        body='{"error":"Service Unavailable"}',
    )

    # when
    with pytest.raises(UnavailabilityError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Service Unavailable"}'


@httpretty.activate
def test_get_user_fails_when_gateway_timeout_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.GATEWAY_TIMEOUT.value,
        body='{"error":"Gateway Timeout"}',
    )

    # when
    with pytest.raises(UnavailabilityError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0

    assert str(exc_info.value) == '{"error":"Gateway Timeout"}'


@httpretty.activate
def test_get_user_fails_when_invalid_response_body_received(kentik_api) -> None:
    # given
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/user/{DUMMY_USER_ID}",
        status=HTTPStatus.OK.value,
        body='"{"dummy":"invalid response body"}"',
    )

    # when
    with pytest.raises(DeserializationError):
        kentik_api.users.get(DUMMY_USER_ID)

    # then
    assert len(httpretty.latest_requests()) == 1
    assert len(httpretty.last_request().querystring) == 0
    assert httpretty.last_request().headers.get(AUTH_EMAIL_KEY) == DUMMY_AUTH_EMAIL
    assert httpretty.last_request().headers.get(AUTH_API_TOKEN_KEY) == DUMMY_TOKEN
    assert len(httpretty.last_request().body) == 0


def test_get_user_fails_when_server_is_down(kentik_api) -> None:
    with pytest.raises(KentikAPIError) as exc_info:
        kentik_api.users.get(DUMMY_USER_ID)

    assert "Failed to establish a new connection" in str(exc_info.value)


@pytest.fixture
def kentik_api():
    return KentikAPI(
        DUMMY_AUTH_EMAIL,
        DUMMY_TOKEN,
        api_host=FAKE_API_HOST,
        retry_strategy=Retry(total=1),
    )
