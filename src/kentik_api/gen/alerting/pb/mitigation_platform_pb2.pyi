import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

from . import common_pb2 as _common_pb2
from . import pagination_pb2 as _pagination_pb2
from . import types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class MitigationPlatformsServiceListRequest(_message.Message):
    __slots__ = ("pagination", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationConfig
    filters: MitigationPlatformsFilters
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationConfig, _Mapping]] = ...,
        filters: _Optional[_Union[MitigationPlatformsFilters, _Mapping]] = ...,
    ) -> None: ...

class MitigationPlatformsFilters(_message.Message):
    __slots__ = ("platform_ids", "platform_types", "created_at", "modified_at")
    PLATFORM_IDS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_TYPES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    platform_ids: _containers.RepeatedScalarFieldContainer[str]
    platform_types: _containers.RepeatedScalarFieldContainer[
        _common_pb2.MitigationPlatformType
    ]
    created_at: _types_pb2.TimeRange
    modified_at: _types_pb2.TimeRange
    def __init__(
        self,
        platform_ids: _Optional[_Iterable[str]] = ...,
        platform_types: _Optional[
            _Iterable[_Union[_common_pb2.MitigationPlatformType, str]]
        ] = ...,
        created_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        modified_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
    ) -> None: ...

class MitigationPlatformsServiceListResponse(_message.Message):
    __slots__ = ("pagination", "platforms")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    PLATFORMS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationInfo
    platforms: _containers.RepeatedCompositeFieldContainer[MitigationPlatform]
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationInfo, _Mapping]] = ...,
        platforms: _Optional[_Iterable[_Union[MitigationPlatform, _Mapping]]] = ...,
    ) -> None: ...

class MitigationPlatformsServiceGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class MitigationPlatformsServiceGetResponse(_message.Message):
    __slots__ = ("platform",)
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    platform: MitigationPlatform
    def __init__(
        self, platform: _Optional[_Union[MitigationPlatform, _Mapping]] = ...
    ) -> None: ...

class MitigationPlatform(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "type",
        "mitigation_method_ids",
        "created_at",
        "modified_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_METHOD_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    type: _common_pb2.MitigationPlatformType
    mitigation_method_ids: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    modified_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        type: _Optional[_Union[_common_pb2.MitigationPlatformType, str]] = ...,
        mitigation_method_ids: _Optional[_Iterable[str]] = ...,
        created_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        modified_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...
