from typing import List, Any, Optional
from dataclasses import dataclass

from kentik_api.public.types import ID


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
        color: Optional[str] = None,
        id: Optional[ID] = None,
        user_id: Optional[ID] = None,
        company_id: Optional[ID] = None,
        devices: Optional[List[DeviceItem]] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
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

    @property
    def id(self) -> ID:
        assert self._id is not None
        return self._id

    @property
    def user_id(self) -> Optional[ID]:
        return self._user_id

    @property
    def company_id(self) -> Optional[ID]:
        return self._company_id

    @property
    def devices(self) -> List[DeviceItem]:
        return [] if self._devices is None else self._devices

    @property
    def created_date(self) -> Optional[str]:
        return self._created_date

    @property
    def updated_date(self) -> Optional[str]:
        return self._updated_date


# pylint: enable=too-many-instance-attributes
