from typing import Optional

from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.types import ID

# pylint: disable=too-many-instance-attributes


class CustomApplication:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        ip_range: Optional[str] = None,
        protocol: Optional[str] = None,
        port: Optional[str] = None,
        asn: Optional[str] = None,
        id: Optional[ID] = None,
        company_id: Optional[ID] = None,
        user_id: Optional[ID] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
    ) -> None:
        # read-write
        self.name = name
        self.description = description
        self.ip_range = ip_range
        self.protocol = protocol
        self.port = port
        self.asn = asn

        # read-only
        self._id = id
        self._company_id = company_id
        self._user_id = user_id
        self._created_date = created_date
        self._updated_date = updated_date

    # pylint: disable=too-many-arguments

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_id is required")
        return self._id

    @property
    def company_id(self) -> Optional[ID]:
        return self._company_id

    @property
    def user_id(self) -> Optional[ID]:
        return self._user_id

    @property
    def created_date(self) -> Optional[str]:
        return self._created_date

    @property
    def updated_date(self) -> Optional[str]:
        return self._updated_date


# pylint: enable=too-many-instance-attributes
