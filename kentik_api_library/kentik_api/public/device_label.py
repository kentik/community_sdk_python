from typing import List, Optional, overload
from dataclasses import dataclass

from kentik_api.public.types import ID
from kentik_api.public.defaults import DEFAULT_ID, DEFAULT_DATE


@dataclass(frozen=True)
class DeviceItem:
    id: ID
    device_name: str
    device_subtype: str
    device_type: Optional[str]


# pylint: disable=too-many-instance-attributes


class DeviceLabel:
    # pylint: disable=too-many-arguments

    @overload
    def __init__(self, name: str, color: str) -> None:
        """ Create """
        ...

    @overload
    def __init__(self, id: ID, name: str, color: str) -> None:
        """ Update """
        ...

    @overload
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
        """ Library-internal use """
        ...

    def __init__(self, *args, **kwargs) -> None:
        """ This constructor covers all the overloads """

        if len(args) > 0:
            raise RuntimeError(f"DeviceLabel() supports only named argumets, got positional: {args}")

        # read-write
        self.name = kwargs["name"]
        self.color = kwargs["color"]

        # read-only
        self._id = kwargs.get("id", DEFAULT_ID)
        self._user_id = kwargs.get("user_id", DEFAULT_ID)
        self._company_id = kwargs.get("company_id", DEFAULT_ID)
        self._devices: List[DeviceItem] = kwargs.get("devices", [])
        self._created_date = kwargs.get("created_date", DEFAULT_DATE)
        self._updated_date = kwargs.get("updated_date", DEFAULT_DATE)

    # pylint: enable=too-many-arguments

    @property
    def id(self) -> ID:
        return self._id

    @property
    def user_id(self) -> ID:
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
