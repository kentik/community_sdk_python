from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.tenant import Tenant, TenantUser
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import convert, dict_from_json, from_dict, list_from_json


def tenant_user_from_dict(dic: Dict[str, Any]) -> TenantUser:
    return TenantUser(
        id=convert(dic["id"], ID),
        user_email=dic["user_email"],
        tenant_id=convert(dic["tenant_id"], ID),
        company_id=convert(dic["company_id"], ID),
        last_login=dic.get("last_login"),
        user_name=dic.get("user_name"),
        user_full_name=dic.get("user_full_name"),
    )


@dataclass()
class GetResponse:
    id: int
    name: str
    description: str
    users: List[Dict[str, Any]]
    created_date: str
    updated_date: str

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, dic)

    def to_tenant(self) -> Tenant:
        users = [tenant_user_from_dict(i) for i in self.users]
        return Tenant(
            id=convert(self.id, ID),
            users=users,
            created_date=self.created_date,
            updated_date=self.updated_date,
            name=self.name,
            description=self.description,
        )


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(cls.__name__, json_string)
        tenants = cls()
        for item in items:
            tenant = from_dict(GetResponse, item)
            tenants.append(tenant)
        return tenants

    def to_tenants(self) -> List[Tenant]:
        return [t.to_tenant() for t in self]


class CreateUserRequest:
    def __init__(self, email: str) -> None:
        self.user = {"user_email": email}


@dataclass()
class CreateUserResponse:
    id: str
    company_id: str
    user_email: str
    tenant_id: str
    last_login: Optional[str] = None
    user_name: Optional[str] = None
    user_full_name: Optional[str] = None

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, dic)

    def to_tenant_user(self):
        return TenantUser(
            id=convert(self.id, ID),
            tenant_id=convert(self.tenant_id, ID),
            company_id=convert(self.company_id, ID),
            user_email=self.user_email,
            last_login=self.last_login,
            user_name=self.user_name,
            user_full_name=self.user_full_name,
        )
