from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.sites_api import SitesAPI
from kentik_api.public.site import Site
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_site_success() -> None:
    # given
    create_response_payload = """
    {
        "site": {
            "id": 42,
            "site_name": "apitest-site-1",
            "lat": 54.349276,
            "lon": 18.659577,
            "company_id": "3250"
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED)
    sites_api = SitesAPI(connector)

    # when
    site = Site("apitest-site-1", 54.349276, 18.659577)
    created = sites_api.create(site)

    # then request properly formed
    assert connector.last_url_path == "/site"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert "site" in connector.last_payload
    assert connector.last_payload["site"]["site_name"] == "apitest-site-1"
    assert connector.last_payload["site"]["lat"] == 54.349276
    assert connector.last_payload["site"]["lon"] == 18.659577

    # and response properly parsed
    assert created.id == ID(42)
    assert created.site_name == "apitest-site-1"
    assert created.latitude == 54.349276
    assert created.longitude == 18.659577
    assert created.company_id == ID(3250)


def test_get_site_success() -> None:
    # given
    get_response_payload = """
    {
        "site": {
            "id": 42,
            "site_name": "apitest-site-1",
            "lat": 54.349276,
            "lon": 18.659577,
            "company_id": 3250
        }
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    sites_api = SitesAPI(connector)

    # when
    site_id = ID(42)
    site = sites_api.get(site_id)

    # then request properly formed
    assert connector.last_url_path == f"/site/{site_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    # then response properly parsed
    assert site.id == ID(42)
    assert site.site_name == "apitest-site-1"
    assert site.latitude == 54.349276
    assert site.longitude == 18.659577
    assert site.company_id == ID(3250)


def test_update_site_success() -> None:
    # given
    update_response_payload = """
    {
        "site": {
            "id": "42",
            "site_name": "new-site",
            "lat": -15.0,
            "lon": -45.0,
            "company_id": "3250"
        }
    }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    sites_api = SitesAPI(connector)

    # when
    site_id = ID(42)
    site = Site(site_name="new-site", latitude=None, longitude=-45.0, id=site_id)
    updated = sites_api.update(site)

    # then request properly formed
    assert connector.last_url_path == f"/site/{site_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None
    assert "site" in connector.last_payload
    assert connector.last_payload["site"]["site_name"] == "new-site"
    assert connector.last_payload["site"]["lon"] == -45.0
    assert "lat" not in connector.last_payload["site"]

    # then response properly parsed
    assert updated.id == ID(42)
    assert updated.site_name == "new-site"
    assert updated.latitude == -15.0
    assert updated.longitude == -45.0
    assert updated.company_id == ID(3250)


def test_delete_site_success() -> None:
    # given
    delete_response_payload = ""  # deleting site responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    sites_api = SitesAPI(connector)

    # when
    site_id = ID(42)
    delete_successful = sites_api.delete(site_id)

    # then request properly formed
    assert connector.last_url_path == f"/site/{site_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None

    # then response properly parsed
    assert delete_successful
