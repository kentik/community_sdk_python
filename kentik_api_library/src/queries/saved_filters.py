from .query_decorators import get, post, put, delete, payload_type
from .query import Query


@get
def get_saved_filters() -> Query:
    """Returns an array of saved-filters objects that each contain information about an individual saved-filter."""
    return Query("/saved-filters/custom")

@get
def get_saved_filter_info(saved_filter_id: int) -> Query:
    """Returns a saved-filter object containing information about an individual saved-filter"""
    url_path = f"/saved-filter/custom/{saved_filter_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_saved_filter() -> Query:
    """Creates and returns a saved-filter object containing information about an individual saved-filter"""
    return Query("/saved-filter/custom")

@put
@payload_type(dict)
def update_saved_filter(saved_filter_id: int) -> Query:
    """Updates and returns a saved-filter object containing information about an individual saved-filter"""
    url_path = f"/saved-filter/custom/{saved_filter_id}"
    return Query(url_path)

@delete
def delete_saved_filter(saved_filter_id: int) -> Query:
    """Deletes a saved-filter."""
    url_path = f"/saved-filter/custom/{saved_filter_id}"
    return Query(url_path)
