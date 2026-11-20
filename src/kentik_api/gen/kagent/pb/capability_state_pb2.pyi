import datetime
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from kentik_api.gen.monitoring.pb import component_pb2 as _component_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class CapabilityState(_message.Message):
    __slots__ = (
        "status",
        "timestamp",
        "errors",
        "metadata",
        "privileges",
        "component_state",
    )
    class Health(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        HEALTH_UNSPECIFIED: _ClassVar[CapabilityState.Health]
        HEALTH_OK: _ClassVar[CapabilityState.Health]
        HEALTH_WARNING: _ClassVar[CapabilityState.Health]
        HEALTH_DEGRADED: _ClassVar[CapabilityState.Health]
        HEALTH_FAILING: _ClassVar[CapabilityState.Health]
        HEALTH_UNKNOWN: _ClassVar[CapabilityState.Health]

    HEALTH_UNSPECIFIED: CapabilityState.Health
    HEALTH_OK: CapabilityState.Health
    HEALTH_WARNING: CapabilityState.Health
    HEALTH_DEGRADED: CapabilityState.Health
    HEALTH_FAILING: CapabilityState.Health
    HEALTH_UNKNOWN: CapabilityState.Health
    class ErrorsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_STATE_FIELD_NUMBER: _ClassVar[int]
    status: CapabilityState.Health
    timestamp: _timestamp_pb2.Timestamp
    errors: _containers.ScalarMap[str, str]
    metadata: _struct_pb2.Struct
    privileges: str
    component_state: _component_pb2.ComponentState
    def __init__(
        self,
        status: _Optional[_Union[CapabilityState.Health, str]] = ...,
        timestamp: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        errors: _Optional[_Mapping[str, str]] = ...,
        metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        privileges: _Optional[str] = ...,
        component_state: _Optional[
            _Union[_component_pb2.ComponentState, _Mapping]
        ] = ...,
    ) -> None: ...
