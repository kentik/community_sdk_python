import json
from typing import List, Any
from dataclasses import dataclass

from kentik_api.public.custom_dimension import CustomDimension


@dataclass
class GetResponse:
    name: str
    display_name: str
    type: str
    populators: List[Any]
    id: int
    company_id: str

    @classmethod
    def from_json(cls, json_string: str):
        dic = json.loads(json_string)
        return cls(**dic["customDimension"])  # payload is embeded under "customDimension" key

    def to_custom_dimension(self) -> CustomDimension:
        return CustomDimension(
            name=self.name,
            display_name=self.display_name,
            type=self.type,
            populators=self.populators,
            id=self.id,
            company_id=self.company_id,
        )


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        dimensions = cls()
        for item in dic["customDimensions"]:  # payload is embeded under "customDimensions" key
            d = GetResponse(**item)
            dimensions.append(d)
        return dimensions

    def to_custom_dimensions(self) -> List[CustomDimension]:
        return [d.to_custom_dimension() for d in self]


@dataclass
class CreateRequest:
    name: str
    display_name: str
    type: str


CreateResponse = GetResponse


@dataclass
class UpdateRequest:
    display_name: str


UpdateResponse = GetResponse


# @dataclass()
# class DeleteResponse:
#     """ Currently custom dimension delete response carries no body data just http code 204 for succcess """
