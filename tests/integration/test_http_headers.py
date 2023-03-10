import httpretty
import pytest

from kentik_api import KentikAPI

DUMMY_AUTH_EMAIL: str = "email@example.com"
DUMMY_TOKEN: str = "api-test-token"
FAKE_API_HOST: str = "api.fakekentik.com"
FAKE_API_V5_URL: str = KentikAPI.make_api_v5_url(FAKE_API_HOST)


@httpretty.activate
def test_user_agent_header_set(kentik_api) -> None:
    # given
    get_labels_response = httpretty.Response("[]")  # empty labels list JSON
    httpretty.register_uri(
        httpretty.GET,
        f"{FAKE_API_V5_URL}/deviceLabels",
        status=200,
        responses=[get_labels_response],
    )

    # when
    kentik_api.device_labels.get_all()

    # then
    assert len(httpretty.latest_requests()) == 1
    assert "kentik_community_sdk_python/" in httpretty.last_request().headers.get("User-Agent")


@pytest.fixture
def kentik_api():
    return KentikAPI(
        DUMMY_AUTH_EMAIL,
        DUMMY_TOKEN,
        api_host=FAKE_API_HOST,
    )
