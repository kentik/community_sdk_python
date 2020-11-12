# Local application imports
from queries.query_decorators import get, post, put, delete, payload_type
from queries.query import Query


@get
def get_sites() -> Query:
    """Returns an array of sites objects that each contain information about an individual site."""
    return Query("/sites")

@get
def get_site_info(site_id: int) -> Query:
    """Returns a site object containing information about an individual site"""
    url_path = f"/site/{site_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_site() -> Query:
    """Creates and returns a site object containing information about an individual site"""
    return Query("/site")

@put
@payload_type(dict)
def update_site(site_id: int) -> Query:
    """Updates and returns a site object containing information about an individual site"""
    url_path = f"/site/{site_id}"
    return Query(url_path)

@delete
def delete_site(site_id: int) -> Query:
    """Deletes a site."""
    url_path = f"/site/{site_id}"
    return Query(url_path)
