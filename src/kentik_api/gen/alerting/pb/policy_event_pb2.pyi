from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import policy_filters_pb2 as _policy_filters_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class EventPolicySettings(_message.Message):
    __slots__ = ("type", "dimensions", "filters")
    class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EVENT_TYPE_UNSPECIFIED: _ClassVar[EventPolicySettings.EventType]
        EVENT_TYPE_SYSLOG: _ClassVar[EventPolicySettings.EventType]
        EVENT_TYPE_SNMP_TRAP: _ClassVar[EventPolicySettings.EventType]

    EVENT_TYPE_UNSPECIFIED: EventPolicySettings.EventType
    EVENT_TYPE_SYSLOG: EventPolicySettings.EventType
    EVENT_TYPE_SNMP_TRAP: EventPolicySettings.EventType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    type: EventPolicySettings.EventType
    dimensions: _containers.RepeatedScalarFieldContainer[str]
    filters: _policy_filters_pb2.PolicyFilters
    def __init__(
        self,
        type: _Optional[_Union[EventPolicySettings.EventType, str]] = ...,
        dimensions: _Optional[_Iterable[str]] = ...,
        filters: _Optional[_Union[_policy_filters_pb2.PolicyFilters, _Mapping]] = ...,
    ) -> None: ...

class EventPolicyLevelSettings(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _policy_filters_pb2.PolicyDimensionFilters
    def __init__(
        self,
        filters: _Optional[
            _Union[_policy_filters_pb2.PolicyDimensionFilters, _Mapping]
        ] = ...,
    ) -> None: ...
