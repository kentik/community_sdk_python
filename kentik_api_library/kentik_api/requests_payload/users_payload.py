import json
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

from kentik_api.public.user import User


@dataclass()
class GetResponse:

    id: int
    username: str
    user_full_name: str
    user_email: str
    role: str
    email_service: bool
    email_product: bool
    last_login: str
    created_date: str
    updated_date: str
    company_id: int
    user_api_token: Optional[str]
    filters: Dict
    saved_filters: List

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)['user']
        return cls(**dic)

    def to_user(self) -> User:
        return User(id=self.id,
                    username=self.username,
                    full_name=self.user_full_name,
                    email=self.user_email,
                    role=self.role,
                    email_service=self.email_service,
                    email_product=self.email_product,
                    last_login=self.last_login,
                    created_date=self.created_date,
                    updated_date=self.updated_date,
                    company_id=self.company_id,
                    api_token=self.user_api_token,
                    filters=self.filters,
                    saved_filters=self.saved_filters,
                    )


class GetAllResponse(List[GetResponse]):

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        users = cls()
        for item in dic['users']:
            user = GetResponse(**item)
            users.append(user)
        return users

    def to_users(self) -> List[GetResponse]:
        return [user.to_user() for user in self]


@dataclass()
class CreateRequest:

    user_name: str
    user_full_name: str
    user_email: str
    user_password: str
    role: str
    email_service: bool
    email_product: bool


# Create response and Update response are exactly the same as Get response
CreateResponse = GetResponse
UpdateResponse = GetResponse


@dataclass()
class UpdateRequest:

    def __init__(self,
                 username: Optional[str] = None,
                 full_name: Optional[str] = None,
                 email: Optional[str] = None,
                 role: Optional[str] = None,
                 email_service: Optional[bool] = None,
                 email_product: Optional[bool] = None,
                 _id: Optional[int] = None,
                 last_login: Optional[str] = None,
                 created_date: Optional[str] = None,
                 updated_date: Optional[str] = None,
                 company_id: Optional[int] = None,
                 api_token: Optional[str] = None,
                 filters: Optional[Dict] = None,
                 saved_filters: Optional[List] = None,
                 ) -> None:
        self.id = _id
        self.user_name = username
        self.user_full_name = full_name
        self.user_email = email
        self.role = role
        self.email_service = email_service
        self.email_product = email_product
        self.last_login = last_login
        self.created_date = created_date
        self.updated_date = updated_date
        self.company_id = company_id
        self.user_api_token = api_token
        self.filters = filters
        self.saved_filters = saved_filters
