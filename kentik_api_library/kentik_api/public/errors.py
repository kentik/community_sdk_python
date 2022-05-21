class KentikAPIError(Exception):
    """KentikAPIError is a base class for all Kentik API library exceptions."""


class ProtocolError(KentikAPIError):
    """ProtocolError is raised when Kentik API returns response with specific error code."""

    def __init__(self, protocol: str, status_code: int, message: str):
        self._protocol = protocol
        self._status_code = status_code
        super().__init__(message)

    @property
    def protocol(self) -> str:
        """Protocol returns the application protocol of returned API response, e.g. HTTP."""
        return self._protocol

    @property
    def status_code(self) -> int:
        """Status_code returns error status code returned by the API, e.g. 418."""
        return self._status_code


class AuthError(ProtocolError):
    """AuthError is raised when authentication or authorization fails.
    It is raised on HTTP 401 Unauthorized and HTTP 403 Forbidden API responses."""


class BadRequestError(ProtocolError):
    """BadRequestError is raised when Kentik API indicates that provided request data is incorrect.
    It is raised on HTTP 400 Bad Request API response."""


class DataFormatError(KentikAPIError):
    """DataFormatError is raised when Kentik API HTTP response JSON has a field of invalid type."""


class DeserializationError(KentikAPIError):
    """DeserializationError is raised when Kentik API HTTP/GRPC response deserialization failed
    because of e.g. missing required field or corrupted JSON document."""

    def __init__(self, class_name: str, description: str):
        """
        class_name - class that failed to deserialize, e.g. _Interface
        description - failure reason, e.g. "missing value for the field snmp_id"
        """
        msg = f"{class_name}: {description}"
        super(DeserializationError, self).__init__(msg)


class IncompleteObjectError(KentikAPIError):
    """IncompleteObjectError is raised when object to be sent in Kentik API request is incomplete."""

    def __init__(self, operation: str, class_name: str, description: str):
        """
        operation - e.g. "Create"
        class_name - e.g. "Interface"
        description - failure reason, e.g. "snmp_id is required"
        """
        msg = f"{operation} {class_name}: {description}"
        super(IncompleteObjectError, self).__init__(msg)


class IntermittentError(KentikAPIError):
    """IntermittentError is base error for all intermittent errors, such as timeouts.
    Retrying operations which caused IntermittentError might succeed."""


class NotFoundError(ProtocolError):
    """NotFoundError is raised when requested resource is not found.
    It is raised on HTTP 404 Not Found API response."""


class RateLimitExceededError(ProtocolError, IntermittentError):
    """RateLimitExceededError is raised when the user has sent too many requests in a given amount of time.
    It is raised on HTTP 429 Too Many Requests API response."""


class TimedOutError(IntermittentError):
    """TimedOutError is raised when there has been a request time out."""


class UnavailabilityError(ProtocolError, IntermittentError):
    """UnavailabilityError is raised when the Kentik API is unavailable.
    It is raised on HTTP 503 Service Unavailable and 504 Gateway Timeout API responses"""
