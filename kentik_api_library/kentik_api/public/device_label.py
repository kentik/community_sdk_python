from typing import List, Optional
from dataclasses import dataclass

from kentik_api.public.types import ID
from kentik_api.public.defaults import DEFAULT_ID, DEFAULT_DATE


@dataclass
class DeviceItem:

    id: ID
    device_name: str
    device_subtype: str
    device_type: Optional[str]


# pylint: disable=too-many-instance-attributes


class DeviceLabel:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name: str,
        color: str,
        devices: List[DeviceItem],
        id: ID,
        user_id: ID,
        company_id: ID,
        created_date: str,
        updated_date: str,
    ) -> None:
        # read-write
        self.name = name
        self.color = color

        # read-only
        self._id = id
        self._user_id = user_id
        self._company_id = company_id
        self._devices = devices
        self._created_date = created_date
        self._updated_date = updated_date

    # pylint: enable=too-many-arguments

    @classmethod
    def new(cls, name: str, color: str):
        return cls(
            name=name,
            color=color,
            devices=[],
            id=DEFAULT_ID,
            user_id=DEFAULT_ID,
            company_id=DEFAULT_ID,
            created_date=DEFAULT_DATE,
            updated_date=DEFAULT_DATE,
        )

    @classmethod
    def update(cls, id: ID, name: str, color: str):
        return cls(
            name=name,
            color=color,
            devices=[],
            id=id,
            user_id=DEFAULT_ID,
            company_id=DEFAULT_ID,
            created_date=DEFAULT_DATE,
            updated_date=DEFAULT_DATE,
        )

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
        return [] if self._devices is None else self._devices

    @property
    def created_date(self) -> str:
        return self._created_date

    @property
    def updated_date(self) -> str:
        return self._updated_date


# pylint: enable=too-many-instance-attributes
