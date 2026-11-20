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
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import common_pb2 as _common_pb2
from . import mitigation_types_v202506_pb2 as _mitigation_pb2
from . import pagination_pb2 as _pagination_pb2
from . import types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class MitigationUserAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MITIGATION_USER_ACTION_UNSPECIFIED: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_TAKE_CONTROL: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_STOP: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_START: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_DELETE: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_APPROVE_START: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_SKIP_WAIT: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_RETRY: _ClassVar[MitigationUserAction]
    MITIGATION_USER_ACTION_ACK: _ClassVar[MitigationUserAction]

class MitigationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MITIGATION_STATE_UNSPECIFIED: _ClassVar[MitigationState]
    MITIGATION_STATE_ACK_REQUIRED: _ClassVar[MitigationState]
    MITIGATION_STATE_ARCHIVED: _ClassVar[MitigationState]
    MITIGATION_STATE_CLEARING: _ClassVar[MitigationState]
    MITIGATION_STATE_CLEARING_FAIL: _ClassVar[MitigationState]
    MITIGATION_STATE_END_GRACE: _ClassVar[MitigationState]
    MITIGATION_STATE_END_WAIT: _ClassVar[MitigationState]
    MITIGATION_STATE_MANUAL_CLEAR: _ClassVar[MitigationState]
    MITIGATION_STATE_MANUAL_CLEARING: _ClassVar[MitigationState]
    MITIGATION_STATE_MANUAL_CLEARING_FAIL: _ClassVar[MitigationState]
    MITIGATION_STATE_MANUAL_MITIGATING: _ClassVar[MitigationState]
    MITIGATION_STATE_MANUAL_STARTING: _ClassVar[MitigationState]
    MITIGATION_STATE_MANUAL_STARTING_FAIL: _ClassVar[MitigationState]
    MITIGATION_STATE_MITIGATING: _ClassVar[MitigationState]
    MITIGATION_STATE_STARTING: _ClassVar[MitigationState]
    MITIGATION_STATE_STARTING_FAIL: _ClassVar[MitigationState]
    MITIGATION_STATE_START_WAIT: _ClassVar[MitigationState]

class MitigationEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MITIGATION_EVENT_UNSPECIFIED: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_MANUAL_CONTROL: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_STOP: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_START: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_DELETE: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_APPROVE_START: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_SKIP_WAIT: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_RETRY: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_USER_ACK: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_SKIP_WAIT: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_DONE_WAIT: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_AUTO_START: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_AUTO_STOP: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_REMOTE_ADDED: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_REMOTE_REMOVED: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_REMOTE_ERROR: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_SYSTEM_CLEAR_DELETED: _ClassVar[MitigationEvent]
    MITIGATION_EVENT_TTL_EXPIRED: _ClassVar[MitigationEvent]

MITIGATION_USER_ACTION_UNSPECIFIED: MitigationUserAction
MITIGATION_USER_ACTION_TAKE_CONTROL: MitigationUserAction
MITIGATION_USER_ACTION_STOP: MitigationUserAction
MITIGATION_USER_ACTION_START: MitigationUserAction
MITIGATION_USER_ACTION_DELETE: MitigationUserAction
MITIGATION_USER_ACTION_APPROVE_START: MitigationUserAction
MITIGATION_USER_ACTION_SKIP_WAIT: MitigationUserAction
MITIGATION_USER_ACTION_RETRY: MitigationUserAction
MITIGATION_USER_ACTION_ACK: MitigationUserAction
MITIGATION_STATE_UNSPECIFIED: MitigationState
MITIGATION_STATE_ACK_REQUIRED: MitigationState
MITIGATION_STATE_ARCHIVED: MitigationState
MITIGATION_STATE_CLEARING: MitigationState
MITIGATION_STATE_CLEARING_FAIL: MitigationState
MITIGATION_STATE_END_GRACE: MitigationState
MITIGATION_STATE_END_WAIT: MitigationState
MITIGATION_STATE_MANUAL_CLEAR: MitigationState
MITIGATION_STATE_MANUAL_CLEARING: MitigationState
MITIGATION_STATE_MANUAL_CLEARING_FAIL: MitigationState
MITIGATION_STATE_MANUAL_MITIGATING: MitigationState
MITIGATION_STATE_MANUAL_STARTING: MitigationState
MITIGATION_STATE_MANUAL_STARTING_FAIL: MitigationState
MITIGATION_STATE_MITIGATING: MitigationState
MITIGATION_STATE_STARTING: MitigationState
MITIGATION_STATE_STARTING_FAIL: MitigationState
MITIGATION_STATE_START_WAIT: MitigationState
MITIGATION_EVENT_UNSPECIFIED: MitigationEvent
MITIGATION_EVENT_USER_MANUAL_CONTROL: MitigationEvent
MITIGATION_EVENT_USER_STOP: MitigationEvent
MITIGATION_EVENT_USER_START: MitigationEvent
MITIGATION_EVENT_USER_DELETE: MitigationEvent
MITIGATION_EVENT_USER_APPROVE_START: MitigationEvent
MITIGATION_EVENT_USER_SKIP_WAIT: MitigationEvent
MITIGATION_EVENT_USER_RETRY: MitigationEvent
MITIGATION_EVENT_USER_ACK: MitigationEvent
MITIGATION_EVENT_SKIP_WAIT: MitigationEvent
MITIGATION_EVENT_DONE_WAIT: MitigationEvent
MITIGATION_EVENT_AUTO_START: MitigationEvent
MITIGATION_EVENT_AUTO_STOP: MitigationEvent
MITIGATION_EVENT_REMOTE_ADDED: MitigationEvent
MITIGATION_EVENT_REMOTE_REMOVED: MitigationEvent
MITIGATION_EVENT_REMOTE_ERROR: MitigationEvent
MITIGATION_EVENT_SYSTEM_CLEAR_DELETED: MitigationEvent
MITIGATION_EVENT_TTL_EXPIRED: MitigationEvent

class MitigationsServiceListRequest(_message.Message):
    __slots__ = ("pagination", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationConfig
    filters: MitigationFilters
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationConfig, _Mapping]] = ...,
        filters: _Optional[_Union[MitigationFilters, _Mapping]] = ...,
    ) -> None: ...

class MitigationFilters(_message.Message):
    __slots__ = (
        "created_at",
        "mitigation_ids",
        "sources",
        "alarm_ids",
        "states",
        "platform_ids",
        "method_ids",
        "ip_cidrs",
        "ip_cidr_pattern",
        "types",
    )
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_IDS_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    ALARM_IDS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_IDS_FIELD_NUMBER: _ClassVar[int]
    METHOD_IDS_FIELD_NUMBER: _ClassVar[int]
    IP_CIDRS_FIELD_NUMBER: _ClassVar[int]
    IP_CIDR_PATTERN_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    created_at: _types_pb2.TimeRange
    mitigation_ids: _containers.RepeatedScalarFieldContainer[str]
    sources: _containers.RepeatedCompositeFieldContainer[_common_pb2.Source]
    alarm_ids: _containers.RepeatedScalarFieldContainer[str]
    states: _containers.RepeatedScalarFieldContainer[MitigationState]
    platform_ids: _containers.RepeatedScalarFieldContainer[str]
    method_ids: _containers.RepeatedScalarFieldContainer[str]
    ip_cidrs: _containers.RepeatedScalarFieldContainer[str]
    ip_cidr_pattern: str
    types: _containers.RepeatedScalarFieldContainer[_common_pb2.MitigationType]
    def __init__(
        self,
        created_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        mitigation_ids: _Optional[_Iterable[str]] = ...,
        sources: _Optional[_Iterable[_Union[_common_pb2.Source, _Mapping]]] = ...,
        alarm_ids: _Optional[_Iterable[str]] = ...,
        states: _Optional[_Iterable[_Union[MitigationState, str]]] = ...,
        platform_ids: _Optional[_Iterable[str]] = ...,
        method_ids: _Optional[_Iterable[str]] = ...,
        ip_cidrs: _Optional[_Iterable[str]] = ...,
        ip_cidr_pattern: _Optional[str] = ...,
        types: _Optional[_Iterable[_Union[_common_pb2.MitigationType, str]]] = ...,
    ) -> None: ...

class MitigationsServiceListResponse(_message.Message):
    __slots__ = ("pagination", "mitigations")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    MITIGATIONS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationInfo
    mitigations: _containers.RepeatedCompositeFieldContainer[Mitigation]
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationInfo, _Mapping]] = ...,
        mitigations: _Optional[_Iterable[_Union[Mitigation, _Mapping]]] = ...,
    ) -> None: ...

class MitigationsServiceGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class MitigationsServiceGetResponse(_message.Message):
    __slots__ = ("mitigation",)
    MITIGATION_FIELD_NUMBER: _ClassVar[int]
    mitigation: Mitigation
    def __init__(
        self, mitigation: _Optional[_Union[Mitigation, _Mapping]] = ...
    ) -> None: ...

class MitigationsServiceCreateRequest(_message.Message):
    __slots__ = (
        "platform_id",
        "method_id",
        "ip_cidr",
        "src_port",
        "dst_port",
        "comment",
        "auto_stop_ttl",
    )
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    METHOD_ID_FIELD_NUMBER: _ClassVar[int]
    IP_CIDR_FIELD_NUMBER: _ClassVar[int]
    SRC_PORT_FIELD_NUMBER: _ClassVar[int]
    DST_PORT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    AUTO_STOP_TTL_FIELD_NUMBER: _ClassVar[int]
    platform_id: str
    method_id: str
    ip_cidr: str
    src_port: int
    dst_port: int
    comment: str
    auto_stop_ttl: _duration_pb2.Duration
    def __init__(
        self,
        platform_id: _Optional[str] = ...,
        method_id: _Optional[str] = ...,
        ip_cidr: _Optional[str] = ...,
        src_port: _Optional[int] = ...,
        dst_port: _Optional[int] = ...,
        comment: _Optional[str] = ...,
        auto_stop_ttl: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
    ) -> None: ...

class MitigationsServiceCreateResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class MitigationsServiceActRequest(_message.Message):
    __slots__ = ("ids", "action")
    IDS_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    action: MitigationUserAction
    def __init__(
        self,
        ids: _Optional[_Iterable[str]] = ...,
        action: _Optional[_Union[MitigationUserAction, str]] = ...,
    ) -> None: ...

class MitigationsServiceAvailableActionsForMitigationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class MitigationsServiceAvailableActionsForMitigationResponse(_message.Message):
    __slots__ = ("available_actions",)
    AVAILABLE_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    available_actions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, available_actions: _Optional[_Iterable[str]] = ...) -> None: ...

class MitigationsServiceAvailableActionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MitigationsServiceAvailableActionsResponse(_message.Message):
    __slots__ = ("transitions",)
    class MitigationAvailableTransitions(_message.Message):
        __slots__ = ("from_state", "available_actions")
        FROM_STATE_FIELD_NUMBER: _ClassVar[int]
        AVAILABLE_ACTIONS_FIELD_NUMBER: _ClassVar[int]
        from_state: MitigationState
        available_actions: _containers.RepeatedCompositeFieldContainer[
            MitigationActionDetail
        ]
        def __init__(
            self,
            from_state: _Optional[_Union[MitigationState, str]] = ...,
            available_actions: _Optional[
                _Iterable[_Union[MitigationActionDetail, _Mapping]]
            ] = ...,
        ) -> None: ...

    TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    transitions: _containers.RepeatedCompositeFieldContainer[
        MitigationsServiceAvailableActionsResponse.MitigationAvailableTransitions
    ]
    def __init__(
        self,
        transitions: _Optional[
            _Iterable[
                _Union[
                    MitigationsServiceAvailableActionsResponse.MitigationAvailableTransitions,
                    _Mapping,
                ]
            ]
        ] = ...,
    ) -> None: ...

class MitigationActionDetails(_message.Message):
    __slots__ = ("actions",)
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedCompositeFieldContainer[MitigationActionDetail]
    def __init__(
        self,
        actions: _Optional[_Iterable[_Union[MitigationActionDetail, _Mapping]]] = ...,
    ) -> None: ...

class MitigationActionDetail(_message.Message):
    __slots__ = (
        "event_name",
        "action",
        "action_description",
        "from_state",
        "to_states",
    )
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ACTION_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FROM_STATE_FIELD_NUMBER: _ClassVar[int]
    TO_STATES_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    action: MitigationUserAction
    action_description: str
    from_state: MitigationState
    to_states: _containers.RepeatedScalarFieldContainer[MitigationState]
    def __init__(
        self,
        event_name: _Optional[str] = ...,
        action: _Optional[_Union[MitigationUserAction, str]] = ...,
        action_description: _Optional[str] = ...,
        from_state: _Optional[_Union[MitigationState, str]] = ...,
        to_states: _Optional[_Iterable[_Union[MitigationState, str]]] = ...,
    ) -> None: ...

class MitigationsServiceActResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[MitigationsActResult]
    def __init__(
        self,
        results: _Optional[_Iterable[_Union[MitigationsActResult, _Mapping]]] = ...,
    ) -> None: ...

class MitigationsActResult(_message.Message):
    __slots__ = ("mitigation_id", "success", "message")
    MITIGATION_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    mitigation_id: int
    success: bool
    message: str
    def __init__(
        self,
        mitigation_id: _Optional[int] = ...,
        success: _Optional[bool] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class Mitigation(_message.Message):
    __slots__ = (
        "id",
        "type",
        "alarm_ids",
        "target",
        "current_state",
        "previous_state",
        "platform_id",
        "method_id",
        "start_time_at",
        "end_time_at",
        "states",
        "auto_stop_ttl",
        "comment",
        "source",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ALARM_IDS_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_STATE_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    METHOD_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    AUTO_STOP_TTL_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: _common_pb2.MitigationType
    alarm_ids: _containers.RepeatedScalarFieldContainer[str]
    target: _mitigation_pb2.MitigationTarget
    current_state: MitigationState
    previous_state: MitigationState
    platform_id: str
    method_id: str
    start_time_at: _timestamp_pb2.Timestamp
    end_time_at: _timestamp_pb2.Timestamp
    states: _containers.RepeatedCompositeFieldContainer[MitigationStateEntry]
    auto_stop_ttl: _duration_pb2.Duration
    comment: str
    source: _common_pb2.Source
    def __init__(
        self,
        id: _Optional[str] = ...,
        type: _Optional[_Union[_common_pb2.MitigationType, str]] = ...,
        alarm_ids: _Optional[_Iterable[str]] = ...,
        target: _Optional[_Union[_mitigation_pb2.MitigationTarget, _Mapping]] = ...,
        current_state: _Optional[_Union[MitigationState, str]] = ...,
        previous_state: _Optional[_Union[MitigationState, str]] = ...,
        platform_id: _Optional[str] = ...,
        method_id: _Optional[str] = ...,
        start_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        states: _Optional[_Iterable[_Union[MitigationStateEntry, _Mapping]]] = ...,
        auto_stop_ttl: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
        comment: _Optional[str] = ...,
        source: _Optional[_Union[_common_pb2.Source, _Mapping]] = ...,
    ) -> None: ...

class MitigationStateEntry(_message.Message):
    __slots__ = ("timestamp", "state", "event")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    state: MitigationState
    event: MitigationEvent
    def __init__(
        self,
        timestamp: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        state: _Optional[_Union[MitigationState, str]] = ...,
        event: _Optional[_Union[MitigationEvent, str]] = ...,
    ) -> None: ...
