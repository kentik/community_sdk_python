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

class AlertAutoAck(_message.Message):
    __slots__ = (
        "id",
        "user_id",
        "source",
        "key",
        "start_time_at",
        "end_time_at",
        "created_at",
        "modified_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    source: _common_pb2.Source
    key: _types_pb2.KeyValue
    start_time_at: _timestamp_pb2.Timestamp
    end_time_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    modified_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        user_id: _Optional[str] = ...,
        source: _Optional[_Union[_common_pb2.Source, _Mapping]] = ...,
        key: _Optional[_Union[_types_pb2.KeyValue, _Mapping]] = ...,
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
    ) -> None: ...

class AlertAutoAckServiceCreateRequest(_message.Message):
    __slots__ = ("auto_ack",)
    AUTO_ACK_FIELD_NUMBER: _ClassVar[int]
    auto_ack: AlertAutoAck
    def __init__(
        self, auto_ack: _Optional[_Union[AlertAutoAck, _Mapping]] = ...
    ) -> None: ...

class AlertAutoAckServiceCreateResponse(_message.Message):
    __slots__ = ("auto_ack",)
    AUTO_ACK_FIELD_NUMBER: _ClassVar[int]
    auto_ack: AlertAutoAck
    def __init__(
        self, auto_ack: _Optional[_Union[AlertAutoAck, _Mapping]] = ...
    ) -> None: ...

class AlertAutoAckServiceGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AlertAutoAckServiceGetResponse(_message.Message):
    __slots__ = ("auto_ack",)
    AUTO_ACK_FIELD_NUMBER: _ClassVar[int]
    auto_ack: AlertAutoAck
    def __init__(
        self, auto_ack: _Optional[_Union[AlertAutoAck, _Mapping]] = ...
    ) -> None: ...

class AlertAutoAckServiceListRequest(_message.Message):
    __slots__ = ("pagination", "sorting", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORTING_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationConfig
    sorting: _sorting_pb2.SortingConfig
    filters: AlertAutoAckFilters
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationConfig, _Mapping]] = ...,
        sorting: _Optional[_Union[_sorting_pb2.SortingConfig, _Mapping]] = ...,
        filters: _Optional[_Union[AlertAutoAckFilters, _Mapping]] = ...,
    ) -> None: ...

class AlertAutoAckFilters(_message.Message):
    __slots__ = (
        "auto_ack_ids",
        "sources",
        "keys",
        "user_ids",
        "created_at",
        "modified_at",
        "start_time_at",
        "end_time_at",
    )
    AUTO_ACK_IDS_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    auto_ack_ids: _containers.RepeatedScalarFieldContainer[str]
    sources: _containers.RepeatedCompositeFieldContainer[_common_pb2.Source]
    keys: _containers.RepeatedCompositeFieldContainer[_types_pb2.KeyValue]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    created_at: _types_pb2.TimeRange
    modified_at: _types_pb2.TimeRange
    start_time_at: _types_pb2.TimeRange
    end_time_at: _types_pb2.TimeRange
    def __init__(
        self,
        auto_ack_ids: _Optional[_Iterable[str]] = ...,
        sources: _Optional[_Iterable[_Union[_common_pb2.Source, _Mapping]]] = ...,
        keys: _Optional[_Iterable[_Union[_types_pb2.KeyValue, _Mapping]]] = ...,
        user_ids: _Optional[_Iterable[str]] = ...,
        created_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        modified_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        start_time_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        end_time_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
    ) -> None: ...

class AlertAutoAckServiceListResponse(_message.Message):
    __slots__ = ("pagination", "auto_acks")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    AUTO_ACKS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationInfo
    auto_acks: _containers.RepeatedCompositeFieldContainer[AlertAutoAck]
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationInfo, _Mapping]] = ...,
        auto_acks: _Optional[_Iterable[_Union[AlertAutoAck, _Mapping]]] = ...,
    ) -> None: ...

class AlertAutoAckServiceReplaceRequest(_message.Message):
    __slots__ = ("auto_ack",)
    AUTO_ACK_FIELD_NUMBER: _ClassVar[int]
    auto_ack: AlertAutoAck
    def __init__(
        self, auto_ack: _Optional[_Union[AlertAutoAck, _Mapping]] = ...
    ) -> None: ...

class AlertAutoAckServiceReplaceResponse(_message.Message):
    __slots__ = ("auto_ack",)
    AUTO_ACK_FIELD_NUMBER: _ClassVar[int]
    auto_ack: AlertAutoAck
    def __init__(
        self, auto_ack: _Optional[_Union[AlertAutoAck, _Mapping]] = ...
    ) -> None: ...

class AlertAutoAckServiceDeleteRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AlertAutoAckServiceDeleteResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
