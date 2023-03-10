# Local application imports
from kentik_api.api_calls.api_call import APICall, ResourceID
from kentik_api.api_calls.api_call_decorators import delete, get, payload_type, post, put


@get
def get_devices() -> APICall:
    """Returns an array of device objects that each
    contain information about an individual device."""
    return APICall("/devices")


@get
def get_device_info(device_id: ResourceID) -> APICall:
    """Returns a device object containing
    information about an individual device"""
    url_path = f"/device/{device_id}"
    return APICall(url_path)


@post
@payload_type(dict)
def create_device() -> APICall:
    """Creates and returns a device object
    containing information about an individual device"""
    return APICall("/device")


@put
@payload_type(dict)
def update_device(device_id: ResourceID) -> APICall:
    """Updates and returns a device object containing information about an individual device"""
    url_path = f"/device/{device_id}"
    return APICall(url_path)


@delete
def delete_device(device_id: ResourceID) -> APICall:
    """Deletes a device."""
    url_path = f"/device/{device_id}"
    return APICall(url_path)


@put
@payload_type(dict)
def apply_device_labels(device_id: ResourceID) -> APICall:
    """Removes all existing labels from the device and
    applies the device labels (see About Device Labels) specified
    by id. Returns a reduced version of device object
    containing an array of the applied labels."""
    url_path = f"/devices/{device_id}/labels"
    return APICall(url_path)


@get
def get_device_interfaces(device_id: ResourceID) -> APICall:
    """Returns an array of interface objects that each contain information about an interface
    from a specified device."""
    url_path = f"/device/{device_id}/interfaces"
    return APICall(url_path)


@get
def get_device_interface_info(device_id: ResourceID, interface_id: ResourceID) -> APICall:
    """Returns a interface object containing information
    about an individual interface from a given device."""
    url_path = f"/device/{device_id}/interface/{interface_id}"
    return APICall(url_path)


@post
@payload_type(dict)
def create_interface(device_id: ResourceID) -> APICall:
    """Creates and returns an interface object containing information about an individual interface
    for a given device."""
    url_path = f"/device/{device_id}/interface"
    return APICall(url_path)


@put
@payload_type(dict)
def update_interface(device_id: ResourceID, interface_id: ResourceID) -> APICall:
    """Updates and returns an interface object containing information about an individual interface
    from a specified device."""
    url_path = f"/device/{device_id}/interface/{interface_id}"
    return APICall(url_path)


@delete
def delete_interface(device_id: ResourceID, interface_id: ResourceID) -> APICall:
    """Deletes an interface from a given device."""
    url_path = f"/device/{device_id}/interface/{interface_id}"
    return APICall(url_path)
