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

DESCRIPTOR: _descriptor.FileDescriptor

class GenericEvent(_message.Message):
    __slots__ = ("event_source", "action", "event_type", "owner", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    EVENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    event_source: str
    action: str
    event_type: str
    owner: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        event_source: _Optional[str] = ...,
        action: _Optional[str] = ...,
        event_type: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class AuditEvent(_message.Message):
    __slots__ = (
        "user_id",
        "id",
        "ctime",
        "api_method",
        "api_path",
        "ip_address",
        "authority",
        "kentik_user_id",
        "kentik_user_email",
        "object_type",
        "object_name",
        "api_action",
        "source",
        "object_id",
        "parent_id",
        "portal_path",
        "generic",
        "title_field",
        "event_payload",
        "user_agent",
    )
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    API_METHOD_FIELD_NUMBER: _ClassVar[int]
    API_PATH_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    KENTIK_USER_ID_FIELD_NUMBER: _ClassVar[int]
    KENTIK_USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    API_ACTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    PORTAL_PATH_FIELD_NUMBER: _ClassVar[int]
    GENERIC_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_FIELD_NUMBER: _ClassVar[int]
    EVENT_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    id: int
    ctime: _timestamp_pb2.Timestamp
    api_method: str
    api_path: str
    ip_address: str
    authority: str
    kentik_user_id: str
    kentik_user_email: str
    object_type: str
    object_name: str
    api_action: str
    source: str
    object_id: str
    parent_id: str
    portal_path: str
    generic: GenericEvent
    title_field: str
    event_payload: str
    user_agent: str
    def __init__(
        self,
        user_id: _Optional[str] = ...,
        id: _Optional[int] = ...,
        ctime: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        api_method: _Optional[str] = ...,
        api_path: _Optional[str] = ...,
        ip_address: _Optional[str] = ...,
        authority: _Optional[str] = ...,
        kentik_user_id: _Optional[str] = ...,
        kentik_user_email: _Optional[str] = ...,
        object_type: _Optional[str] = ...,
        object_name: _Optional[str] = ...,
        api_action: _Optional[str] = ...,
        source: _Optional[str] = ...,
        object_id: _Optional[str] = ...,
        parent_id: _Optional[str] = ...,
        portal_path: _Optional[str] = ...,
        generic: _Optional[_Union[GenericEvent, _Mapping]] = ...,
        title_field: _Optional[str] = ...,
        event_payload: _Optional[str] = ...,
        user_agent: _Optional[str] = ...,
    ) -> None: ...

class ListAuditEventsRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "offset", "limit")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    start_time: str
    end_time: str
    offset: int
    limit: int
    def __init__(
        self,
        start_time: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
        offset: _Optional[int] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListAuditEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[AuditEvent]
    def __init__(
        self, events: _Optional[_Iterable[_Union[AuditEvent, _Mapping]]] = ...
    ) -> None: ...

class GetAuditEventRequest(_message.Message):
    __slots__ = ("id", "ctime")
    ID_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    ctime: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        ctime: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class GetAuditEventResponse(_message.Message):
    __slots__ = ("event",)
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event: AuditEvent
    def __init__(
        self, event: _Optional[_Union[AuditEvent, _Mapping]] = ...
    ) -> None: ...
