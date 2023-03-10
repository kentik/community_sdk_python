from dataclasses import dataclass
from typing import List, Optional

from kentik_api.public.custom_application import CustomApplication
from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, convert_or_none, dict_from_json, from_dict, list_from_json

# pylint: disable=too-many-instance-attributes


@dataclass
class CustomApplicationPayload:
    """This data structure represents JSON CustomApplication payload as it is transmitted to and from Kentik API"""

    name: Optional[str] = None
    description: Optional[str] = None
    ip_range: Optional[str] = None
    protocol: Optional[str] = None
    port: Optional[str] = None
    asn: Optional[str] = None

    @classmethod
    def from_custom_application(cls, custom_application: CustomApplication):
        return cls(
            name=custom_application.name,
            description=custom_application.description,
            ip_range=custom_application.ip_range,
            protocol=custom_application.protocol,
            port=custom_application.port,
            asn=custom_application.asn,
        )


@dataclass
class GetResponse:
    name: str
    description: str
    ip_range: str
    protocol: str
    port: str
    asn: str
    id: int
    company_id: str
    user_id: Optional[str] = None  # yes API happens to return user_id = null
    cdate: Optional[str] = None
    edate: Optional[str] = None

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, dic)

    def to_custom_application(self) -> CustomApplication:
        return CustomApplication(
            name=self.name,
            description=self.description,
            ip_range=self.ip_range,
            protocol=self.protocol,
            port=self.port,
            asn=self.asn,
            id=convert(self.id, ID),
            company_id=convert(self.company_id, ID),
            user_id=convert_or_none(self.user_id, ID),
            created_date=self.cdate,
            updated_date=self.edate,
        )


# pylint: enable=too-many-instance-attributes


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string: str):
        data = list_from_json(cls.__name__, json_string)
        apps = cls()
        for item in data:
            a = from_dict(GetResponse, item)
            apps.append(a)
        return apps

    def to_custom_applications(self) -> List[CustomApplication]:
        return [a.to_custom_application() for a in self]


@dataclass
class CreateRequest:

    custom_application: CustomApplicationPayload

    @classmethod
    def from_custom_application(cls, custom_application: CustomApplication):
        CreateRequest.validate(custom_application)
        return CustomApplicationPayload.from_custom_application(custom_application)

    @staticmethod
    def validate(custom_application: CustomApplication) -> None:
        if custom_application.name is None:
            raise IncompleteObjectError("Create", custom_application.__class__.__name__, "name is required")


CreateResponse = GetResponse


@dataclass
class UpdateRequest:

    custom_application: CustomApplicationPayload

    @classmethod
    def from_custom_application(cls, custom_application: CustomApplication):
        return CustomApplicationPayload.from_custom_application(custom_application)


UpdateResponse = GetResponse


# @dataclass()
# class DeleteResponse:
#     """ Currently custom application delete response carries no body data just http code 204 for succcess """
