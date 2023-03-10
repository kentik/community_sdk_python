from dataclasses import dataclass
from typing import List, Optional

from kentik_api.public.custom_dimension import CustomDimension
from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, dict_from_json, from_dict, list_from_json
from kentik_api.requests_payload.populators_payload import PopulatorArray


@dataclass
class CustomDimensionPayload:
    """This data structure represents JSON CustomDimension payload as it is transmitted to and from Kentik API"""

    name: Optional[str] = None
    display_name: Optional[str] = None
    type: Optional[str] = None

    @classmethod
    def from_custom_dimension(cls, custom_dimension: CustomDimension):
        return cls(
            name=custom_dimension.name,
            display_name=custom_dimension.display_name,
            type=custom_dimension.type,
        )


@dataclass
class GetResponse:
    name: str
    display_name: str
    type: str
    populators: PopulatorArray
    id: int
    company_id: str

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(
            cls.__name__, json_string, "customDimension"
        )  # payload is embeded under "customDimension" key
        dic["populators"] = PopulatorArray.from_list(dic["populators"])
        return from_dict(cls, dic)

    def to_custom_dimension(self) -> CustomDimension:
        return CustomDimension(
            name=self.name,
            display_name=self.display_name,
            type=self.type,
            populators=self.populators.to_populators(),
            id=convert(self.id, ID),
            company_id=convert(self.company_id, ID),
        )


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string: str):
        # payload is embeded under "customDimensions" key
        items = list_from_json(cls.__name__, json_string, "customDimensions")
        dimensions = cls()
        for dic in items:
            dic["populators"] = PopulatorArray.from_list(dic["populators"])
            d = from_dict(GetResponse, dic)
            dimensions.append(d)
        return dimensions

    def to_custom_dimensions(self) -> List[CustomDimension]:
        return [d.to_custom_dimension() for d in self]


@dataclass
class CreateRequest:

    custom_dimension: CustomDimensionPayload

    @classmethod
    def from_custom_dimension(cls, custom_dimension: CustomDimension):
        validate(custom_dimension, "Create")
        return CustomDimensionPayload.from_custom_dimension(custom_dimension)


CreateResponse = GetResponse


@dataclass
class UpdateRequest:

    custom_dimension: CustomDimensionPayload

    @classmethod
    def from_custom_dimension(cls, custom_dimension: CustomDimension):
        validate(custom_dimension, "Update")
        return CustomDimensionPayload.from_custom_dimension(custom_dimension)


UpdateResponse = GetResponse


def validate(custom_dimension: CustomDimension, operation: str):
    if operation == "Create":
        if custom_dimension.name is None:
            raise IncompleteObjectError(operation, custom_dimension.__class__.__name__, "name is required")
        if custom_dimension.type is None:
            raise IncompleteObjectError(operation, custom_dimension.__class__.__name__, "type is required")
    if custom_dimension.display_name is None:
        raise IncompleteObjectError(operation, custom_dimension.__class__.__name__, "display_name is required")


# @dataclass()
# class DeleteResponse:
#     """ Currently custom dimension delete response carries no body data just http code 204 for succcess """
