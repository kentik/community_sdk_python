from .query_decorators import get, post, put, delete, payload_type
from .query import Query


@get
def get_device_labels() -> Query:
    """Returns an array of device_labels objects that each contain information about an individual device_label."""
    return Query("/deviceLabels")

@get
def get_device_label_info(device_label_id: int) -> Query:
    """Returns a device_label object containing information about an individual device_label"""
    url_path = f"/deviceLabels/{device_label_id}"
    return Query(url_path)

@post
@payload_type(dict)
def create_device_label() -> Query:
    """Creates and returns a device_label object containing information about an individual device_label"""
    return Query("/deviceLabels")

@put
@payload_type(dict)
def update_device_label(device_label_id: int) -> Query:
    """Updates and returns a device_label object containing information about an individual device_label"""
    url_path = f"/deviceLabels/{device_label_id}"
    return Query(url_path)

@delete
def delete_device_label(device_label_id: int) -> Query:
    """Deletes a device_label."""
    url_path = f"/deviceLabels/{device_label_id}"
    return Query(url_path)
