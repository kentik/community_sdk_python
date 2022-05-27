import functools
from typing import Any, Callable

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


def wrap_grpc_errors(func: Callable) -> Callable:
    """Wrap GRPC error into KentikAPIError"""

    @functools.wraps(func)
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except RpcError as error:
            raise new_api_error(error) from error

    return inner


def new_api_error(error: RpcError) -> KentikAPIError:
    """Create API error from gRPC error"""

    protocol_grpc = "gRPC"

    if not isinstance(error, _InactiveRpcError):
        return KentikAPIError(str(error))

    # _InactiveRpcError holds error code details
    code: StatusCode = error.code()
    status_code, status_name = code.value

    errors = {
        StatusCode.INVALID_ARGUMENT: BadRequestError(protocol_grpc, status_code, status_name),
        StatusCode.DEADLINE_EXCEEDED: TimedOutError(f"grpc_status: {status_code} - '{status_name}'"),
        StatusCode.NOT_FOUND: NotFoundError(protocol_grpc, status_code, status_name),
        StatusCode.ALREADY_EXISTS: BadRequestError(protocol_grpc, status_code, status_name),
        StatusCode.PERMISSION_DENIED: AuthError(protocol_grpc, status_code, status_name),
        StatusCode.UNIMPLEMENTED: BadRequestError(protocol_grpc, status_code, status_name),
        StatusCode.UNAVAILABLE: UnavailabilityError(protocol_grpc, status_code, status_name),
        StatusCode.UNAUTHENTICATED: AuthError(protocol_grpc, status_code, status_name),
    }

    # StatusCode.CANCELLED
    # StatusCode.UNKNOWN
    # StatusCode.FAILED_PRECONDITION
    # StatusCode.ABORTED
    # StatusCode.OUT_OF_RANGE
    # StatusCode.INTERNAL
    # StatusCode.DATA_LOSS
    default_error = ProtocolError(protocol_grpc, status_code, status_name)

    return errors.get(status_code, default_error)
