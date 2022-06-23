# Standard library imports
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.device_label import DeviceItem, DeviceLabel
from kentik_api.public.types import ID

# Local imports
from kentik_api.requests_payload.conversions import convert, convert_or_none, dict_from_json, from_dict, list_from_json


@dataclass()
class _Device:
    id: str
    device_name: str
    device_subtype: str
    device_type: Optional[str] = None

    def to_device_item(self) -> DeviceItem:
        return DeviceItem(
            id=convert(self.id, ID),
            device_name=self.device_name,
            device_subtype=self.device_subtype,
            device_type=self.device_type,
        )


class _DeviceArray(List[_Device]):
    @classmethod
    def from_list(cls, items: List[Dict[str, Any]]):
        devices = cls()
        for item in items:
            d = from_dict(_Device, item)
            devices.append(d)
        return devices

    def to_device_items(self) -> List[DeviceItem]:
        return [d.to_device_item() for d in self]


# pylint: disable=too-many-instance-attributes


@dataclass()
class GetResponse:
    id: int
    name: str
    color: str
    user_id: Optional[str]
    company_id: str
    devices: _DeviceArray
    created_date: str
    updated_date: str
    order: Optional[int] = None

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string)
        dic["devices"] = _DeviceArray.from_list(dic["devices"])
        return from_dict(cls, dic)

    def to_device_label(self) -> DeviceLabel:
        return DeviceLabel(
            name=self.name,
            color=self.color,
            _id=convert(self.id, ID),
            _user_id=convert_or_none(self.user_id, ID),
            _company_id=convert(self.company_id, ID),
            _devices=self.devices.to_device_items(),
            _created_date=self.created_date,
            _updated_date=self.updated_date,
        )


# pylint: enable=too-many-instance-attributes


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string)
        labels = cls()
        for item in items:
            item["devices"] = _DeviceArray.from_list(item["devices"])
            labels.append(from_dict(GetResponse, item))
        return labels

    def to_device_labels(self) -> List[DeviceLabel]:
        return [label.to_device_label() for label in self]


@dataclass()
class CreateRequest:
    name: str  # eg. "apitest-label-1"
    color: str  # eg. "#00FF00"


CreateResponse = GetResponse


@dataclass()
class UpdateRequest:
    name: str
    color: Optional[str] = None


UpdateResponse = GetResponse


@dataclass()
class DeleteResponse:
    success: bool

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, dic)
