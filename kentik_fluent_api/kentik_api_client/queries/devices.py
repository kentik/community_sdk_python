from query_annotations import get, post, put, delete, data


@get
def get_devices(self):
    """Returns an array of device objects that each contain information about an individual device."""
    pass

@get
def get_device_info(self, device_id: int):
    """Returns a device object containing information about an individual device"""
    pass

@post
@data
def create_device(self):
    """Creates and returns a device object containing information about an individual device"""
    pass

@put
@data
def update_device(self, device_id: int):
    """Updates and returns a device object containing information about an individual device"""
    pass

@put
@data
def apply_device_labels(self, device_id: int):
    """Removes all existing labels from the device and applies the device labels (see About Device Labels) specified
     by id. Returns a reduced version of device object containing an array of the applied labels."""
    pass

@delete
def delete_device(self, device_id: int):
    """Deletes a device."""
    pass

@get
def get_device_interfaces(self, interface_id: int):
    """Returns an array of interface objects that each contain information about an interface
     from a specified device."""
    pass

@get
def get_device_interface_info(self, interface_id: int):
    """Returns a interface object containing information about an individual interface from a given device."""
    pass

@post
@data
def create_interface(self, device_id: int):
    """Creates and returns an interface object containing information about an individual interface
     for a given device."""
    pass

@put
@data
def update_interface(self, device_id: int):
    """Updates and returns an interface object containing information about an individual interface
     from a specified device."""
    pass


@delete
def delete_interfaces(self, device_id: int):
    """Deletes an interface from a given device."""
    pass
