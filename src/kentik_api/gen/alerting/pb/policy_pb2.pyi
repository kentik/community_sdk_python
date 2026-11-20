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
from . import policy_event_pb2 as _policy_event_pb2
from . import policy_flow_pb2 as _policy_flow_pb2
from . import policy_nms_pb2 as _policy_nms_pb2
from . import sorting_pb2 as _sorting_pb2
from . import types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyServiceGetRequest(_message.Message):
    __slots__ = ("policy_type", "id")
    POLICY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    policy_type: _common_pb2.PolicyType
    id: str
    def __init__(
        self,
        policy_type: _Optional[_Union[_common_pb2.PolicyType, str]] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...

class PolicyServiceGetResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: Policy
    def __init__(self, policy: _Optional[_Union[Policy, _Mapping]] = ...) -> None: ...

class PolicyServiceListRequest(_message.Message):
    __slots__ = ("pagination", "sorting", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORTING_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationConfig
    sorting: _sorting_pb2.SortingConfig
    filters: PolicyListFilters
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationConfig, _Mapping]] = ...,
        sorting: _Optional[_Union[_sorting_pb2.SortingConfig, _Mapping]] = ...,
        filters: _Optional[_Union[PolicyListFilters, _Mapping]] = ...,
    ) -> None: ...

class PolicyListFilters(_message.Message):
    __slots__ = ("sources", "user_ids", "created_at", "modified_at")
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    sources: _containers.RepeatedCompositeFieldContainer[_common_pb2.Source]
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    created_at: _types_pb2.TimeRange
    modified_at: _types_pb2.TimeRange
    def __init__(
        self,
        sources: _Optional[_Iterable[_Union[_common_pb2.Source, _Mapping]]] = ...,
        user_ids: _Optional[_Iterable[str]] = ...,
        created_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        modified_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
    ) -> None: ...

class PolicyServiceListResponse(_message.Message):
    __slots__ = ("pagination", "policies")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationInfo
    policies: _containers.RepeatedCompositeFieldContainer[Policy]
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationInfo, _Mapping]] = ...,
        policies: _Optional[_Iterable[_Union[Policy, _Mapping]]] = ...,
    ) -> None: ...

class PolicyServiceDisableRequest(_message.Message):
    __slots__ = ("policy_type", "id")
    POLICY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    policy_type: _common_pb2.PolicyType
    id: str
    def __init__(
        self,
        policy_type: _Optional[_Union[_common_pb2.PolicyType, str]] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...

class PolicyServiceDisableResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: Policy
    def __init__(self, policy: _Optional[_Union[Policy, _Mapping]] = ...) -> None: ...

class PolicyServiceEnableRequest(_message.Message):
    __slots__ = ("policy_type", "id")
    POLICY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    policy_type: _common_pb2.PolicyType
    id: str
    def __init__(
        self,
        policy_type: _Optional[_Union[_common_pb2.PolicyType, str]] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...

class PolicyServiceEnableResponse(_message.Message):
    __slots__ = ("policy",)
    POLICY_FIELD_NUMBER: _ClassVar[int]
    policy: Policy
    def __init__(self, policy: _Optional[_Union[Policy, _Mapping]] = ...) -> None: ...

class Policy(_message.Message):
    __slots__ = (
        "source",
        "created_at",
        "modified_at",
        "created_by",
        "modified_by",
        "name",
        "description",
        "enabled",
        "levels",
        "flow",
        "nms",
        "event",
        "has_errors",
        "last_error",
        "expire_date",
    )
    class PolicyErrorInfo(_message.Message):
        __slots__ = ("timestamp", "description")
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        timestamp: _timestamp_pb2.Timestamp
        description: str
        def __init__(
            self,
            timestamp: _Optional[
                _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
            ] = ...,
            description: _Optional[str] = ...,
        ) -> None: ...

    class PolicyLevel(_message.Message):
        __slots__ = (
            "severity",
            "description",
            "ack_required",
            "nms",
            "flow",
            "event",
            "notifications",
        )
        SEVERITY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ACK_REQUIRED_FIELD_NUMBER: _ClassVar[int]
        NMS_FIELD_NUMBER: _ClassVar[int]
        FLOW_FIELD_NUMBER: _ClassVar[int]
        EVENT_FIELD_NUMBER: _ClassVar[int]
        NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
        severity: _types_pb2.Severity
        description: str
        ack_required: bool
        nms: _policy_nms_pb2.NmsPolicyLevelSettings
        flow: _policy_flow_pb2.FlowPolicyLevelSettings
        event: _policy_event_pb2.EventPolicyLevelSettings
        notifications: _containers.RepeatedCompositeFieldContainer[
            _common_pb2.NotificationChannelAssociation
        ]
        def __init__(
            self,
            severity: _Optional[_Union[_types_pb2.Severity, str]] = ...,
            description: _Optional[str] = ...,
            ack_required: _Optional[bool] = ...,
            nms: _Optional[
                _Union[_policy_nms_pb2.NmsPolicyLevelSettings, _Mapping]
            ] = ...,
            flow: _Optional[
                _Union[_policy_flow_pb2.FlowPolicyLevelSettings, _Mapping]
            ] = ...,
            event: _Optional[
                _Union[_policy_event_pb2.EventPolicyLevelSettings, _Mapping]
            ] = ...,
            notifications: _Optional[
                _Iterable[_Union[_common_pb2.NotificationChannelAssociation, _Mapping]]
            ] = ...,
        ) -> None: ...

    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_BY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    LEVELS_FIELD_NUMBER: _ClassVar[int]
    FLOW_FIELD_NUMBER: _ClassVar[int]
    NMS_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    HAS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    LAST_ERROR_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_DATE_FIELD_NUMBER: _ClassVar[int]
    source: _common_pb2.Source
    created_at: _timestamp_pb2.Timestamp
    modified_at: _timestamp_pb2.Timestamp
    created_by: str
    modified_by: str
    name: str
    description: str
    enabled: bool
    levels: _containers.RepeatedCompositeFieldContainer[Policy.PolicyLevel]
    flow: _policy_flow_pb2.FlowPolicySettings
    nms: _policy_nms_pb2.NmsPolicySettings
    event: _policy_event_pb2.EventPolicySettings
    has_errors: bool
    last_error: Policy.PolicyErrorInfo
    expire_date: _timestamp_pb2.Timestamp
    def __init__(
        self,
        source: _Optional[_Union[_common_pb2.Source, _Mapping]] = ...,
        created_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        modified_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        created_by: _Optional[str] = ...,
        modified_by: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        enabled: _Optional[bool] = ...,
        levels: _Optional[_Iterable[_Union[Policy.PolicyLevel, _Mapping]]] = ...,
        flow: _Optional[_Union[_policy_flow_pb2.FlowPolicySettings, _Mapping]] = ...,
        nms: _Optional[_Union[_policy_nms_pb2.NmsPolicySettings, _Mapping]] = ...,
        event: _Optional[_Union[_policy_event_pb2.EventPolicySettings, _Mapping]] = ...,
        has_errors: _Optional[bool] = ...,
        last_error: _Optional[_Union[Policy.PolicyErrorInfo, _Mapping]] = ...,
        expire_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...
