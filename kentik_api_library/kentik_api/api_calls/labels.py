# Local application imports
from kentik_api.api_calls.api_call_decorators import get, post, put, delete, payload_type
from kentik_api.api_calls.api_call import APICall


@get
def get_labels() -> APICall:
    """Returns an array of device label objects that each
    contain information about an individual label."""
    return APICall("/deviceLabels")


@get
def get_label_info(label_id: int) -> APICall:
    """Returns a label object containing
    information about an individual label"""
    url_path = f"/deviceLabels/{label_id}"
    return APICall(url_path)


@post
@payload_type(dict)
def create_label() -> APICall:
    """Creates and returns a label object
    containing information about an individual label"""
    return APICall("/deviceLabels")


@put
@payload_type(dict)
def update_label(label_id: int) -> APICall:
    """Updates and returns a label object containing information about an individual label"""
    url_path = f"/deviceLabels/{label_id}"
    return APICall(url_path)


@delete
def delete_label(label_id: int) -> APICall:
    """Deletes a label."""
    url_path = f"/deviceLabels/{label_id}"
    return APICall(url_path)
