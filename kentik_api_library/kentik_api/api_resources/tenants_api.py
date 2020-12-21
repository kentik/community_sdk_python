from http import HTTPStatus
from typing import List

from kentik_api.api_calls import my_kentik_portal
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.tenant import TenantUser, Tenant
from kentik_api.requests_payload import tenants_payload


class MyKentikPortalAPI(BaseAPI):
    """Exposes Kentik API operations related to My Kentik Portal. """

    def get_all(self) -> List[Tenant]:
        api_call = my_kentik_portal.get_tenants()
        print(api_call)
        response = self._send(api_call)
        print(response)
        return tenants_payload.GetAllResponse.from_json(response.text).to_tenants()

    def get(self, tenant_id: int) -> Tenant:
        api_call = my_kentik_portal.get_tenant_info(tenant_id)
        print(api_call)
        response = self._send(api_call)
        print(response)
        return tenants_payload.GetResponse.from_json(response.text).to_tenant()

    def create_tenant_user(self, tenant_id: int, user_email: str) -> TenantUser:
        api_call = my_kentik_portal.create_tenant_user(tenant_id)
        payload = tenants_payload.CreateUserRequest(email=user_email)
        print(api_call)
        print(payload)
        response = self._send(api_call, payload)
        print(response)
        return tenants_payload.CreateUserResponse.from_json(response.text).to_tenant_user()

    def delete_tenant_user(self, tenant_id: int, user_id: int) -> bool:
        api_call = my_kentik_portal.delete_tenant_user(tenant_id, user_id)
        print(api_call)
        response = self._send(api_call)
        print(response)
        return response.http_status_code == HTTPStatus.NO_CONTENT
