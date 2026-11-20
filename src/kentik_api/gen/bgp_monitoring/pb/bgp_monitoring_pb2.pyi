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

from kentik_api.gen.core.pb import user_info_pb2 as _user_info_pb2
from kentik_api.gen.net.pb import bgp_types_pb2 as _bgp_types_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class BgpMonitorStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BGP_MONITOR_STATUS_UNSPECIFIED: _ClassVar[BgpMonitorStatus]
    BGP_MONITOR_STATUS_ACTIVE: _ClassVar[BgpMonitorStatus]
    BGP_MONITOR_STATUS_PAUSED: _ClassVar[BgpMonitorStatus]
    BGP_MONITOR_STATUS_DELETED: _ClassVar[BgpMonitorStatus]

class BgpMetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BGP_METRIC_TYPE_UNSPECIFIED: _ClassVar[BgpMetricType]
    BGP_METRIC_TYPE_REACHABILITY: _ClassVar[BgpMetricType]
    BGP_METRIC_TYPE_PATH_CHANGES: _ClassVar[BgpMetricType]

BGP_MONITOR_STATUS_UNSPECIFIED: BgpMonitorStatus
BGP_MONITOR_STATUS_ACTIVE: BgpMonitorStatus
BGP_MONITOR_STATUS_PAUSED: BgpMonitorStatus
BGP_MONITOR_STATUS_DELETED: BgpMonitorStatus
BGP_METRIC_TYPE_UNSPECIFIED: BgpMetricType
BGP_METRIC_TYPE_REACHABILITY: BgpMetricType
BGP_METRIC_TYPE_PATH_CHANGES: BgpMetricType

class Nlri(_message.Message):
    __slots__ = ("afi", "safi", "prefix")
    AFI_FIELD_NUMBER: _ClassVar[int]
    SAFI_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    afi: _bgp_types_pb2.Afi
    safi: _bgp_types_pb2.Safi
    prefix: str
    def __init__(
        self,
        afi: _Optional[_Union[_bgp_types_pb2.Afi, str]] = ...,
        safi: _Optional[_Union[_bgp_types_pb2.Safi, str]] = ...,
        prefix: _Optional[str] = ...,
    ) -> None: ...

class BgpHealthSettings(_message.Message):
    __slots__ = ("reachability_warning", "reachability_critical")
    REACHABILITY_WARNING_FIELD_NUMBER: _ClassVar[int]
    REACHABILITY_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    reachability_warning: float
    reachability_critical: float
    def __init__(
        self,
        reachability_warning: _Optional[float] = ...,
        reachability_critical: _Optional[float] = ...,
    ) -> None: ...

class BgpMonitorSettings(_message.Message):
    __slots__ = (
        "allowed_asns",
        "targets",
        "check_rpki",
        "include_covered_prefixes",
        "health_settings",
        "notification_channels",
        "notes",
        "allowed_upstreams",
    )
    ALLOWED_ASNS_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    CHECK_RPKI_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_COVERED_PREFIXES_FIELD_NUMBER: _ClassVar[int]
    HEALTH_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_UPSTREAMS_FIELD_NUMBER: _ClassVar[int]
    allowed_asns: _containers.RepeatedScalarFieldContainer[int]
    targets: _containers.RepeatedCompositeFieldContainer[Nlri]
    check_rpki: bool
    include_covered_prefixes: bool
    health_settings: BgpHealthSettings
    notification_channels: _containers.RepeatedScalarFieldContainer[str]
    notes: str
    allowed_upstreams: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        allowed_asns: _Optional[_Iterable[int]] = ...,
        targets: _Optional[_Iterable[_Union[Nlri, _Mapping]]] = ...,
        check_rpki: _Optional[bool] = ...,
        include_covered_prefixes: _Optional[bool] = ...,
        health_settings: _Optional[_Union[BgpHealthSettings, _Mapping]] = ...,
        notification_channels: _Optional[_Iterable[str]] = ...,
        notes: _Optional[str] = ...,
        allowed_upstreams: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class BgpMonitor(_message.Message):
    __slots__ = (
        "id",
        "name",
        "status",
        "settings",
        "cdate",
        "edate",
        "created_by",
        "last_updated_by",
        "labels",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    status: BgpMonitorStatus
    settings: BgpMonitorSettings
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    created_by: _user_info_pb2.UserInfo
    last_updated_by: _user_info_pb2.UserInfo
    labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        status: _Optional[_Union[BgpMonitorStatus, str]] = ...,
        settings: _Optional[_Union[BgpMonitorSettings, _Mapping]] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        created_by: _Optional[_Union[_user_info_pb2.UserInfo, _Mapping]] = ...,
        last_updated_by: _Optional[_Union[_user_info_pb2.UserInfo, _Mapping]] = ...,
        labels: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class RouteInfo(_message.Message):
    __slots__ = (
        "nlri",
        "origin_asn",
        "as_path",
        "vantage_point",
        "rpki_status",
        "nexthop",
    )
    NLRI_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_ASN_FIELD_NUMBER: _ClassVar[int]
    AS_PATH_FIELD_NUMBER: _ClassVar[int]
    VANTAGE_POINT_FIELD_NUMBER: _ClassVar[int]
    RPKI_STATUS_FIELD_NUMBER: _ClassVar[int]
    NEXTHOP_FIELD_NUMBER: _ClassVar[int]
    nlri: Nlri
    origin_asn: int
    as_path: _containers.RepeatedScalarFieldContainer[str]
    vantage_point: _bgp_types_pb2.VantagePoint
    rpki_status: _bgp_types_pb2.RpkiStatus
    nexthop: str
    def __init__(
        self,
        nlri: _Optional[_Union[Nlri, _Mapping]] = ...,
        origin_asn: _Optional[int] = ...,
        as_path: _Optional[_Iterable[str]] = ...,
        vantage_point: _Optional[_Union[_bgp_types_pb2.VantagePoint, _Mapping]] = ...,
        rpki_status: _Optional[_Union[_bgp_types_pb2.RpkiStatus, str]] = ...,
        nexthop: _Optional[str] = ...,
    ) -> None: ...

class BgpMetric(_message.Message):
    __slots__ = ("timestamp", "nlri", "reachability", "path_changes")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NLRI_FIELD_NUMBER: _ClassVar[int]
    REACHABILITY_FIELD_NUMBER: _ClassVar[int]
    PATH_CHANGES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    nlri: Nlri
    reachability: float
    path_changes: int
    def __init__(
        self,
        timestamp: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        nlri: _Optional[_Union[Nlri, _Mapping]] = ...,
        reachability: _Optional[float] = ...,
        path_changes: _Optional[int] = ...,
    ) -> None: ...

class ListMonitorsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMonitorsResponse(_message.Message):
    __slots__ = ("monitors", "invalid_count")
    MONITORS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    monitors: _containers.RepeatedCompositeFieldContainer[BgpMonitor]
    invalid_count: int
    def __init__(
        self,
        monitors: _Optional[_Iterable[_Union[BgpMonitor, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class CreateMonitorRequest(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: BgpMonitor
    def __init__(
        self, monitor: _Optional[_Union[BgpMonitor, _Mapping]] = ...
    ) -> None: ...

class CreateMonitorResponse(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: BgpMonitor
    def __init__(
        self, monitor: _Optional[_Union[BgpMonitor, _Mapping]] = ...
    ) -> None: ...

class GetMonitorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetMonitorResponse(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: BgpMonitor
    def __init__(
        self, monitor: _Optional[_Union[BgpMonitor, _Mapping]] = ...
    ) -> None: ...

class UpdateMonitorRequest(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: BgpMonitor
    def __init__(
        self, monitor: _Optional[_Union[BgpMonitor, _Mapping]] = ...
    ) -> None: ...

class UpdateMonitorResponse(_message.Message):
    __slots__ = ("monitor",)
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    monitor: BgpMonitor
    def __init__(
        self, monitor: _Optional[_Union[BgpMonitor, _Mapping]] = ...
    ) -> None: ...

class DeleteMonitorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteMonitorResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetMonitorStatusRequest(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: BgpMonitorStatus
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[BgpMonitorStatus, str]] = ...,
    ) -> None: ...

class SetMonitorStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetMetricsForTargetRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "target", "include_covered", "metrics")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_COVERED_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    target: Nlri
    include_covered: bool
    metrics: _containers.RepeatedScalarFieldContainer[BgpMetricType]
    def __init__(
        self,
        start_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        target: _Optional[_Union[Nlri, _Mapping]] = ...,
        include_covered: _Optional[bool] = ...,
        metrics: _Optional[_Iterable[_Union[BgpMetricType, str]]] = ...,
    ) -> None: ...

class GetMetricsForTargetResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[BgpMetric]
    def __init__(
        self, metrics: _Optional[_Iterable[_Union[BgpMetric, _Mapping]]] = ...
    ) -> None: ...

class GetRoutesForTargetRequest(_message.Message):
    __slots__ = ("time", "target", "include_covered", "check_rpki")
    TIME_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_COVERED_FIELD_NUMBER: _ClassVar[int]
    CHECK_RPKI_FIELD_NUMBER: _ClassVar[int]
    time: _timestamp_pb2.Timestamp
    target: Nlri
    include_covered: bool
    check_rpki: bool
    def __init__(
        self,
        time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        target: _Optional[_Union[Nlri, _Mapping]] = ...,
        include_covered: _Optional[bool] = ...,
        check_rpki: _Optional[bool] = ...,
    ) -> None: ...

class GetRoutesForTargetResponse(_message.Message):
    __slots__ = ("routes", "as_names")
    class AsNamesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(
            self, key: _Optional[int] = ..., value: _Optional[str] = ...
        ) -> None: ...

    ROUTES_FIELD_NUMBER: _ClassVar[int]
    AS_NAMES_FIELD_NUMBER: _ClassVar[int]
    routes: _containers.RepeatedCompositeFieldContainer[RouteInfo]
    as_names: _containers.ScalarMap[int, str]
    def __init__(
        self,
        routes: _Optional[_Iterable[_Union[RouteInfo, _Mapping]]] = ...,
        as_names: _Optional[_Mapping[int, str]] = ...,
    ) -> None: ...
