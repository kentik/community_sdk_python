import unittest
from http import HTTPStatus

from kentik_api import kentik_api
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.site import Site
from tests.component.stub_api_connector import StubAPIConnector


class SitesAPITest(unittest.TestCase):
    def test_create_site(self):
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
        connector = StubAPIConnector(create_response_payload, HTTPStatus.CREATED.value)
        client = kentik_api.KentikAPI(connector)

        # when
        site = Site("apitest-site-1", 54.349276, 18.659577)
        created = client.sites.create(site)

        # then request properly formed
        self.assertEqual(connector.last_url, "/site")
        self.assertEqual(connector.last_method, APICallMethods.POST)
        request_payload = connector.last_payload
        self.assertIsNotNone(request_payload)
        self.assertEqual(request_payload["site"]["site_name"], "apitest-site-1")
        self.assertEqual(request_payload["site"]["lat"], 54.349276)
        self.assertEqual(request_payload["site"]["lon"], 18.659577)

        # then response properly unmarshalled
        self.assertEqual(created.id, 42)
        self.assertEqual(created.site_name, "apitest-site-1")
        self.assertEqual(created.latitude, 54.349276)
        self.assertEqual(created.longitude, 18.659577)
        self.assertEqual(created.company_id, "3250")

    def test_get_site(self):
        # given
        get_response_payload = """
        {
            "site": {
                "id": 42,
                "site_name": "apitest-site-1",
                "lat": 54.349276,
                "lon": 18.659577,
                "company_id": "3250"
            }
        }"""
        connector = StubAPIConnector(get_response_payload, HTTPStatus.OK.value)
        client = kentik_api.KentikAPI(connector)

        # when
        site_id = 42
        site = client.sites.get(site_id)

        # then request properly formed
        self.assertEqual(connector.last_url, f"/site/{site_id}")
        self.assertEqual(connector.last_method, APICallMethods.GET)
        self.assertIsNone(connector.last_payload)

        # then response properly unmarshalled
        self.assertEqual(site.id, 42)
        self.assertEqual(site.site_name, "apitest-site-1")
        self.assertEqual(site.latitude, 54.349276)
        self.assertEqual(site.longitude, 18.659577)
        self.assertEqual(site.company_id, "3250")

    def test_update_site(self):
        # given
        update_response_payload = """
        {
            "site": {
                "id": 42,
                "site_name": "new-site",
                "lat": -15.0,
                "lon": -45.0,
                "company_id": "3250"
            }
        }"""
        connector = StubAPIConnector(update_response_payload, HTTPStatus.OK.value)
        client = kentik_api.KentikAPI(connector)

        # when
        site_id = 42
        site = Site(site_name="new-site", latitude=None, longitude=-45.0, id=site_id)
        updated = client.sites.update(site)

        # then request properly formed
        self.assertEqual(connector.last_url, f"/site/{site_id}")
        self.assertEqual(connector.last_method, APICallMethods.PUT)
        request_payload = connector.last_payload
        self.assertIsNotNone(request_payload)
        self.assertEqual(request_payload["site"]["site_name"], "new-site")
        self.assertEqual(request_payload["site"]["lon"], -45.0)
        self.assertNotIn("lat", request_payload["site"])

        # then response properly unmarshalled
        self.assertEqual(updated.id, 42)
        self.assertEqual(updated.site_name, "new-site")
        self.assertEqual(updated.latitude, -15.0)
        self.assertEqual(updated.longitude, -45.0)
        self.assertEqual(updated.company_id, "3250")

    def test_delete_site(self):
        # given
        delete_response_payload = ""  # deleting site responds with empty body
        connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT.value)
        client = kentik_api.KentikAPI(connector)

        # when
        site_id = 42
        update_successful = client.sites.delete(site_id)

        # then request properly formed
        self.assertEqual(connector.last_url, f"/site/{site_id}")
        self.assertEqual(connector.last_method, APICallMethods.DELETE)
        self.assertIsNone(connector.last_payload)

        # then response properly unmarshalled
        self.assertTrue(update_successful)
