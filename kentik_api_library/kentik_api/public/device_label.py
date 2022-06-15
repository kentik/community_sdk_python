from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from kentik_api.internal.datetime_zulu import from_iso_format_zulu
from kentik_api.public.defaults import DEFAULT_ID
from kentik_api.public.types import ID


@dataclass(frozen=True)
class DeviceItem:
    id: ID
    device_name: str
    device_subtype: str
    device_type: Optional[str]


# pylint: disable=too-many-instance-attributes


@dataclass
class DeviceLabel:
    # read-write
    name: str
    color: str

    # read-only
    _devices: List[DeviceItem] = field(default_factory=list)
    _id: ID = DEFAULT_ID
    _user_id: Optional[ID] = DEFAULT_ID
    _company_id: ID = DEFAULT_ID
    _created_date: str = ""
    _updated_date: str = ""

    @classmethod
    def new(cls, name: str, color: str):
        return cls(name=name, color=color)

    @property
    def id(self) -> ID:
        return self._id

    @property
    def user_id(self) -> Optional[ID]:
        return self._user_id

    @property
    def company_id(self) -> ID:
        return self._company_id

    @property
    def devices(self) -> List[DeviceItem]:
        return self._devices

    @property
    def created_date(self) -> Optional[datetime]:
        return from_iso_format_zulu(self._created_date) if self._created_date else None

    @property
    def updated_date(self) -> Optional[datetime]:
        return from_iso_format_zulu(self._updated_date) if self._updated_date else None


# pylint: enable=too-many-instance-attributes
