from typing import List, Optional

from kentik_api.public.types import ID


class TenantUser:
    def __init__(
        self,
        id: ID,
        user_email: str,
        tenant_id: ID,
        company_id: ID,
        last_login: Optional[str] = None,
        user_name: Optional[str] = None,
        user_full_name: Optional[str] = None,
    ) -> None:
        self.id = id
        self.email = user_email
        self.last_login = last_login
        self.tenant_id = tenant_id
        self.company_id = company_id
        self.name = user_name
        self.fullname = user_full_name


class Tenant:
    def __init__(
        self,
        id: ID,
        users: List[TenantUser],
        created_date: str,
        updated_date: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.id = id
        self.company_id = users[0].company_id if len(users) > 0 else None
        self.name = name
        self.description = description
        self.created_date = created_date
        self.updated_date = updated_date
        self.users = users
