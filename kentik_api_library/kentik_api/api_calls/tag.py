# Local application imports
from api_calls.api_call_decorators import get, post, put, delete, payload_type
from api_calls.api_call import APICall


@get
def get_tags() -> APICall:
    """Returns an array of tags objects that each contain information about an individual tag."""
    return APICall("/tags")


@get
def get_tag_info(tag_id: int) -> APICall:
    """Returns a tag object containing information about an individual tag"""
    url_path = f"/tag/{tag_id}"
    return APICall(url_path)


@post
@payload_type(dict)
def create_tag() -> APICall:
    """Creates and returns a tag object containing information about an individual tag"""
    return APICall("/tag")


@put
@payload_type(dict)
def update_tag(tag_id: int) -> APICall:
    """Updates and returns a tag object containing information about an individual tag"""
    url_path = f"/tag/{tag_id}"
    return APICall(url_path)


@delete
def delete_tag(tag_id: int) -> APICall:
    """Deletes a tag."""
    url_path = f"/tag/{tag_id}"
    return APICall(url_path)
