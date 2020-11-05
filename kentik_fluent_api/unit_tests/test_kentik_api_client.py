from kentik_api_client import kentik_api_client
from python_http_client import Client


DUMMY_API_URL = " www.dummyurl.test"
DUMMY_EMAIL = "dummy@email"
DUMMY_API_TOKEN = "dummy_api_tocen"


def test_get_kentik_client__return_api_client():
    # GIVEN
    # DUMMY_API_URL, DUMMY_EMAIL, DUMMY_API_TOKEN

    # WHEN
    client = kentik_api_client.get_kentik_client(DUMMY_API_URL, DUMMY_EMAIL, DUMMY_API_TOKEN)

    # THEN
    assert isinstance(client, Client)


def test_get_kentik_com_client__return_com_api_client():
    # GIVEN
    # DUMMY_EMAIL, DUMMY_API_TOKEN

    # WHEN
    client = kentik_api_client.get_kentik_com_client(DUMMY_EMAIL, DUMMY_API_TOKEN)

    # THEN
    assert isinstance(client, Client)
    assert client.host == kentik_api_client.BASE_API_COM_URL


def test_get_kentik_com_client__return_eu_api_client():
    # GIVEN
    # DUMMY_EMAIL, DUMMY_API_TOKEN

    # WHEN
    client = kentik_api_client.get_kentik_eu_client(DUMMY_EMAIL, DUMMY_API_TOKEN)

    # THEN
    assert isinstance(client, Client)
    assert client.host == kentik_api_client.BASE_API_EU_URL
