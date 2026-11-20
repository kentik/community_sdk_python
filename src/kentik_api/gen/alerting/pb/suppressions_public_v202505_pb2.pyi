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
from . import sorting_pb2 as _sorting_pb2
from . import types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class Suppression(_message.Message):
    __slots__ = (
        "id",
        "user_id",
        "source",
        "key_filter",
        "strict",
        "comment",
        "start_time_at",
        "end_time_at",
        "created_at",
        "modified_at",
        "display_name",
        "severities",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    KEY_FILTER_FIELD_NUMBER: _ClassVar[int]
    STRICT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    SEVERITIES_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    source: _common_pb2.Source
    key_filter: _types_pb2.MultiAttributeFilter
    strict: bool
    comment: str
    start_time_at: _timestamp_pb2.Timestamp
    end_time_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    modified_at: _timestamp_pb2.Timestamp
    display_name: str
    severities: _containers.RepeatedScalarFieldContainer[_types_pb2.Severity]
    def __init__(
        self,
        id: _Optional[str] = ...,
        user_id: _Optional[str] = ...,
        source: _Optional[_Union[_common_pb2.Source, _Mapping]] = ...,
        key_filter: _Optional[_Union[_types_pb2.MultiAttributeFilter, _Mapping]] = ...,
        strict: _Optional[bool] = ...,
        comment: _Optional[str] = ...,
        start_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        created_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        modified_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        display_name: _Optional[str] = ...,
        severities: _Optional[_Iterable[_Union[_types_pb2.Severity, str]]] = ...,
    ) -> None: ...

class SuppressionServiceCreateRequest(_message.Message):
    __slots__ = ("suppression",)
    SUPPRESSION_FIELD_NUMBER: _ClassVar[int]
    suppression: Suppression
    def __init__(
        self, suppression: _Optional[_Union[Suppression, _Mapping]] = ...
    ) -> None: ...

class SuppressionServiceCreateResponse(_message.Message):
    __slots__ = ("suppression",)
    SUPPRESSION_FIELD_NUMBER: _ClassVar[int]
    suppression: Suppression
    def __init__(
        self, suppression: _Optional[_Union[Suppression, _Mapping]] = ...
    ) -> None: ...

class SuppressionServiceGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SuppressionServiceGetResponse(_message.Message):
    __slots__ = ("suppression",)
    SUPPRESSION_FIELD_NUMBER: _ClassVar[int]
    suppression: Suppression
    def __init__(
        self, suppression: _Optional[_Union[Suppression, _Mapping]] = ...
    ) -> None: ...

class SuppressionServiceListRequest(_message.Message):
    __slots__ = ("pagination", "sorting", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORTING_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationConfig
    sorting: _sorting_pb2.SortingConfig
    filters: SuppressionFilters
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationConfig, _Mapping]] = ...,
        sorting: _Optional[_Union[_sorting_pb2.SortingConfig, _Mapping]] = ...,
        filters: _Optional[_Union[SuppressionFilters, _Mapping]] = ...,
    ) -> None: ...

class SuppressionFilters(_message.Message):
    __slots__ = (
        "suppression_ids",
        "sources",
        "user_ids",
        "created_at",
        "modified_at",
        "start_time_at",
        "end_time_at",
    )
    SUPPRESSION_IDS_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    suppression_ids: _containers.RepeatedScalarFieldContainer[str]
    sources: _containers.RepeatedCompositeFieldContainer[_common_pb2.Source]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    created_at: _types_pb2.TimeRange
    modified_at: _types_pb2.TimeRange
    start_time_at: _types_pb2.TimeRange
    end_time_at: _types_pb2.TimeRange
    def __init__(
        self,
        suppression_ids: _Optional[_Iterable[str]] = ...,
        sources: _Optional[_Iterable[_Union[_common_pb2.Source, _Mapping]]] = ...,
        user_ids: _Optional[_Iterable[str]] = ...,
        created_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        modified_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        start_time_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        end_time_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
    ) -> None: ...

class SuppressionServiceListResponse(_message.Message):
    __slots__ = ("pagination", "suppressions")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SUPPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationInfo
    suppressions: _containers.RepeatedCompositeFieldContainer[Suppression]
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationInfo, _Mapping]] = ...,
        suppressions: _Optional[_Iterable[_Union[Suppression, _Mapping]]] = ...,
    ) -> None: ...

class SuppressionServiceReplaceRequest(_message.Message):
    __slots__ = ("suppression",)
    SUPPRESSION_FIELD_NUMBER: _ClassVar[int]
    suppression: Suppression
    def __init__(
        self, suppression: _Optional[_Union[Suppression, _Mapping]] = ...
    ) -> None: ...

class SuppressionServiceReplaceResponse(_message.Message):
    __slots__ = ("suppression",)
    SUPPRESSION_FIELD_NUMBER: _ClassVar[int]
    suppression: Suppression
    def __init__(
        self, suppression: _Optional[_Union[Suppression, _Mapping]] = ...
    ) -> None: ...

class SuppressionServiceDeleteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SuppressionServiceDeleteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
