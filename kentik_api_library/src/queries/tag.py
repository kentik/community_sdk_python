# Local application imports
from queries.query_decorators import get, post, put, delete, payload_type
from queries.query import Query


@get
def get_tags() -> Query:
    """Returns an array of tags objects that each contain information about an individual tag."""
    return Query("/tags")

@get
def get_tag_info(tag_id: int) -> Query:
    """Returns a tag object containing information about an individual tag"""
    url_path = f"/tag/{tag_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_tag() -> Query:
    """Creates and returns a tag object containing information about an individual tag"""
    return Query("/tag")

@put
@payload_type(dict)
def update_tag(tag_id: int) -> Query:
    """Updates and returns a tag object containing information about an individual tag"""
    url_path = f"/tag/{tag_id}"
    return Query(url_path)

@delete
def delete_tag(tag_id: int) -> Query:
    """Deletes a tag."""
    url_path = f"/tag/{tag_id}"
    return Query(url_path)
