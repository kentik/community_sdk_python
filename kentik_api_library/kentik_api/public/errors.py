# This is temporary solution until comprehensive error handling is in place


class DataFormatError(Exception):
    """ When KentikAPI HTTP response JSON has field of invalid type """


class DeserializationError(Exception):
    """ When KentikAPI HTTP response JSON deserialization failed because of eg. missing required field or corrupted JSON document """

    def __init__(self, class_name: str, description: str):
        """
        class_name - class that failed to deserialize, eg. _Interface
        description - failure reason, eg. "missing value for field snmp_id"
        """
        msg = f"{class_name}: {description}"
        super(DeserializationError, self).__init__(msg)


class IncompleteObjectError(Exception):
    """ When object to be sent in KentikAPI request is incomplete"""

    def __init__(self, operation_class_name: str, description: str):
        """
        operation_class_name - eg. "Create Interface"
        description - failure reason, eg. "snmp_id is required"
        """
        msg = f"{operation_class_name}: {description}"
        super(IncompleteObjectError, self).__init__(msg)
