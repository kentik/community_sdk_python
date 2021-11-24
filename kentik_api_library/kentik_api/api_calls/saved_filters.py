from kentik_api.api_calls.api_call import APICall, ResourceID
from kentik_api.api_calls.api_call_decorators import delete, get, payload_type, post, put


@get
def get_saved_filters() -> APICall:
    """Returns an array of saved-filters objects
    that each contain information about an individual saved-filter."""
    return APICall("/saved-filters/custom")


@get
def get_saved_filter_info(saved_filter_id: ResourceID) -> APICall:
    """Returns a saved-filter object containing
    information about an individual saved-filter"""
    url_path = f"/saved-filter/custom/{saved_filter_id}"
    return APICall(url_path)


@post
@payload_type(dict)
def create_saved_filter() -> APICall:
    """Creates and returns a saved-filter object containing
    information about an individual saved-filter"""
    return APICall("/saved-filter/custom")


@put
@payload_type(dict)
def update_saved_filter(saved_filter_id: ResourceID) -> APICall:
    """Updates and returns a saved-filter object containing
    information about an individual saved-filter"""
    url_path = f"/saved-filter/custom/{saved_filter_id}"
    return APICall(url_path)


@delete
def delete_saved_filter(saved_filter_id: ResourceID) -> APICall:
    """Deletes a saved-filter."""
    url_path = f"/saved-filter/custom/{saved_filter_id}"
    return APICall(url_path)
