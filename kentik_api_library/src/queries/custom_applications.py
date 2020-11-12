# Local application imports
from queries.query_decorators import get, post, put, delete, payload_type
from queries.query import Query


@get
def get_custom_applications() -> Query:
    """Returns an array of customApplication objects that each contain information about an individual customApplication."""
    return Query("/customApplications")

@post
@payload_type(dict)
def create_custom_application() -> Query:
    """Creates and returns a custocustomApplicationm_application object containing information about an individual custom_appcustomApplicationlication"""
    return Query("/customApplications")

@put
@payload_type(dict)
def update_custom_application(custom_application_id: int) -> Query:
    """Updates and returns a customApplication object containing information about an individual customApplication"""
    url_path = f"/customApplications/{custom_application_id}"
    return Query(url_path)

@delete
def delete_custom_application(custom_application_id: int) -> Query:
    """Deletes a customApplication."""
    url_path = f"/customApplications/{custom_application_id}"
    return Query(url_path)
