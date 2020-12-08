from typing import List

from kentik_api.api_calls import sites
from kentik_api.public.site import Site
from kentik_api.requests_payload import sites_payload, as_dict
from kentik_api.api_connection.api_connector_protocol import APIConnectorProtocol


class SitesAPI:
    """ Exposes Kentik API operations related to sites """

    def __init__(self, api_connector: APIConnectorProtocol) -> None:
        self._api_connector = api_connector

    def _send(self, api_call, payload=None):
        if payload is not None:
            payload = as_dict.as_dict(payload)
        return self._api_connector.send(api_call, payload)

    def get_all(self) -> List[Site]:
        apicall = sites.get_sites()
        response = self._send(apicall)
        return sites_payload.GetAllResponse.from_json(response.text).to_sites()

    def get(self, site_id: int) -> Site:
        apicall = sites.get_site_info(site_id)
        response = self._send(apicall)
        return sites_payload.GetResponse.from_json(response.text).to_site()

    def create(self, site: Site) -> Site:
        apicall = sites.create_site()
        payload = sites_payload.CreateRequest(site.site_name, site.latitude, site.longitude)
        response = self._send(apicall, payload)
        return sites_payload.CreateResponse.from_json(response.text).to_site()

    def update(self, site: Site) -> Site:
        apicall = sites.update_site(site.id)
        payload = sites_payload.UpdateRequest(site.site_name, site.latitude, site.longitude)
        response = self._send(apicall, payload)
        return sites_payload.UpdateResponse.from_json(response.text).to_site()

    def delete(self, site_id: int) -> bool:
        apicall = sites.delete_site(site_id)
        response = self._send(apicall)
        return response.http_status_code == 204
