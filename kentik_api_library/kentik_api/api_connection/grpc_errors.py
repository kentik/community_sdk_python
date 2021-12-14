from grpc import RpcError, StatusCode
from grpc._channel import _InactiveRpcError

from kentik_api.public.errors import (
    AuthError,
    BadRequestError,
    KentikAPIError,
    NotFoundError,
    ProtocolError,
    TimedOutError,
    UnavailabilityError,
)

PROTOCOL_GRPC = "gRPC"


def new_api_error(error: RpcError) -> KentikAPIError:
    """Create API error from gRPC error"""

    if not isinstance(error, _InactiveRpcError):
        return KentikAPIError(str(error))

    code: StatusCode = error.code()
    status_code, status_name = code.value

    # StatusCode.OK
    # StatusCode.CANCELLED
    # StatusCode.UNKNOWN
    if code == StatusCode.INVALID_ARGUMENT:
        return BadRequestError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.DEADLINE_EXCEEDED:
        return TimedOutError(f"grpc_status: {status_code} - '{status_name}'")
    if code == StatusCode.NOT_FOUND:
        return NotFoundError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.ALREADY_EXISTS:
        return BadRequestError(PROTOCOL_GRPC, status_code, status_name)
    if code == StatusCode.PERMISSION_DENIED:
        return AuthError(PROTOCOL_GRPC, status_code, status_name)
    # StatusCode.FAILED_PRECONDITION
    # StatusCode.ABORTED
    # StatusCode.OUT_OF_RANGE
    if code == StatusCode.UNIMPLEMENTED:
        return BadRequestError(PROTOCOL_GRPC, status_code, status_name)
    # StatusCode.INTERNAL
    if code == StatusCode.UNAVAILABLE:
        return UnavailabilityError(PROTOCOL_GRPC, status_code, status_name)
    # StatusCode.DATA_LOSS
    if code == StatusCode.UNAUTHENTICATED:
        return AuthError(PROTOCOL_GRPC, status_code, status_name)

    return ProtocolError(PROTOCOL_GRPC, status_code, status_name)
