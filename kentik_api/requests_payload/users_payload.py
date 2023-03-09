from dataclasses import dataclass
from typing import Dict, List, Optional

from kentik_api.public.types import ID
from kentik_api.public.user import User
from kentik_api.requests_payload.conversions import convert, dict_from_json, from_dict, list_from_json

# pylint: disable=too-many-instance-attributes


@dataclass()
class _User:
    id: str
    username: str
    user_full_name: str
    user_email: str
    role: str
    email_service: bool
    email_product: bool
    last_login: Optional[str]
    created_date: str
    updated_date: str
    company_id: str
    filters: Dict
    saved_filters: List

    def to_user(self) -> User:
        return User(
            _id=convert(self.id, ID),
            username=self.username,
            full_name=self.user_full_name,
            email=self.user_email,
            role=self.role,
            email_service=bool(self.email_service),
            email_product=bool(self.email_product),
            _last_login=self.last_login if self.last_login is not None else "",
            _created_date=self.created_date,
            _updated_date=self.updated_date,
            _company_id=convert(self.company_id, ID),
            _filters=dict(self.filters),
            _saved_filters=list(self.saved_filters),
        )


# pylint: enable=too-many-instance-attributes


@dataclass()
class GetResponse:
    user: _User

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string, "user")
        dic["email_service"] = convert(dic["email_service"], bool)
        dic["email_product"] = convert(dic["email_product"], bool)
        return cls(from_dict(_User, dic))

    def to_user(self) -> User:
        return self.user.to_user()


@dataclass()
class GetAllResponse:

    users: List[_User]

    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string, "users")
        response = cls([])
        for item in items:
            user = from_dict(_User, item)
            response.users.append(user)
        return response

    def to_users(self) -> List[User]:
        return [user.to_user() for user in self.users]


@dataclass()
class CreateRequest:
    @dataclass()
    class _CreateData:
        user_name: Optional[str]
        user_full_name: Optional[str]
        user_email: str
        role: str
        email_service: bool
        email_product: bool

    user: _CreateData
    # pylint: disable=too-many-arguments

    def __init__(
        self,
        user_email: str,
        role: str,
        email_service: bool,
        email_product: bool,
        user_name: Optional[str] = None,
        user_full_name: Optional[str] = None,
    ) -> None:
        self.user = CreateRequest._CreateData(user_name, user_full_name, user_email, role, email_service, email_product)

    # pylint: enable=too-many-arguments


# Create response and Update response are exactly the same as Get response
CreateResponse = GetResponse
UpdateResponse = GetResponse


@dataclass()
class UpdateRequest:
    @dataclass()
    class _UpdateData:
        user_name: Optional[str]
        user_full_name: Optional[str]
        user_email: Optional[str]
        role: Optional[str]
        email_service: Optional[bool]
        email_product: Optional[bool]

    user: _UpdateData

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        user_email: Optional[str] = None,
        role: Optional[str] = None,
        email_service: Optional[bool] = None,
        email_product: Optional[bool] = None,
        user_name: Optional[str] = None,
        user_full_name: Optional[str] = None,
    ) -> None:
        self.user = UpdateRequest._UpdateData(user_name, user_full_name, user_email, role, email_service, email_product)

    # pylint: enable=too-many-arguments
