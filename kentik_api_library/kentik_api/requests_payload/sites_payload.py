from typing import Optional, Any, List, Dict
from dataclasses import dataclass

from kentik_api.requests_payload.conversions import dict_from_json, list_from_json, from_dict, convert
from kentik_api.public.types import ID
from kentik_api.public.site import Site


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


class CreateRequest:
    @dataclass
    class _Site:
        site_name: str  # eg. "apitest-site-1"
        lat: Optional[float]  # eg. 50.102
        lon: Optional[float]  # eg. 18.209

    def __init__(self, site_name: str, lat: Optional[float], lon: Optional[float]) -> None:
        self.site = CreateRequest._Site(site_name, lat, lon)  # sites api payload is embedded under "site" key


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


class UpdateRequest:
    @dataclass
    class _Site:
        site_name: Optional[str]  # eg. "apitest-site-1"
        lat: Optional[float]  # eg. 50.102
        lon: Optional[float]  # eg. 18.201

    def __init__(self, site_name: Optional[str], lat: Optional[float], lon: Optional[float]) -> None:
        self.site = UpdateRequest._Site(site_name, lat, lon)  # sites api payload is embedded under "site" key


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


@dataclass()
class DeleteResponse:
    """Currently site delete response carries no body data just http code 204 for succcess"""
