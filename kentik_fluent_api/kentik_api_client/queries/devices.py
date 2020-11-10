from query_decorators import get, post, put, delete, payload_type
from query import Query


@get
def get_devices() -> Query:
    """Returns an array of device objects that each contain information about an individual device."""
    return Query("/devices")


@get
def get_device_info(device_id: int) -> Query:
    """Returns a device object containing information about an individual device"""
    url_path = f"/device/{device_id}"
    return Query(url_path)


@post
@payload_type(dict)
def create_device() -> Query:
    """Creates and returns a device object containing information about an individual device"""
    return Query("/device")


@put
@payload_type(dict)
def update_device(device_id: int) -> Query:
    """Updates and returns a device object containing information about an individual device"""
    url_path = f"/device/{device_id}"
    return Query(url_path)


@delete
def delete_device(device_id: int) -> Query:
    """Deletes a device."""
    url_path = f"/device/{device_id}"
    return Query(url_path)


@put
@payload_type(dict)
def apply_device_labels(device_id: int) -> Query:
    """Removes all existing labels from the device and applies the device labels (see About Device Labels) specified
     by id. Returns a reduced version of device object containing an array of the applied labels."""
    url_path = f"/devices/{device_id}/labels"
    return Query(url_path)


@get
def get_device_interfaces(device_id: int) -> Query:
    """Returns an array of interface objects that each contain information about an interface
     from a specified device."""
    url_path = f"/devices/{device_id}/interfaces"
    return Query(url_path)


@get
def get_device_interface_info(device_id: int, interface_id: int) -> Query:
    """Returns a interface object containing information about an individual interface from a given device."""
    url_path = f"/device/{device_id}/interface/{interface_id}"


@post
@payload_type(dict)
def create_interface(device_id: int) -> Query:
    """Creates and returns an interface object containing information about an individual interface
     for a given device."""
    url_path = f"/device/{device_id}/interface"
    return Query(url_path)


@put
@payload_type(dict)
def update_interface(device_id: int, interface_id: int) -> Query:
    """Updates and returns an interface object containing information about an individual interface
     from a specified device."""
    url_path = f"/device/{device_id}/interface/{interface_id}"
    return Query(url_path)


@delete
def delete_interfaces(device_id: int, interface_id: int) -> Query:
    """Deletes an interface from a given device."""
    url_path = f"/device/{device_id}/interface/{interface_id}"
    return Query(url_path)
