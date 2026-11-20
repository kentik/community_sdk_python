import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

from . import common_pb2 as _common_pb2
from . import pagination_pb2 as _pagination_pb2
from . import types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class MitigationMethodsServiceListRequest(_message.Message):
    __slots__ = ("pagination", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationConfig
    filters: MitigationMethodsFilters
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationConfig, _Mapping]] = ...,
        filters: _Optional[_Union[MitigationMethodsFilters, _Mapping]] = ...,
    ) -> None: ...

class MitigationMethodsFilters(_message.Message):
    __slots__ = ("method_ids", "platform_types", "created_at", "modified_at")
    METHOD_IDS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_TYPES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    method_ids: _containers.RepeatedScalarFieldContainer[str]
    platform_types: _containers.RepeatedScalarFieldContainer[
        _common_pb2.MitigationPlatformType
    ]
    created_at: _types_pb2.TimeRange
    modified_at: _types_pb2.TimeRange
    def __init__(
        self,
        method_ids: _Optional[_Iterable[str]] = ...,
        platform_types: _Optional[
            _Iterable[_Union[_common_pb2.MitigationPlatformType, str]]
        ] = ...,
        created_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        modified_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
    ) -> None: ...

class MitigationMethodsServiceListResponse(_message.Message):
    __slots__ = ("pagination", "methods")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    METHODS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationInfo
    methods: _containers.RepeatedCompositeFieldContainer[MitigationMethod]
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationInfo, _Mapping]] = ...,
        methods: _Optional[_Iterable[_Union[MitigationMethod, _Mapping]]] = ...,
    ) -> None: ...

class MitigationMethodsServiceGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class MitigationMethodsServiceGetResponse(_message.Message):
    __slots__ = ("method",)
    METHOD_FIELD_NUMBER: _ClassVar[int]
    method: MitigationMethod
    def __init__(
        self, method: _Optional[_Union[MitigationMethod, _Mapping]] = ...
    ) -> None: ...

class MitigationMethod(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "ack_required",
        "excluded_ip_cidrs",
        "grace_period",
        "type",
        "created_at",
        "modified_at",
        "notifications",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACK_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_IP_CIDRS_FIELD_NUMBER: _ClassVar[int]
    GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    ack_required: bool
    excluded_ip_cidrs: _containers.RepeatedScalarFieldContainer[str]
    grace_period: _duration_pb2.Duration
    type: _common_pb2.MitigationPlatformType
    created_at: _timestamp_pb2.Timestamp
    modified_at: _timestamp_pb2.Timestamp
    notifications: _containers.RepeatedCompositeFieldContainer[
        _common_pb2.NotificationChannelAssociation
    ]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        ack_required: _Optional[bool] = ...,
        excluded_ip_cidrs: _Optional[_Iterable[str]] = ...,
        grace_period: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
        type: _Optional[_Union[_common_pb2.MitigationPlatformType, str]] = ...,
        created_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        modified_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        notifications: _Optional[
            _Iterable[_Union[_common_pb2.NotificationChannelAssociation, _Mapping]]
        ] = ...,
    ) -> None: ...
