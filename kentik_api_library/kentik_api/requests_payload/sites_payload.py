import json
from typing import Optional, List
from dataclasses import dataclass

from kentik_api.public.site import Site


@dataclass()
class GetResponse:
    @dataclass
    class _Site:
        id: int
        site_name: str
        lat: Optional[float]
        lon: Optional[float]
        company_id: str

    site: _Site  # sites api payload is embedded under "site" key

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(GetResponse._Site(**dic["site"]))

    # pylint: disable=too-many-arguments
    @classmethod
    def from_fields(cls, id: int, site_name: str, lat: Optional[float], lon: Optional[float], company_id: str):
        return cls(GetResponse._Site(id, site_name, lat, lon, company_id))

    # pylint: enable=too-many-arguments
    def to_site(self) -> Site:
        return Site(self.site.site_name, self.site.lat, self.site.lon, self.site.id, self.site.company_id)


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        sites = cls()
        for item in dic["sites"]:
            s = GetResponse.from_fields(**item)
            sites.append(s)
        return sites

    def to_sites(self) -> List[Site]:
        return [s.to_site() for s in self]


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
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(CreateResponse._Site(**dic["site"]))

    def to_site(self) -> Site:
        return Site(self.site.site_name, self.site.lat, self.site.lon, self.site.id, self.site.company_id)


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
        id: int
        site_name: str
        lat: Optional[float]
        lon: Optional[float]
        company_id: str

    site: _Site  # sites api payload is embedded under "site" key

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(UpdateResponse._Site(**dic["site"]))

    def to_site(self) -> Site:
        return Site(self.site.site_name, self.site.lat, self.site.lon, self.site.id, self.site.company_id)


@dataclass()
class DeleteResponse:
    """ Currently site delete response carries no body data just http code 204 for succcess """
