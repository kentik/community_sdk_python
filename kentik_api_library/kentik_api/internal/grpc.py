import functools
from dataclasses import fields
from enum import Enum
from typing import Any, Callable, Type, TypeVar, Union, get_args, get_origin

from google.protobuf.wrappers_pb2 import BoolValue
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

SerializableEnumT = TypeVar("SerializableEnumT", bound="SerializableEnum")


class SerializableEnum(Enum):
    @classmethod
    def from_pb(cls: Type[SerializableEnumT], value: Any) -> SerializableEnumT:
        return cls(value)

    def to_pb(self) -> Any:
        return self.value


def wrap_grpc_errors(func: Callable) -> Callable:
    """Wrap GRPC error into KentikAPIError"""

    @functools.wraps(func)
    def inner(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except RpcError as error:
            raise new_api_error(error) from error

    return inner


class DoNotSerializeMarker:
    """
    Marker type for _ConfigElement.to_pb() method:
    skip objects with field PB_TYPE == NotSerializableMarker during serialization to protobuf object
    """


_ConfigElementT = TypeVar("_ConfigElementT", bound="_ConfigElement")


class _ConfigElement:
    """
    Base class that enables automatic protobuf class <-> user facing dataclass serialization/deserialization.
    Protobuf class and user facing dataclass need to have fields named exactly the same, otherwise the deviations
    must be handled explicitly by defining custom from_pb/to_pb methods for the respective class.
    Fields starting with underscore "_" are treated as read-only and are not serialized to protobuf.
    """

    PB_TYPE = DoNotSerializeMarker  # Target protobuf type for serialization. To be overridden by inheriting class

    def to_pb(self) -> Any:
        """
        Serialize self to protobuf object type determined by "PB_TYPE"
        """

        def skip_serialization(obj: Any) -> bool:
            return obj is None or hasattr(obj, "PB_TYPE") and obj.PB_TYPE == DoNotSerializeMarker

        def get_value(dst_type: Type[Any], src_value: Any) -> Any:
            if skip_serialization(src_value):
                return None  # None values are not serialized into output protobuf object
            if hasattr(src_value, "to_pb"):
                return src_value.to_pb()
            if isinstance(src_value, list):
                return [get_value(type(e), e) for e in src_value]
            if isinstance(src_value, dict):
                return {k: get_value(type(v), v) for k, v in src_value.items()}
            try:
                return dst_type(src_value)
            except TypeError as error:
                raise RuntimeError(
                    f"Don't know how to serialize to '{dst_type}' (type: '{type(src_value)}', value: '{src_value}')"
                ) from error

        dummy_pb_instance = self.PB_TYPE()  # used only for examining the destination protobuf object field types
        args = {}
        for f in fields(self):
            if f.name[0] == "_":
                continue  # don't serialize read-only fields
            dst_field_type = type(getattr(dummy_pb_instance, f.name))
            src_field_value = getattr(self, f.name)
            args[f.name] = get_value(dst_field_type, src_field_value)
        return self.PB_TYPE(**args)

    @classmethod
    def from_pb(cls: Type[_ConfigElementT], obj: Any) -> _ConfigElementT:
        """
        Deserialize protobuf obj into a respective dataclass
        """

        def get_value(dst_type: Type[Any], src_value: Any) -> Any:
            if hasattr(dst_type, "from_pb"):
                return dst_type.from_pb(src_value)
            if isinstance(src_value, BoolValue):  # protobuf BoolValue requires special treatment
                return src_value.value
            try:
                return dst_type(src_value)
            except TypeError as error:
                args = get_args(dst_type)
                origin = get_origin(dst_type)
                if origin is list:
                    return [get_value(args[0], elem) for elem in src_value]
                if origin is dict:
                    return {_k: get_value(args[1], _v) for _k, _v in src_value.items()}
                if origin is Union and len(args) == 2 and isinstance(None, args[1]):  # this means type is Optional[...]
                    if src_value == type(src_value)():  # empty optional protobuf field
                        return None
                    return get_value(args[0], src_value)
                raise RuntimeError(f"Don't know how to instantiate '{dst_type}' (value: '{src_value}')") from error

        _init_fields = [f for f in fields(cls) if f.init]
        args = {}
        for f in _init_fields:
            src_name = f.name[1:] if (f.name[0] == "_") else f.name  # remove leading underscore from attribute name
            args[f.name] = get_value(f.type, getattr(obj, src_name))
        instance = cls(**args)

        _remaining_fields = [f for f in fields(cls) if not f.init]
        for f in _remaining_fields:
            src_name = f.name[1:] if (f.name[0] == "_") else f.name  # remove leading underscore from attribute name
            v = get_value(f.type, getattr(obj, src_name))
            setattr(instance, f.name, v)
        return instance


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
    # Status Codes covered by default_error:
    #   StatusCode.CANCELLED
    #   StatusCode.UNKNOWN
    #   StatusCode.FAILED_PRECONDITION
    #   StatusCode.ABORTED
    #   StatusCode.OUT_OF_RANGE
    #   StatusCode.INTERNAL
    #   StatusCode.DATA_LOSS
    default_error = ProtocolError(protocol_grpc, status_code, status_name)

    return errors.get(status_code, default_error)
