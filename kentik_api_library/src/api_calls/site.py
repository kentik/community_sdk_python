# Local application imports
from api_calls.api_call_decorators import get, post, put, delete, payload_type
from api_calls.api_call import APICall


@get
def get_sites() -> APICall:
    """Returns an array of sites objects that each contain information about an individual site."""
    return APICall("/sites")

@get
def get_site_info(site_id: int) -> APICall:
    """Returns a site object containing information about an individual site"""
    url_path = f"/site/{site_id}"
    return APICall(url_path)

@post
@payload_type(dict)
def create_site() -> APICall:
    """Creates and returns a site object containing information about an individual site"""
    return APICall("/site")

@put
@payload_type(dict)
def update_site(site_id: int) -> APICall:
    """Updates and returns a site object containing information about an individual site"""
    url_path = f"/site/{site_id}"
    return APICall(url_path)

@delete
def delete_site(site_id: int) -> APICall:
    """Deletes a site."""
    url_path = f"/site/{site_id}"
    return APICall(url_path)
