import json
from typing import List, Any
from dataclasses import dataclass

from kentik_api.public.types import ID
from kentik_api.public.custom_dimension import CustomDimension
from kentik_api.requests_payload.conversions import convert
from kentik_api.requests_payload.populators_payload import PopulatorArray


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
        dic = json.loads(json_string)["customDimension"]  # payload is embeded under "customDimension" key
        dic["populators"] = PopulatorArray.from_list(dic["populators"])
        return cls(**dic)

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
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        dimensions = cls()
        for item in dic["customDimensions"]:  # payload is embeded under "customDimensions" key
            d = GetResponse(
                name=item["name"],
                display_name=item["display_name"],
                type=item["type"],
                populators=PopulatorArray.from_list(item["populators"]),
                id=item["id"],
                company_id=item["company_id"],
            )
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
