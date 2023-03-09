from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.site import Site
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, dict_from_json, from_dict, list_from_json


@dataclass
class SitePayload:
    """This data structure represents JSON SitePayload payload as it is transmitted to and from Kentik API"""

    site_name: Optional[str]  # eg. "apitest-site-1"
    lat: Optional[float]  # eg. 50.102
    lon: Optional[float]  # eg. 18.209

    @classmethod
    def from_site(cls, site: Site):
        return cls(
            site_name=site.site_name,
            lat=site.latitude,
            lon=site.longitude,
        )


@dataclass()
class GetResponse:
    @dataclass
    class _Site:
        id: int
        site_name: str
        lat: Optional[float]
        lon: Optional[float]
        company_id: int

    site: _Site  # sites api payload is embedded under "site" key

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string, root="site")
        return cls.from_dict(dic=dic)

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(site=from_dict(data_class=GetResponse._Site, data=dic))

    def to_site(self) -> Site:
        return Site(
            self.site.site_name,
            self.site.lat,
            self.site.lon,
            convert(self.site.id, ID),
            convert(self.site.company_id, ID),
        )


@dataclass(frozen=True)
class GetAllResponse:
    sites: List[GetResponse]

    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(class_name=cls.__name__, json_string=json_string, root="sites")
        sites = [GetResponse.from_dict(item) for item in items]
        return cls(sites=sites)

    def to_sites(self) -> List[Site]:
        return [item.to_site() for item in self.sites]


@dataclass()
class CreateResponse:
    @dataclass
    class _Site:
        id: int
        site_name: str
        lat: Optional[float]
        lon: Optional[float]
        company_id: str

    site: _Site  # sites api payload is embedded under "site" key

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string, root="site")
        return cls(site=from_dict(data_class=CreateResponse._Site, data=dic))

    def to_site(self) -> Site:
        return Site(
            self.site.site_name,
            self.site.lat,
            self.site.lon,
            convert(self.site.id, ID),
            convert(self.site.company_id, ID),
        )


@dataclass()
class UpdateResponse:
    @dataclass
    class _Site:
        id: str
        site_name: str
        lat: Optional[float]
        lon: Optional[float]
        company_id: str

    site: _Site  # sites api payload is embedded under "site" key

    @classmethod
    def from_json(cls, json_string):
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string, root="site")
        return cls(site=from_dict(data_class=UpdateResponse._Site, data=dic))

    def to_site(self) -> Site:
        return Site(
            self.site.site_name,
            self.site.lat,
            self.site.lon,
            convert(self.site.id, ID),
            convert(self.site.company_id, ID),
        )


@dataclass
class CreateRequest:

    site: SitePayload

    @classmethod
    def from_site(cls, site: Site):
        CreateRequest.validate(site)
        return cls(site=SitePayload.from_site(site))

    @staticmethod
    def validate(site: Site):
        if site.site_name is None:
            raise IncompleteObjectError("Create", site.__class__.__name__, "site_name has to be provided")


@dataclass
class UpdateRequest:

    site: SitePayload

    @classmethod
    def from_site(cls, site: Site):
        return cls(site=SitePayload.from_site(site))


@dataclass()
class DeleteResponse:
    """Currently site delete response carries no body data just http code 204 for succcess"""
