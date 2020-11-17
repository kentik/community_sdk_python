# Local application imports
from api_calls.api_call_decorators import get, post, delete, payload_type
from api_calls.api_call import APICall


@get
def get_tenants() -> APICall:
    """Returns an array of tenants, each of which contains information about an individual tenant."""
    return APICall("/mykentik/tenants")

@get
def get_tenant_info(tenant_id: int) -> APICall:
    """Returns a tenant object containing information about an individual tenant"""
    url_path = f"/mykentik/tenant/{tenant_id}"
    return APICall(url_path)

@post
@payload_type(dict)
def create_tenant_user(tenant_id: int) -> APICall:
    """Creates and returns a tenant user object containing information about an individual tenant user"""
    return APICall(f"/mykentik/tenant/{tenant_id}/user")

@delete
def delete_tenant_user(tenant_id: int, user_id: int) -> APICall:
    """Deletes a tenant user from the system"""
    url_path = f"/mykentik/tenant/{tenant_id}/user/{user_id}"
    return APICall(url_path)
