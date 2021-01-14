from dataclasses import dataclass
import json
from typing import Optional, Dict, List
from kentik_api.public.tenant import Tenant, TenantUser


@dataclass()
class GetResponse:
    id: int
    name: str
    description: str
    users: List[Dict]
    created_date: str
    updated_date: str

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_tenant(self) -> Tenant:
        users = [TenantUser(**i) for i in self.users]
        return Tenant(
            id=self.id,
            users=users,
            created_date=self.created_date,
            updated_date=self.updated_date,
            name=self.name,
            description=self.description,
        )


class GetAllResponse(List[GetResponse]):
    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        tenants = cls()
        for item in dic:
            tenant = GetResponse(**item)
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
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_tenant_user(self):
        return TenantUser(**self.__dict__)
