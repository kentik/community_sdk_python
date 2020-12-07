# Local application imports
from api_calls.api_call_decorators import get, post, put, delete, payload_type
from api_calls.api_call import APICall


@get
def get_users() -> APICall:
    """Returns an array of users objects that each contain information about an individual user."""
    return APICall("/users")


@get
def get_user_info(user_id: int) -> APICall:
    """Returns a user object containing information about an individual user"""
    url_path = f"/user/{user_id}"
    return APICall(url_path)


@post
@payload_type(dict)
def create_user() -> APICall:
    """Creates and returns a user object containing information about an individual user"""
    return APICall("/user")


@put
@payload_type(dict)
def update_user(user_id: int) -> APICall:
    """Updates and returns a user object containing information about an individual user"""
    url_path = f"/user/{user_id}"
    return APICall(url_path)


@delete
def delete_user(user_id: int) -> APICall:
    """Deletes a user."""
    url_path = f"/user/{user_id}"
    return APICall(url_path)
