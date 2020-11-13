# Local application imports
from queries.query_decorators import get, post, put, delete, payload_type
from queries.query import Query


@get
def get_tenants() -> Query:
    """Returns an array of tenants, each of which contains information about an individual tenant."""
    return Query("/mykentik/tenants")

@get
def get_tenant_info(tenant_id: int) -> Query:
    """Returns a tenant object containing information about an individual tenant"""
    url_path = f"/mykentik/tenant/{tenant_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_tenant_user(tenant_id: int) -> Query:
    """Creates and returns a tenant user object containing information about an individual tenant user"""
    return Query("/mykentik/tenant/{tenant_id}/user")

@delete
def delete_tenant_user(tenant_id: int, user_id: int) -> Query:
    """Deletes a tenant user from the system"""
    url_path = f"/mykentik/tenant/{tenant_id}/user/{user_id}"
    return Query(url_path)
