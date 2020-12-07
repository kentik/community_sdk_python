# Standard library imports
import json
from typing import Optional, List, Any
from dataclasses import dataclass
from kentik_api.public.device_label import DeviceLabel

@dataclass()
class GetResponse:

    id : int
    name: str
    color: str
    user_id: str
    company_id: str
    devices : List[Any]
    created_date : str
    updated_date : str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_device_label(self) -> DeviceLabel:
        return DeviceLabel(self.name, self.color, self.id, self.user_id, self.company_id, self.devices, self.created_date, self.updated_date)




class GetAllResponse(List[GetResponse]):

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        labels = cls()
        for item in dic:
            l = GetResponse(**item)
            labels.append(l)
        return labels

    def to_device_labels(self) -> List[DeviceLabel]:
        return [l.to_device_label() for l in self]


@dataclass()
class CreateRequest:

    name: str # eg. "apitest-label-1"
    color: str # eg. "#00FF00"


@dataclass()
class CreateResponse:

    id : int
    name: str
    color: str
    user_id: str
    company_id: str
    devices : List[Any]
    created_date : str
    updated_date : str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_device_label(self) -> DeviceLabel:
        return DeviceLabel(self.name, self.color, self.id, self.user_id, self.company_id, self.devices, self.created_date, self.updated_date)


@dataclass()
class UpdateRequest:

    name: str
    color: Optional[str] = None


@dataclass()
class UpdateResponse:

    id : int
    name: str
    color: str
    user_id: str
    company_id: str
    devices : List[Any]
    created_date : str
    updated_date : str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_device_label(self) -> DeviceLabel:
        return DeviceLabel(self.name, self.color, self.id, self.user_id, self.company_id, self.devices, self.created_date, self.updated_date)


@dataclass()
class DeleteResponse:

    success: bool

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)
