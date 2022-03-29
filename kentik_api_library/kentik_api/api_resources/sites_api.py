from http import HTTPStatus
from typing import List

from kentik_api.api_calls import sites
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.site import Site
from kentik_api.public.types import ID
from kentik_api.requests_payload import sites_payload


class SitesAPI(BaseAPI):
    """Exposes Kentik API operations related to sites"""

    def get_all(self) -> List[Site]:
        apicall = sites.get_sites()
        response = self.send(apicall)
        return sites_payload.GetAllResponse.from_json(response.text).to_sites()

    def get(self, site_id: ID) -> Site:
        apicall = sites.get_site_info(site_id)
        response = self.send(apicall)
        return sites_payload.GetResponse.from_json(response.text).to_site()

    def create(self, site: Site) -> Site:
        apicall = sites.create_site()
        payload = sites_payload.CreateRequest.from_site(site)
        response = self.send(apicall, payload)
        return sites_payload.CreateResponse.from_json(response.text).to_site()

    def update(self, site: Site) -> Site:
        apicall = sites.update_site(site.id)
        payload = sites_payload.UpdateRequest.from_site(site)
        response = self.send(apicall, payload)
        return sites_payload.UpdateResponse.from_json(response.text).to_site()

    def delete(self, site_id: ID) -> bool:
        apicall = sites.delete_site(site_id)
        response = self.send(apicall)
        return response.http_status_code == HTTPStatus.NO_CONTENT
