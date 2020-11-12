# Local application imports
from .query_decorators import get, post, put, delete, payload_type
from .query import Query


@get
def get_users() -> Query:
    """Returns an array of users objects that each contain information about an individual user."""
    return Query("/users")

@get
def get_user_info(user_id: int) -> Query:
    """Returns a user object containing information about an individual user"""
    url_path = f"/user/{user_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_user() -> Query:
    """Creates and returns a user object containing information about an individual user"""
    return Query("/user")

@put
@payload_type(dict)
def update_user(user_id: int) -> Query:
    """Updates and returns a user object containing information about an individual user"""
    url_path = f"/user/{user_id}"
    return Query(url_path)

@delete
def delete_user(user_id: int) -> Query:
    """Deletes a user."""
    url_path = f"/user/{user_id}"
    return Query(url_path)
