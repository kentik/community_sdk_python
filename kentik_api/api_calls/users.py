# Local application imports
from kentik_api.api_calls.api_call import APICall, ResourceID
from kentik_api.api_calls.api_call_decorators import delete, get, payload_type, post, put


@get
def get_users() -> APICall:
    """Returns an array of users objects that each contain information about an individual user."""
    return APICall("/users")


@get
def get_user_info(user_id: ResourceID) -> APICall:
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
def update_user(user_id: ResourceID) -> APICall:
    """Updates and returns a user object containing information about an individual user"""
    url_path = f"/user/{user_id}"
    return APICall(url_path)


@delete
def delete_user(user_id: ResourceID) -> APICall:
    """Deletes a user."""
    url_path = f"/user/{user_id}"
    return APICall(url_path)
