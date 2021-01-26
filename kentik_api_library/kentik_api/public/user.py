from typing import List, Dict, Optional

from kentik_api.public.types import ID

# pylint: disable=too-many-instance-attributes


class User:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        email_service: Optional[bool] = None,
        email_product: Optional[bool] = None,
        id: Optional[ID] = None,
        password: Optional[str] = None,
        last_login: Optional[str] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        company_id: Optional[ID] = None,
        api_token: Optional[str] = None,
        filters: Optional[Dict] = None,
        saved_filters: Optional[List] = None,
    ) -> None:
        self.username = username
        self.full_name = full_name
        self.email = email
        self.password = password
        self.role = role
        self.email_service = email_service
        self.email_product = email_product
        self.company_id = company_id
        self.api_token = api_token
        self.filters = filters
        self.saved_filters = saved_filters

        self._id = id
        self._last_login = last_login
        self._created_date = created_date
        self._updated_date = updated_date

    # pylint: enable=too-many-arguments
    @property
    def id(self) -> ID:
        assert self._id is not None
        return self._id

    @property
    def last_login(self) -> Optional[str]:
        return self._last_login

    @property
    def created_date(self) -> Optional[str]:
        return self._created_date

    @property
    def updated_date(self) -> Optional[str]:
        return self._updated_date


# pylint: enable=too-many-instance-attributes
