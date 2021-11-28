# Local application imports
from kentik_api.api_calls.api_call import APICall, ResourceID
from kentik_api.api_calls.api_call_decorators import delete, get, payload_type, post


@get
def get_tenants() -> APICall:
    """Returns an array of tenants, each of which contains
    information about an individual tenant."""
    return APICall("/mykentik/tenants")


@get
def get_tenant_info(tenant_id: ResourceID) -> APICall:
    """Returns a tenant object containing information about an individual tenant"""
    url_path = f"/mykentik/tenant/{tenant_id}"
    return APICall(url_path)


@post
@payload_type(dict)
def create_tenant_user(tenant_id: ResourceID) -> APICall:
    """Creates and returns a tenant user object containing
    information about an individual tenant user"""
    url_path = f"/mykentik/tenant/{tenant_id}/user"
    return APICall(url_path)


@delete
def delete_tenant_user(tenant_id: ResourceID, user_id: ResourceID) -> APICall:
    """Deletes a tenant user from the system"""
    url_path = f"/mykentik/tenant/{tenant_id}/user/{user_id}"
    return APICall(url_path)
