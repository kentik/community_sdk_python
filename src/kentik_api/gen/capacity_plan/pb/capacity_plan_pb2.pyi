from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Config(_message.Message):
    __slots__ = ("runout", "utilization")
    class RunoutConfig(_message.Message):
        __slots__ = ("strategy", "warn_qty", "crit_qty")
        STRATEGY_FIELD_NUMBER: _ClassVar[int]
        WARN_QTY_FIELD_NUMBER: _ClassVar[int]
        CRIT_QTY_FIELD_NUMBER: _ClassVar[int]
        strategy: str
        warn_qty: int
        crit_qty: int
        def __init__(
            self,
            strategy: _Optional[str] = ...,
            warn_qty: _Optional[int] = ...,
            crit_qty: _Optional[int] = ...,
        ) -> None: ...

    class UtilConfig(_message.Message):
        __slots__ = ("aggregate", "warn_pct", "crit_pct")
        AGGREGATE_FIELD_NUMBER: _ClassVar[int]
        WARN_PCT_FIELD_NUMBER: _ClassVar[int]
        CRIT_PCT_FIELD_NUMBER: _ClassVar[int]
        aggregate: str
        warn_pct: int
        crit_pct: int
        def __init__(
            self,
            aggregate: _Optional[str] = ...,
            warn_pct: _Optional[int] = ...,
            crit_pct: _Optional[int] = ...,
        ) -> None: ...

    RUNOUT_FIELD_NUMBER: _ClassVar[int]
    UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    runout: Config.RunoutConfig
    utilization: Config.UtilConfig
    def __init__(
        self,
        runout: _Optional[_Union[Config.RunoutConfig, _Mapping]] = ...,
        utilization: _Optional[_Union[Config.UtilConfig, _Mapping]] = ...,
    ) -> None: ...

class SummaryStatus(_message.Message):
    __slots__ = ("runout", "utilization")
    class RunoutStatus(_message.Message):
        __slots__ = ("status", "earliest_date")
        STATUS_FIELD_NUMBER: _ClassVar[int]
        EARLIEST_DATE_FIELD_NUMBER: _ClassVar[int]
        status: str
        earliest_date: int
        def __init__(
            self, status: _Optional[str] = ..., earliest_date: _Optional[int] = ...
        ) -> None: ...

    class UtilStatus(_message.Message):
        __slots__ = ("status", "highest_pct")
        STATUS_FIELD_NUMBER: _ClassVar[int]
        HIGHEST_PCT_FIELD_NUMBER: _ClassVar[int]
        status: str
        highest_pct: int
        def __init__(
            self, status: _Optional[str] = ..., highest_pct: _Optional[int] = ...
        ) -> None: ...

    RUNOUT_FIELD_NUMBER: _ClassVar[int]
    UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    runout: SummaryStatus.RunoutStatus
    utilization: SummaryStatus.UtilStatus
    def __init__(
        self,
        runout: _Optional[_Union[SummaryStatus.RunoutStatus, _Mapping]] = ...,
        utilization: _Optional[_Union[SummaryStatus.UtilStatus, _Mapping]] = ...,
    ) -> None: ...

class CapacitySummary(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "status",
        "interfaces",
        "config",
        "summary_status",
    )
    class InterfacesDetail(_message.Message):
        __slots__ = (
            "total_count",
            "total_capacity_bps",
            "healthy",
            "warning",
            "critical",
        )
        class StatusDetail(_message.Message):
            __slots__ = ("bps", "count")
            BPS_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            bps: int
            count: int
            def __init__(
                self, bps: _Optional[int] = ..., count: _Optional[int] = ...
            ) -> None: ...

        TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_CAPACITY_BPS_FIELD_NUMBER: _ClassVar[int]
        HEALTHY_FIELD_NUMBER: _ClassVar[int]
        WARNING_FIELD_NUMBER: _ClassVar[int]
        CRITICAL_FIELD_NUMBER: _ClassVar[int]
        total_count: int
        total_capacity_bps: int
        healthy: CapacitySummary.InterfacesDetail.StatusDetail
        warning: CapacitySummary.InterfacesDetail.StatusDetail
        critical: CapacitySummary.InterfacesDetail.StatusDetail
        def __init__(
            self,
            total_count: _Optional[int] = ...,
            total_capacity_bps: _Optional[int] = ...,
            healthy: _Optional[
                _Union[CapacitySummary.InterfacesDetail.StatusDetail, _Mapping]
            ] = ...,
            warning: _Optional[
                _Union[CapacitySummary.InterfacesDetail.StatusDetail, _Mapping]
            ] = ...,
            critical: _Optional[
                _Union[CapacitySummary.InterfacesDetail.StatusDetail, _Mapping]
            ] = ...,
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    status: str
    interfaces: CapacitySummary.InterfacesDetail
    config: Config
    summary_status: SummaryStatus
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        status: _Optional[str] = ...,
        interfaces: _Optional[_Union[CapacitySummary.InterfacesDetail, _Mapping]] = ...,
        config: _Optional[_Union[Config, _Mapping]] = ...,
        summary_status: _Optional[_Union[SummaryStatus, _Mapping]] = ...,
    ) -> None: ...

class CapacityPlan(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "status",
        "interfaces",
        "config",
        "summary_status",
    )
    class InterfaceDetail(_message.Message):
        __slots__ = (
            "device_name",
            "intf_name",
            "intf_description",
            "intf_capacity",
            "network_boundary",
            "conn_type",
            "provider",
            "util_status",
            "util_out_mbps",
            "util_out_pct",
            "util_in_mbps",
            "util_in_pct",
            "runout_status",
            "runout_in_date",
            "runout_in_variation",
            "runout_out_date",
            "runout_out_variation",
        )
        DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
        INTF_NAME_FIELD_NUMBER: _ClassVar[int]
        INTF_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        INTF_CAPACITY_FIELD_NUMBER: _ClassVar[int]
        NETWORK_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
        CONN_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROVIDER_FIELD_NUMBER: _ClassVar[int]
        UTIL_STATUS_FIELD_NUMBER: _ClassVar[int]
        UTIL_OUT_MBPS_FIELD_NUMBER: _ClassVar[int]
        UTIL_OUT_PCT_FIELD_NUMBER: _ClassVar[int]
        UTIL_IN_MBPS_FIELD_NUMBER: _ClassVar[int]
        UTIL_IN_PCT_FIELD_NUMBER: _ClassVar[int]
        RUNOUT_STATUS_FIELD_NUMBER: _ClassVar[int]
        RUNOUT_IN_DATE_FIELD_NUMBER: _ClassVar[int]
        RUNOUT_IN_VARIATION_FIELD_NUMBER: _ClassVar[int]
        RUNOUT_OUT_DATE_FIELD_NUMBER: _ClassVar[int]
        RUNOUT_OUT_VARIATION_FIELD_NUMBER: _ClassVar[int]
        device_name: str
        intf_name: str
        intf_description: str
        intf_capacity: str
        network_boundary: str
        conn_type: str
        provider: str
        util_status: str
        util_out_mbps: str
        util_out_pct: str
        util_in_mbps: str
        util_in_pct: str
        runout_status: str
        runout_in_date: str
        runout_in_variation: str
        runout_out_date: str
        runout_out_variation: str
        def __init__(
            self,
            device_name: _Optional[str] = ...,
            intf_name: _Optional[str] = ...,
            intf_description: _Optional[str] = ...,
            intf_capacity: _Optional[str] = ...,
            network_boundary: _Optional[str] = ...,
            conn_type: _Optional[str] = ...,
            provider: _Optional[str] = ...,
            util_status: _Optional[str] = ...,
            util_out_mbps: _Optional[str] = ...,
            util_out_pct: _Optional[str] = ...,
            util_in_mbps: _Optional[str] = ...,
            util_in_pct: _Optional[str] = ...,
            runout_status: _Optional[str] = ...,
            runout_in_date: _Optional[str] = ...,
            runout_in_variation: _Optional[str] = ...,
            runout_out_date: _Optional[str] = ...,
            runout_out_variation: _Optional[str] = ...,
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    status: str
    interfaces: _containers.RepeatedCompositeFieldContainer[
        CapacityPlan.InterfaceDetail
    ]
    config: Config
    summary_status: SummaryStatus
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        status: _Optional[str] = ...,
        interfaces: _Optional[
            _Iterable[_Union[CapacityPlan.InterfaceDetail, _Mapping]]
        ] = ...,
        config: _Optional[_Union[Config, _Mapping]] = ...,
        summary_status: _Optional[_Union[SummaryStatus, _Mapping]] = ...,
    ) -> None: ...

class ListCapacitySummariesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCapacitySummariesResponse(_message.Message):
    __slots__ = ("capacity", "invalid_count")
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    capacity: _containers.RepeatedCompositeFieldContainer[CapacitySummary]
    invalid_count: int
    def __init__(
        self,
        capacity: _Optional[_Iterable[_Union[CapacitySummary, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetCapacitySummaryRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCapacitySummaryResponse(_message.Message):
    __slots__ = ("capacity",)
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    capacity: CapacitySummary
    def __init__(
        self, capacity: _Optional[_Union[CapacitySummary, _Mapping]] = ...
    ) -> None: ...

class ListCapacityPlansRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCapacityPlansResponse(_message.Message):
    __slots__ = ("capacity", "invalid_count")
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    capacity: _containers.RepeatedCompositeFieldContainer[CapacityPlan]
    invalid_count: int
    def __init__(
        self,
        capacity: _Optional[_Iterable[_Union[CapacityPlan, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetCapacityPlanRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetCapacityPlanResponse(_message.Message):
    __slots__ = ("capacity",)
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    capacity: CapacityPlan
    def __init__(
        self, capacity: _Optional[_Union[CapacityPlan, _Mapping]] = ...
    ) -> None: ...
