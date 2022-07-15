from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from kentik_api.internal.datetime_zulu import from_iso_format_zulu
from kentik_api.public.defaults import DEFAULT_ID
from kentik_api.public.types import ID

# pylint: disable=too-many-instance-attributes


@dataclass
class User:
    # read-write
    username: str
    full_name: str
    email: str
    email_service: bool
    email_product: bool
    role: str = ""

    # read-only
    _company_id: ID = DEFAULT_ID
    _filters: Dict = field(default_factory=dict)
    _saved_filters: List = field(default_factory=list)
    _id: ID = DEFAULT_ID
    _last_login: str = ""
    _created_date: str = ""
    _updated_date: str = ""

    @classmethod
    def new(
        cls,
        username: str,
        full_name: str,
        user_email: str,
        email_service: bool,
        email_product: bool,
        role: str = "",
    ):
        return cls(
            username=username,
            full_name=full_name,
            email=user_email,
            email_service=email_service,
            email_product=email_product,
            role=role,
        )

    @property
    def company_id(self) -> ID:
        return self._company_id

    @property
    def filters(self) -> Dict:
        return self._filters

    @property
    def saved_filters(self) -> List:
        return self._saved_filters

    @property
    def id(self) -> ID:
        return self._id

    @property
    def last_login(self) -> Optional[datetime]:
        return from_iso_format_zulu(self._last_login) if self._last_login else None

    @property
    def created_date(self) -> Optional[datetime]:
        return from_iso_format_zulu(self._created_date) if self._created_date else None

    @property
    def updated_date(self) -> Optional[datetime]:
        return from_iso_format_zulu(self._updated_date) if self._updated_date else None


# pylint: enable=too-many-instance-attributes
