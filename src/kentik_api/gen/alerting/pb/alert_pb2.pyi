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
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from . import comment_pb2 as _comment_pb2
from . import common_pb2 as _common_pb2
from . import nms_common_pb2 as _nms_common_pb2
from . import pagination_pb2 as _pagination_pb2
from . import sorting_pb2 as _sorting_pb2
from . import types_pb2 as _types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class AlertState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALERT_STATE_UNSPECIFIED: _ClassVar[AlertState]
    ALERT_STATE_CLEAR: _ClassVar[AlertState]
    ALERT_STATE_ACTIVE: _ClassVar[AlertState]

class AlertAcknowledgement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALERT_ACKNOWLEDGEMENT_UNSPECIFIED: _ClassVar[AlertAcknowledgement]
    ALERT_ACKNOWLEDGEMENT_REQUIRED: _ClassVar[AlertAcknowledgement]
    ALERT_ACKNOWLEDGEMENT_DONE: _ClassVar[AlertAcknowledgement]
    ALERT_ACKNOWLEDGEMENT_NOT_ACKED: _ClassVar[AlertAcknowledgement]

ALERT_STATE_UNSPECIFIED: AlertState
ALERT_STATE_CLEAR: AlertState
ALERT_STATE_ACTIVE: AlertState
ALERT_ACKNOWLEDGEMENT_UNSPECIFIED: AlertAcknowledgement
ALERT_ACKNOWLEDGEMENT_REQUIRED: AlertAcknowledgement
ALERT_ACKNOWLEDGEMENT_DONE: AlertAcknowledgement
ALERT_ACKNOWLEDGEMENT_NOT_ACKED: AlertAcknowledgement

class AlertServiceGetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AlertServiceGetResponse(_message.Message):
    __slots__ = ("alert", "history", "comments")
    ALERT_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    alert: Alert
    history: _containers.RepeatedCompositeFieldContainer[AlertPhase]
    comments: _containers.RepeatedCompositeFieldContainer[_comment_pb2.Comment]
    def __init__(
        self,
        alert: _Optional[_Union[Alert, _Mapping]] = ...,
        history: _Optional[_Iterable[_Union[AlertPhase, _Mapping]]] = ...,
        comments: _Optional[_Iterable[_Union[_comment_pb2.Comment, _Mapping]]] = ...,
    ) -> None: ...

class AlertPhase(_message.Message):
    __slots__ = ("severity", "start_time_at", "end_time_at", "flow", "nms")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    FLOW_FIELD_NUMBER: _ClassVar[int]
    NMS_FIELD_NUMBER: _ClassVar[int]
    severity: _types_pb2.Severity
    start_time_at: _timestamp_pb2.Timestamp
    end_time_at: _timestamp_pb2.Timestamp
    flow: FlowContext
    nms: NmsContext
    def __init__(
        self,
        severity: _Optional[_Union[_types_pb2.Severity, str]] = ...,
        start_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        flow: _Optional[_Union[FlowContext, _Mapping]] = ...,
        nms: _Optional[_Union[NmsContext, _Mapping]] = ...,
    ) -> None: ...

class AlertServiceListRequest(_message.Message):
    __slots__ = ("pagination", "sorting", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    SORTING_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationConfig
    sorting: _sorting_pb2.SortingConfig
    filters: AlertFilters
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationConfig, _Mapping]] = ...,
        sorting: _Optional[_Union[_sorting_pb2.SortingConfig, _Mapping]] = ...,
        filters: _Optional[_Union[AlertFilters, _Mapping]] = ...,
    ) -> None: ...

class AlertFilters(_message.Message):
    __slots__ = (
        "severities",
        "alert_ids",
        "sources",
        "keys",
        "states",
        "started_at",
        "ended_at",
        "highest_severities",
        "recent_severities",
        "ack_states",
        "active_at",
        "acked_by_user_ids",
        "include_removed_policies",
        "context_search",
    )
    SEVERITIES_FIELD_NUMBER: _ClassVar[int]
    ALERT_IDS_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    ENDED_AT_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_SEVERITIES_FIELD_NUMBER: _ClassVar[int]
    RECENT_SEVERITIES_FIELD_NUMBER: _ClassVar[int]
    ACK_STATES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_AT_FIELD_NUMBER: _ClassVar[int]
    ACKED_BY_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_REMOVED_POLICIES_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_SEARCH_FIELD_NUMBER: _ClassVar[int]
    severities: _containers.RepeatedScalarFieldContainer[_types_pb2.Severity]
    alert_ids: _containers.RepeatedScalarFieldContainer[str]
    sources: _containers.RepeatedCompositeFieldContainer[_common_pb2.Source]
    keys: _types_pb2.MultiAttributeFilter
    states: _containers.RepeatedScalarFieldContainer[AlertState]
    started_at: _types_pb2.TimeRange
    ended_at: _types_pb2.TimeRange
    highest_severities: _containers.RepeatedScalarFieldContainer[_types_pb2.Severity]
    recent_severities: _containers.RepeatedScalarFieldContainer[_types_pb2.Severity]
    ack_states: _containers.RepeatedScalarFieldContainer[AlertAcknowledgement]
    active_at: _types_pb2.TimeRange
    acked_by_user_ids: _containers.RepeatedScalarFieldContainer[str]
    include_removed_policies: bool
    context_search: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        severities: _Optional[_Iterable[_Union[_types_pb2.Severity, str]]] = ...,
        alert_ids: _Optional[_Iterable[str]] = ...,
        sources: _Optional[_Iterable[_Union[_common_pb2.Source, _Mapping]]] = ...,
        keys: _Optional[_Union[_types_pb2.MultiAttributeFilter, _Mapping]] = ...,
        states: _Optional[_Iterable[_Union[AlertState, str]]] = ...,
        started_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        ended_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        highest_severities: _Optional[
            _Iterable[_Union[_types_pb2.Severity, str]]
        ] = ...,
        recent_severities: _Optional[_Iterable[_Union[_types_pb2.Severity, str]]] = ...,
        ack_states: _Optional[_Iterable[_Union[AlertAcknowledgement, str]]] = ...,
        active_at: _Optional[_Union[_types_pb2.TimeRange, _Mapping]] = ...,
        acked_by_user_ids: _Optional[_Iterable[str]] = ...,
        include_removed_policies: _Optional[bool] = ...,
        context_search: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class AlertServiceListResponse(_message.Message):
    __slots__ = ("pagination", "alerts")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    ALERTS_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PaginationInfo
    alerts: _containers.RepeatedCompositeFieldContainer[Alert]
    def __init__(
        self,
        pagination: _Optional[_Union[_pagination_pb2.PaginationInfo, _Mapping]] = ...,
        alerts: _Optional[_Iterable[_Union[Alert, _Mapping]]] = ...,
    ) -> None: ...

class AlertServiceAckRequest(_message.Message):
    __slots__ = ("id", "comment")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    id: str
    comment: str
    def __init__(
        self, id: _Optional[str] = ..., comment: _Optional[str] = ...
    ) -> None: ...

class AlertServiceAckResponse(_message.Message):
    __slots__ = ("alert",)
    ALERT_FIELD_NUMBER: _ClassVar[int]
    alert: Alert
    def __init__(self, alert: _Optional[_Union[Alert, _Mapping]] = ...) -> None: ...

class AlertServiceUnAckRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AlertServiceUnAckResponse(_message.Message):
    __slots__ = ("alert",)
    ALERT_FIELD_NUMBER: _ClassVar[int]
    alert: Alert
    def __init__(self, alert: _Optional[_Union[Alert, _Mapping]] = ...) -> None: ...

class AlertServiceClearRequest(_message.Message):
    __slots__ = ("alert_ids",)
    ALERT_IDS_FIELD_NUMBER: _ClassVar[int]
    alert_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, alert_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AlertServiceClearResponse(_message.Message):
    __slots__ = ("cleared_alert_ids",)
    CLEARED_ALERT_IDS_FIELD_NUMBER: _ClassVar[int]
    cleared_alert_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cleared_alert_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ServiceNowContext(_message.Message):
    __slots__ = ("incident_id", "incident_url")
    INCIDENT_ID_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_URL_FIELD_NUMBER: _ClassVar[int]
    incident_id: str
    incident_url: str
    def __init__(
        self, incident_id: _Optional[str] = ..., incident_url: _Optional[str] = ...
    ) -> None: ...

class JiraCloudContext(_message.Message):
    __slots__ = ("issue_key", "issue_url")
    ISSUE_KEY_FIELD_NUMBER: _ClassVar[int]
    ISSUE_URL_FIELD_NUMBER: _ClassVar[int]
    issue_key: str
    issue_url: str
    def __init__(
        self, issue_key: _Optional[str] = ..., issue_url: _Optional[str] = ...
    ) -> None: ...

class ExternalContext(_message.Message):
    __slots__ = ("servicenow", "jira_cloud")
    SERVICENOW_FIELD_NUMBER: _ClassVar[int]
    JIRA_CLOUD_FIELD_NUMBER: _ClassVar[int]
    servicenow: ServiceNowContext
    jira_cloud: JiraCloudContext
    def __init__(
        self,
        servicenow: _Optional[_Union[ServiceNowContext, _Mapping]] = ...,
        jira_cloud: _Optional[_Union[JiraCloudContext, _Mapping]] = ...,
    ) -> None: ...

class AlertServiceSetExternalContextRequest(_message.Message):
    __slots__ = ("alert_id", "context")
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    alert_id: str
    context: ExternalContext
    def __init__(
        self,
        alert_id: _Optional[str] = ...,
        context: _Optional[_Union[ExternalContext, _Mapping]] = ...,
    ) -> None: ...

class AlertServiceSetExternalContextResponse(_message.Message):
    __slots__ = ("updated_at",)
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        updated_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class Alert(_message.Message):
    __slots__ = (
        "id",
        "source",
        "start_time_at",
        "end_time_at",
        "state",
        "severity",
        "highest_severity",
        "acknowledgement",
        "event_start_time_at",
        "flow",
        "nms",
        "mitigation_id",
        "external_contexts",
    )
    class Acknowledgement(_message.Message):
        __slots__ = ("state", "acked_by_user", "auto_ack_id", "acked_at")
        STATE_FIELD_NUMBER: _ClassVar[int]
        ACKED_BY_USER_FIELD_NUMBER: _ClassVar[int]
        AUTO_ACK_ID_FIELD_NUMBER: _ClassVar[int]
        ACKED_AT_FIELD_NUMBER: _ClassVar[int]
        state: AlertAcknowledgement
        acked_by_user: str
        auto_ack_id: str
        acked_at: _timestamp_pb2.Timestamp
        def __init__(
            self,
            state: _Optional[_Union[AlertAcknowledgement, str]] = ...,
            acked_by_user: _Optional[str] = ...,
            auto_ack_id: _Optional[str] = ...,
            acked_at: _Optional[
                _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
            ] = ...,
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    END_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    HIGHEST_SEVERITY_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGEMENT_FIELD_NUMBER: _ClassVar[int]
    EVENT_START_TIME_AT_FIELD_NUMBER: _ClassVar[int]
    FLOW_FIELD_NUMBER: _ClassVar[int]
    NMS_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONTEXTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    source: _common_pb2.Source
    start_time_at: _timestamp_pb2.Timestamp
    end_time_at: _timestamp_pb2.Timestamp
    state: AlertState
    severity: _types_pb2.Severity
    highest_severity: _types_pb2.Severity
    acknowledgement: Alert.Acknowledgement
    event_start_time_at: _timestamp_pb2.Timestamp
    flow: FlowContext
    nms: NmsContext
    mitigation_id: int
    external_contexts: _containers.RepeatedCompositeFieldContainer[ExternalContext]
    def __init__(
        self,
        id: _Optional[str] = ...,
        source: _Optional[_Union[_common_pb2.Source, _Mapping]] = ...,
        start_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        state: _Optional[_Union[AlertState, str]] = ...,
        severity: _Optional[_Union[_types_pb2.Severity, str]] = ...,
        highest_severity: _Optional[_Union[_types_pb2.Severity, str]] = ...,
        acknowledgement: _Optional[_Union[Alert.Acknowledgement, _Mapping]] = ...,
        event_start_time_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        flow: _Optional[_Union[FlowContext, _Mapping]] = ...,
        nms: _Optional[_Union[NmsContext, _Mapping]] = ...,
        mitigation_id: _Optional[int] = ...,
        external_contexts: _Optional[
            _Iterable[_Union[ExternalContext, _Mapping]]
        ] = ...,
    ) -> None: ...

class FlowContext(_message.Message):
    __slots__ = (
        "metric_values",
        "activation_status",
        "baseline_value",
        "alert_key_details",
    )
    class ActivationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACTIVATION_STATUS_UNSPECIFIED: _ClassVar[FlowContext.ActivationStatus]
        ACTIVATION_STATUS_NOT_USED_BASELINE: _ClassVar[FlowContext.ActivationStatus]
        ACTIVATION_STATUS_BASELINE_MISSING_SKIP: _ClassVar[FlowContext.ActivationStatus]
        ACTIVATION_STATUS_BASELINE_MISSING_TRIGGER: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_BASELINE_USED_FOUND: _ClassVar[FlowContext.ActivationStatus]
        ACTIVATION_STATUS_BASELINE_MISSING_DEFAULT: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_BASELINE_MISSING_LOWEST: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_BASELINE_MISSING_HIGHEST: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_BASELINE_NOT_FOUND_EXISTS: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_CURRENT_MISSING_SKIP: _ClassVar[FlowContext.ActivationStatus]
        ACTIVATION_STATUS_CURRENT_MISSING_TRIGGER: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_CURRENT_USED_FOUND: _ClassVar[FlowContext.ActivationStatus]
        ACTIVATION_STATUS_CURRENT_MISSING_DEFAULT: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_CURRENT_MISSING_LOWEST: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_CURRENT_MISSING_HIGHEST: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_CURRENT_NOT_FOUND_EXISTS: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_BASELINE_MISSING_DEFAULT_INSTEAD_OF_LOWEST: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_BASELINE_MISSING_DEFAULT_INSTEAD_OF_HIGHEST: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_CURRENT_MISSING_DEFAULT_INSTEAD_OF_LOWEST: _ClassVar[
            FlowContext.ActivationStatus
        ]
        ACTIVATION_STATUS_CURRENT_MISSING_DEFAULT_INSTEAD_OF_HIGHEST: _ClassVar[
            FlowContext.ActivationStatus
        ]

    ACTIVATION_STATUS_UNSPECIFIED: FlowContext.ActivationStatus
    ACTIVATION_STATUS_NOT_USED_BASELINE: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_MISSING_SKIP: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_MISSING_TRIGGER: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_USED_FOUND: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_MISSING_DEFAULT: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_MISSING_LOWEST: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_MISSING_HIGHEST: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_NOT_FOUND_EXISTS: FlowContext.ActivationStatus
    ACTIVATION_STATUS_CURRENT_MISSING_SKIP: FlowContext.ActivationStatus
    ACTIVATION_STATUS_CURRENT_MISSING_TRIGGER: FlowContext.ActivationStatus
    ACTIVATION_STATUS_CURRENT_USED_FOUND: FlowContext.ActivationStatus
    ACTIVATION_STATUS_CURRENT_MISSING_DEFAULT: FlowContext.ActivationStatus
    ACTIVATION_STATUS_CURRENT_MISSING_LOWEST: FlowContext.ActivationStatus
    ACTIVATION_STATUS_CURRENT_MISSING_HIGHEST: FlowContext.ActivationStatus
    ACTIVATION_STATUS_CURRENT_NOT_FOUND_EXISTS: FlowContext.ActivationStatus
    ACTIVATION_STATUS_BASELINE_MISSING_DEFAULT_INSTEAD_OF_LOWEST: (
        FlowContext.ActivationStatus
    )
    ACTIVATION_STATUS_BASELINE_MISSING_DEFAULT_INSTEAD_OF_HIGHEST: (
        FlowContext.ActivationStatus
    )
    ACTIVATION_STATUS_CURRENT_MISSING_DEFAULT_INSTEAD_OF_LOWEST: (
        FlowContext.ActivationStatus
    )
    ACTIVATION_STATUS_CURRENT_MISSING_DEFAULT_INSTEAD_OF_HIGHEST: (
        FlowContext.ActivationStatus
    )
    class AlertKeyDetailsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FlowContext.AlertKeyDetails
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[FlowContext.AlertKeyDetails, _Mapping]] = ...,
        ) -> None: ...

    class MetricValue(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: float
        def __init__(
            self, name: _Optional[str] = ..., value: _Optional[float] = ...
        ) -> None: ...

    class AlertKeyDetails(_message.Message):
        __slots__ = ("device", "interface", "site", "extended_value")
        DEVICE_FIELD_NUMBER: _ClassVar[int]
        INTERFACE_FIELD_NUMBER: _ClassVar[int]
        SITE_FIELD_NUMBER: _ClassVar[int]
        EXTENDED_VALUE_FIELD_NUMBER: _ClassVar[int]
        device: FlowContext.DeviceDetails
        interface: FlowContext.InterfaceDetails
        site: FlowContext.SiteDetails
        extended_value: str
        def __init__(
            self,
            device: _Optional[_Union[FlowContext.DeviceDetails, _Mapping]] = ...,
            interface: _Optional[_Union[FlowContext.InterfaceDetails, _Mapping]] = ...,
            site: _Optional[_Union[FlowContext.SiteDetails, _Mapping]] = ...,
            extended_value: _Optional[str] = ...,
        ) -> None: ...

    class DeviceDetails(_message.Message):
        __slots__ = ("id", "name", "type", "labels")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        LABELS_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        type: str
        labels: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self,
            id: _Optional[str] = ...,
            name: _Optional[str] = ...,
            type: _Optional[str] = ...,
            labels: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    class InterfaceDetails(_message.Message):
        __slots__ = ("snmp_id", "snmp_alias", "description", "snmp_speed_mbps")
        SNMP_ID_FIELD_NUMBER: _ClassVar[int]
        SNMP_ALIAS_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        SNMP_SPEED_MBPS_FIELD_NUMBER: _ClassVar[int]
        snmp_id: str
        snmp_alias: str
        description: str
        snmp_speed_mbps: int
        def __init__(
            self,
            snmp_id: _Optional[str] = ...,
            snmp_alias: _Optional[str] = ...,
            description: _Optional[str] = ...,
            snmp_speed_mbps: _Optional[int] = ...,
        ) -> None: ...

    class SiteDetails(_message.Message):
        __slots__ = ("id", "name", "latitude", "longitude", "location", "country")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        LATITUDE_FIELD_NUMBER: _ClassVar[int]
        LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        COUNTRY_FIELD_NUMBER: _ClassVar[int]
        id: str
        name: str
        latitude: str
        longitude: str
        location: str
        country: str
        def __init__(
            self,
            id: _Optional[str] = ...,
            name: _Optional[str] = ...,
            latitude: _Optional[str] = ...,
            longitude: _Optional[str] = ...,
            location: _Optional[str] = ...,
            country: _Optional[str] = ...,
        ) -> None: ...

    METRIC_VALUES_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    BASELINE_VALUE_FIELD_NUMBER: _ClassVar[int]
    ALERT_KEY_DETAILS_FIELD_NUMBER: _ClassVar[int]
    metric_values: _containers.RepeatedCompositeFieldContainer[FlowContext.MetricValue]
    activation_status: FlowContext.ActivationStatus
    baseline_value: float
    alert_key_details: _containers.MessageMap[str, FlowContext.AlertKeyDetails]
    def __init__(
        self,
        metric_values: _Optional[
            _Iterable[_Union[FlowContext.MetricValue, _Mapping]]
        ] = ...,
        activation_status: _Optional[_Union[FlowContext.ActivationStatus, str]] = ...,
        baseline_value: _Optional[float] = ...,
        alert_key_details: _Optional[_Mapping[str, FlowContext.AlertKeyDetails]] = ...,
    ) -> None: ...

class NmsContext(_message.Message):
    __slots__ = (
        "activation_info",
        "dataset_info",
        "targets",
        "metric_values",
        "previous_metric_values",
        "device",
        "group_key",
    )
    class TargetsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NmsContext.AlarmTarget
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[NmsContext.AlarmTarget, _Mapping]] = ...,
        ) -> None: ...

    class MetricValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NmsContext.AlarmMetricMap
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[NmsContext.AlarmMetricMap, _Mapping]] = ...,
        ) -> None: ...

    class PreviousMetricValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NmsContext.AlarmMetricMap
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[NmsContext.AlarmMetricMap, _Mapping]] = ...,
        ) -> None: ...

    class DeviceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class GroupKeyEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class ActivationInfo(_message.Message):
        __slots__ = ("activate", "severity", "clear_manual", "clear_unless_activated")
        ACTIVATE_FIELD_NUMBER: _ClassVar[int]
        SEVERITY_FIELD_NUMBER: _ClassVar[int]
        CLEAR_MANUAL_FIELD_NUMBER: _ClassVar[int]
        CLEAR_UNLESS_ACTIVATED_FIELD_NUMBER: _ClassVar[int]
        activate: _nms_common_pb2.NmsActivateOrClearConditions
        severity: _types_pb2.Severity
        clear_manual: bool
        clear_unless_activated: bool
        def __init__(
            self,
            activate: _Optional[
                _Union[_nms_common_pb2.NmsActivateOrClearConditions, _Mapping]
            ] = ...,
            severity: _Optional[_Union[_types_pb2.Severity, str]] = ...,
            clear_manual: _Optional[bool] = ...,
            clear_unless_activated: _Optional[bool] = ...,
        ) -> None: ...

    class DatasetInfo(_message.Message):
        __slots__ = ("custom_type", "dimensions", "entity_type", "measurements")
        CUSTOM_TYPE_FIELD_NUMBER: _ClassVar[int]
        DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
        ENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
        MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
        custom_type: bool
        dimensions: _containers.RepeatedScalarFieldContainer[str]
        entity_type: str
        measurements: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self,
            custom_type: _Optional[bool] = ...,
            dimensions: _Optional[_Iterable[str]] = ...,
            entity_type: _Optional[str] = ...,
            measurements: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    class AlarmTarget(_message.Message):
        __slots__ = ("fields", "tags")
        class FieldsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: float
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[float] = ...
            ) -> None: ...

        class TagsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[str] = ...
            ) -> None: ...

        FIELDS_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        fields: _containers.ScalarMap[str, float]
        tags: _containers.ScalarMap[str, str]
        def __init__(
            self,
            fields: _Optional[_Mapping[str, float]] = ...,
            tags: _Optional[_Mapping[str, str]] = ...,
        ) -> None: ...

    class AlarmMetricMap(_message.Message):
        __slots__ = ("metrics",)
        class MetricsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: float
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[float] = ...
            ) -> None: ...

        METRICS_FIELD_NUMBER: _ClassVar[int]
        metrics: _containers.ScalarMap[str, float]
        def __init__(self, metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

    ACTIVATION_INFO_FIELD_NUMBER: _ClassVar[int]
    DATASET_INFO_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    METRIC_VALUES_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_METRIC_VALUES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    GROUP_KEY_FIELD_NUMBER: _ClassVar[int]
    activation_info: NmsContext.ActivationInfo
    dataset_info: NmsContext.DatasetInfo
    targets: _containers.MessageMap[str, NmsContext.AlarmTarget]
    metric_values: _containers.MessageMap[str, NmsContext.AlarmMetricMap]
    previous_metric_values: _containers.MessageMap[str, NmsContext.AlarmMetricMap]
    device: _containers.ScalarMap[str, str]
    group_key: _containers.ScalarMap[str, str]
    def __init__(
        self,
        activation_info: _Optional[_Union[NmsContext.ActivationInfo, _Mapping]] = ...,
        dataset_info: _Optional[_Union[NmsContext.DatasetInfo, _Mapping]] = ...,
        targets: _Optional[_Mapping[str, NmsContext.AlarmTarget]] = ...,
        metric_values: _Optional[_Mapping[str, NmsContext.AlarmMetricMap]] = ...,
        previous_metric_values: _Optional[
            _Mapping[str, NmsContext.AlarmMetricMap]
        ] = ...,
        device: _Optional[_Mapping[str, str]] = ...,
        group_key: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class AlertServiceAddCommentRequest(_message.Message):
    __slots__ = ("alert_id", "text")
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    alert_id: str
    text: str
    def __init__(
        self, alert_id: _Optional[str] = ..., text: _Optional[str] = ...
    ) -> None: ...

class AlertServiceAddCommentResponse(_message.Message):
    __slots__ = ("comment",)
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    comment: _comment_pb2.Comment
    def __init__(
        self, comment: _Optional[_Union[_comment_pb2.Comment, _Mapping]] = ...
    ) -> None: ...

class AlertServiceListCommentsRequest(_message.Message):
    __slots__ = ("alert_id",)
    ALERT_ID_FIELD_NUMBER: _ClassVar[int]
    alert_id: str
    def __init__(self, alert_id: _Optional[str] = ...) -> None: ...

class AlertServiceListCommentsResponse(_message.Message):
    __slots__ = ("comments",)
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[_comment_pb2.Comment]
    def __init__(
        self,
        comments: _Optional[_Iterable[_Union[_comment_pb2.Comment, _Mapping]]] = ...,
    ) -> None: ...
