from dataclasses import dataclass
import json
from typing import Optional, Dict, List

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
        dic = json.loads(json_string)
        return cls(**dic['user'])

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

    def to_users(self) -> List[User]:
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

    user_name: Optional[str]
    user_full_name: Optional[str]
    user_email: Optional[str]
    role: Optional[str]
    email_service: Optional[bool]
    email_product: Optional[bool]
    id: Optional[int]
    last_login: Optional[str]
    created_date: Optional[str]
    updated_date: Optional[str]
    company_id: Optional[int]
    user_api_token: Optional[str]
    filters: Optional[Dict]
    saved_filters: Optional[List]
