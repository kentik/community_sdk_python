from dataclasses import dataclass, field
from typing import Dict, List

from kentik_api.public.defaults import DEFAULT_DATE, DEFAULT_ID
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
    _last_login: str = DEFAULT_DATE
    _created_date: str = DEFAULT_DATE
    _updated_date: str = DEFAULT_DATE

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
    def last_login(self) -> str:
        return self._last_login

    @property
    def created_date(self) -> str:
        return self._created_date

    @property
    def updated_date(self) -> str:
        return self._updated_date


# pylint: enable=too-many-instance-attributes
