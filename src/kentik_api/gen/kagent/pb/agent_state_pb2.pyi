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

from kentik_api.gen.monitoring.pb import component_pb2 as _component_pb2

from . import agent_capabilities_pb2 as _agent_capabilities_pb2
from . import capability_pb2 as _capability_pb2
from . import capability_state_pb2 as _capability_state_pb2
from . import config_pb2 as _config_pb2
from . import resources_pb2 as _resources_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class CapabilityPromotionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CAPABILITY_PROMOTION_STATE_UNSPECIFIED: _ClassVar[CapabilityPromotionState]
    CAPABILITY_PROMOTION_STATE_PROMOTED: _ClassVar[CapabilityPromotionState]
    CAPABILITY_PROMOTION_STATE_PENDING: _ClassVar[CapabilityPromotionState]
    CAPABILITY_PROMOTION_STATE_ROLLED_BACK: _ClassVar[CapabilityPromotionState]

class AgentHealthState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGENT_HEALTH_STATE_UNSPECIFIED: _ClassVar[AgentHealthState]
    AGENT_HEALTH_STATE_HEALTHY: _ClassVar[AgentHealthState]
    AGENT_HEALTH_STATE_DEGRADED: _ClassVar[AgentHealthState]
    AGENT_HEALTH_STATE_UNHEALTHY: _ClassVar[AgentHealthState]
    AGENT_HEALTH_STATE_OFFLINE: _ClassVar[AgentHealthState]

class CapabilityHealthState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CAPABILITY_HEALTH_STATE_UNSPECIFIED: _ClassVar[CapabilityHealthState]
    CAPABILITY_HEALTH_STATE_HEALTHY: _ClassVar[CapabilityHealthState]
    CAPABILITY_HEALTH_STATE_DEGRADED: _ClassVar[CapabilityHealthState]
    CAPABILITY_HEALTH_STATE_UNHEALTHY: _ClassVar[CapabilityHealthState]
    CAPABILITY_HEALTH_STATE_DISABLED: _ClassVar[CapabilityHealthState]

class AgentHealthStateV2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGENT_HEALTH_STATE_V2_UNSPECIFIED: _ClassVar[AgentHealthStateV2]
    AGENT_HEALTH_STATE_V2_HEALTHY: _ClassVar[AgentHealthStateV2]
    AGENT_HEALTH_STATE_V2_WARNING: _ClassVar[AgentHealthStateV2]
    AGENT_HEALTH_STATE_V2_DEGRADED: _ClassVar[AgentHealthStateV2]
    AGENT_HEALTH_STATE_V2_CRITICAL: _ClassVar[AgentHealthStateV2]
    AGENT_HEALTH_STATE_V2_DOWN: _ClassVar[AgentHealthStateV2]

class CapabilityHealthStateV2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CAPABILITY_HEALTH_STATE_V2_UNSPECIFIED: _ClassVar[CapabilityHealthStateV2]
    CAPABILITY_HEALTH_STATE_V2_DISABLED: _ClassVar[CapabilityHealthStateV2]
    CAPABILITY_HEALTH_STATE_V2_HEALTHY: _ClassVar[CapabilityHealthStateV2]
    CAPABILITY_HEALTH_STATE_V2_WARNING: _ClassVar[CapabilityHealthStateV2]
    CAPABILITY_HEALTH_STATE_V2_DEGRADED: _ClassVar[CapabilityHealthStateV2]
    CAPABILITY_HEALTH_STATE_V2_CRITICAL: _ClassVar[CapabilityHealthStateV2]
    CAPABILITY_HEALTH_STATE_V2_DOWN: _ClassVar[CapabilityHealthStateV2]

CAPABILITY_PROMOTION_STATE_UNSPECIFIED: CapabilityPromotionState
CAPABILITY_PROMOTION_STATE_PROMOTED: CapabilityPromotionState
CAPABILITY_PROMOTION_STATE_PENDING: CapabilityPromotionState
CAPABILITY_PROMOTION_STATE_ROLLED_BACK: CapabilityPromotionState
AGENT_HEALTH_STATE_UNSPECIFIED: AgentHealthState
AGENT_HEALTH_STATE_HEALTHY: AgentHealthState
AGENT_HEALTH_STATE_DEGRADED: AgentHealthState
AGENT_HEALTH_STATE_UNHEALTHY: AgentHealthState
AGENT_HEALTH_STATE_OFFLINE: AgentHealthState
CAPABILITY_HEALTH_STATE_UNSPECIFIED: CapabilityHealthState
CAPABILITY_HEALTH_STATE_HEALTHY: CapabilityHealthState
CAPABILITY_HEALTH_STATE_DEGRADED: CapabilityHealthState
CAPABILITY_HEALTH_STATE_UNHEALTHY: CapabilityHealthState
CAPABILITY_HEALTH_STATE_DISABLED: CapabilityHealthState
AGENT_HEALTH_STATE_V2_UNSPECIFIED: AgentHealthStateV2
AGENT_HEALTH_STATE_V2_HEALTHY: AgentHealthStateV2
AGENT_HEALTH_STATE_V2_WARNING: AgentHealthStateV2
AGENT_HEALTH_STATE_V2_DEGRADED: AgentHealthStateV2
AGENT_HEALTH_STATE_V2_CRITICAL: AgentHealthStateV2
AGENT_HEALTH_STATE_V2_DOWN: AgentHealthStateV2
CAPABILITY_HEALTH_STATE_V2_UNSPECIFIED: CapabilityHealthStateV2
CAPABILITY_HEALTH_STATE_V2_DISABLED: CapabilityHealthStateV2
CAPABILITY_HEALTH_STATE_V2_HEALTHY: CapabilityHealthStateV2
CAPABILITY_HEALTH_STATE_V2_WARNING: CapabilityHealthStateV2
CAPABILITY_HEALTH_STATE_V2_DEGRADED: CapabilityHealthStateV2
CAPABILITY_HEALTH_STATE_V2_CRITICAL: CapabilityHealthStateV2
CAPABILITY_HEALTH_STATE_V2_DOWN: CapabilityHealthStateV2

class AgentDesiredState(_message.Message):
    __slots__ = ("agent", "capabilities", "version", "current_time")
    class CapabilityState(_message.Message):
        __slots__ = ("capability", "group", "release", "config")
        CAPABILITY_FIELD_NUMBER: _ClassVar[int]
        GROUP_FIELD_NUMBER: _ClassVar[int]
        RELEASE_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        capability: _agent_capabilities_pb2.AgentCapability
        group: _agent_capabilities_pb2.AgentCapabilityGroup
        release: _capability_pb2.CapabilityRelease
        config: _config_pb2.Config
        def __init__(
            self,
            capability: _Optional[
                _Union[_agent_capabilities_pb2.AgentCapability, _Mapping]
            ] = ...,
            group: _Optional[
                _Union[_agent_capabilities_pb2.AgentCapabilityGroup, _Mapping]
            ] = ...,
            release: _Optional[
                _Union[_capability_pb2.CapabilityRelease, _Mapping]
            ] = ...,
            config: _Optional[_Union[_config_pb2.Config, _Mapping]] = ...,
        ) -> None: ...

    class AgentState(_message.Message):
        __slots__ = (
            "version",
            "channel",
            "bundle_id",
            "config_id",
            "release",
            "config",
        )
        VERSION_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_FIELD_NUMBER: _ClassVar[int]
        BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
        CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
        RELEASE_FIELD_NUMBER: _ClassVar[int]
        CONFIG_FIELD_NUMBER: _ClassVar[int]
        version: str
        channel: str
        bundle_id: str
        config_id: str
        release: _capability_pb2.CapabilityRelease
        config: _config_pb2.Config
        def __init__(
            self,
            version: _Optional[str] = ...,
            channel: _Optional[str] = ...,
            bundle_id: _Optional[str] = ...,
            config_id: _Optional[str] = ...,
            release: _Optional[
                _Union[_capability_pb2.CapabilityRelease, _Mapping]
            ] = ...,
            config: _Optional[_Union[_config_pb2.Config, _Mapping]] = ...,
        ) -> None: ...

    AGENT_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
    agent: AgentDesiredState.AgentState
    capabilities: _containers.RepeatedCompositeFieldContainer[
        AgentDesiredState.CapabilityState
    ]
    version: int
    current_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        agent: _Optional[_Union[AgentDesiredState.AgentState, _Mapping]] = ...,
        capabilities: _Optional[
            _Iterable[_Union[AgentDesiredState.CapabilityState, _Mapping]]
        ] = ...,
        version: _Optional[int] = ...,
        current_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class AgentCurrentState(_message.Message):
    __slots__ = ("agent", "capabilities")
    class AgentState(_message.Message):
        __slots__ = (
            "version",
            "bundle_id",
            "config_id",
            "config_version",
            "supervisor_version",
            "last_seen",
            "reconcile_error",
            "reconcile_interval",
            "last_error",
            "pid",
            "started_at",
            "current_time",
            "health",
            "health_v2",
            "os_distribution",
            "privileges",
            "resources",
            "host_resources",
            "promotion_state",
            "facts",
            "health_fingerprint",
            "mem_used_percent",
            "mem_free_bytes",
            "cpu_total_cores",
            "cpu_used_percent",
            "disk_used_percent",
            "disk_free_bytes",
        )
        class HealthFingerprintEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: _component_pb2.HealthStatus
            def __init__(
                self,
                key: _Optional[str] = ...,
                value: _Optional[_Union[_component_pb2.HealthStatus, str]] = ...,
            ) -> None: ...

        VERSION_FIELD_NUMBER: _ClassVar[int]
        BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
        CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
        CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
        SUPERVISOR_VERSION_FIELD_NUMBER: _ClassVar[int]
        LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
        RECONCILE_ERROR_FIELD_NUMBER: _ClassVar[int]
        RECONCILE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        LAST_ERROR_FIELD_NUMBER: _ClassVar[int]
        PID_FIELD_NUMBER: _ClassVar[int]
        STARTED_AT_FIELD_NUMBER: _ClassVar[int]
        CURRENT_TIME_FIELD_NUMBER: _ClassVar[int]
        HEALTH_FIELD_NUMBER: _ClassVar[int]
        HEALTH_V2_FIELD_NUMBER: _ClassVar[int]
        OS_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
        PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
        RESOURCES_FIELD_NUMBER: _ClassVar[int]
        HOST_RESOURCES_FIELD_NUMBER: _ClassVar[int]
        PROMOTION_STATE_FIELD_NUMBER: _ClassVar[int]
        FACTS_FIELD_NUMBER: _ClassVar[int]
        HEALTH_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
        MEM_USED_PERCENT_FIELD_NUMBER: _ClassVar[int]
        MEM_FREE_BYTES_FIELD_NUMBER: _ClassVar[int]
        CPU_TOTAL_CORES_FIELD_NUMBER: _ClassVar[int]
        CPU_USED_PERCENT_FIELD_NUMBER: _ClassVar[int]
        DISK_USED_PERCENT_FIELD_NUMBER: _ClassVar[int]
        DISK_FREE_BYTES_FIELD_NUMBER: _ClassVar[int]
        version: str
        bundle_id: str
        config_id: str
        config_version: str
        supervisor_version: str
        last_seen: _timestamp_pb2.Timestamp
        reconcile_error: str
        reconcile_interval: _duration_pb2.Duration
        last_error: str
        pid: int
        started_at: _timestamp_pb2.Timestamp
        current_time: _timestamp_pb2.Timestamp
        health: AgentHealthState
        health_v2: AgentHealthStateV2
        os_distribution: str
        privileges: str
        resources: _resources_pb2.ProcessResources
        host_resources: _resources_pb2.HostResources
        promotion_state: CapabilityPromotionState
        facts: _containers.RepeatedCompositeFieldContainer[CapabilityFact]
        health_fingerprint: _containers.ScalarMap[str, _component_pb2.HealthStatus]
        mem_used_percent: float
        mem_free_bytes: int
        cpu_total_cores: int
        cpu_used_percent: float
        disk_used_percent: float
        disk_free_bytes: int
        def __init__(
            self,
            version: _Optional[str] = ...,
            bundle_id: _Optional[str] = ...,
            config_id: _Optional[str] = ...,
            config_version: _Optional[str] = ...,
            supervisor_version: _Optional[str] = ...,
            last_seen: _Optional[
                _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
            ] = ...,
            reconcile_error: _Optional[str] = ...,
            reconcile_interval: _Optional[
                _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
            ] = ...,
            last_error: _Optional[str] = ...,
            pid: _Optional[int] = ...,
            started_at: _Optional[
                _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
            ] = ...,
            current_time: _Optional[
                _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
            ] = ...,
            health: _Optional[_Union[AgentHealthState, str]] = ...,
            health_v2: _Optional[_Union[AgentHealthStateV2, str]] = ...,
            os_distribution: _Optional[str] = ...,
            privileges: _Optional[str] = ...,
            resources: _Optional[
                _Union[_resources_pb2.ProcessResources, _Mapping]
            ] = ...,
            host_resources: _Optional[
                _Union[_resources_pb2.HostResources, _Mapping]
            ] = ...,
            promotion_state: _Optional[_Union[CapabilityPromotionState, str]] = ...,
            facts: _Optional[_Iterable[_Union[CapabilityFact, _Mapping]]] = ...,
            health_fingerprint: _Optional[
                _Mapping[str, _component_pb2.HealthStatus]
            ] = ...,
            mem_used_percent: _Optional[float] = ...,
            mem_free_bytes: _Optional[int] = ...,
            cpu_total_cores: _Optional[int] = ...,
            cpu_used_percent: _Optional[float] = ...,
            disk_used_percent: _Optional[float] = ...,
            disk_free_bytes: _Optional[int] = ...,
        ) -> None: ...

    AGENT_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    agent: AgentCurrentState.AgentState
    capabilities: _containers.RepeatedCompositeFieldContainer[CapabilityCurrentState]
    def __init__(
        self,
        agent: _Optional[_Union[AgentCurrentState.AgentState, _Mapping]] = ...,
        capabilities: _Optional[
            _Iterable[_Union[CapabilityCurrentState, _Mapping]]
        ] = ...,
    ) -> None: ...

class OSMetadata(_message.Message):
    __slots__ = ("name", "vendor", "release", "version", "release_metadata")
    class ReleaseMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RELEASE_METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    vendor: str
    release: str
    version: str
    release_metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        vendor: _Optional[str] = ...,
        release: _Optional[str] = ...,
        version: _Optional[str] = ...,
        release_metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class CapabilityCurrentState(_message.Message):
    __slots__ = (
        "name",
        "version",
        "installed",
        "running",
        "bundle_id",
        "restarts",
        "crash_loop_count",
        "restart_loop_count",
        "last_error",
        "pid",
        "config_id",
        "group_id",
        "config_version",
        "privileges",
        "started_at",
        "stopped_at",
        "health",
        "health_v2",
        "enabled",
        "state",
        "cpu_used_cores",
        "mem_used_bytes",
        "resources",
        "promotion_state",
        "facts",
        "health_fingerprint",
    )
    class HealthFingerprintEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _component_pb2.HealthStatus
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[_component_pb2.HealthStatus, str]] = ...,
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    INSTALLED_FIELD_NUMBER: _ClassVar[int]
    RUNNING_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
    RESTARTS_FIELD_NUMBER: _ClassVar[int]
    CRASH_LOOP_COUNT_FIELD_NUMBER: _ClassVar[int]
    RESTART_LOOP_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_ERROR_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    PRIVILEGES_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STOPPED_AT_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    HEALTH_V2_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CPU_USED_CORES_FIELD_NUMBER: _ClassVar[int]
    MEM_USED_BYTES_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PROMOTION_STATE_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    installed: bool
    running: bool
    bundle_id: str
    restarts: int
    crash_loop_count: int
    restart_loop_count: int
    last_error: str
    pid: int
    config_id: str
    group_id: str
    config_version: str
    privileges: str
    started_at: _timestamp_pb2.Timestamp
    stopped_at: _timestamp_pb2.Timestamp
    health: CapabilityHealthState
    health_v2: CapabilityHealthStateV2
    enabled: bool
    state: _capability_state_pb2.CapabilityState
    cpu_used_cores: float
    mem_used_bytes: int
    resources: _resources_pb2.ProcessResources
    promotion_state: CapabilityPromotionState
    facts: _containers.RepeatedCompositeFieldContainer[CapabilityFact]
    health_fingerprint: _containers.ScalarMap[str, _component_pb2.HealthStatus]
    def __init__(
        self,
        name: _Optional[str] = ...,
        version: _Optional[str] = ...,
        installed: _Optional[bool] = ...,
        running: _Optional[bool] = ...,
        bundle_id: _Optional[str] = ...,
        restarts: _Optional[int] = ...,
        crash_loop_count: _Optional[int] = ...,
        restart_loop_count: _Optional[int] = ...,
        last_error: _Optional[str] = ...,
        pid: _Optional[int] = ...,
        config_id: _Optional[str] = ...,
        group_id: _Optional[str] = ...,
        config_version: _Optional[str] = ...,
        privileges: _Optional[str] = ...,
        started_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        stopped_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        health: _Optional[_Union[CapabilityHealthState, str]] = ...,
        health_v2: _Optional[_Union[CapabilityHealthStateV2, str]] = ...,
        enabled: _Optional[bool] = ...,
        state: _Optional[_Union[_capability_state_pb2.CapabilityState, _Mapping]] = ...,
        cpu_used_cores: _Optional[float] = ...,
        mem_used_bytes: _Optional[int] = ...,
        resources: _Optional[_Union[_resources_pb2.ProcessResources, _Mapping]] = ...,
        promotion_state: _Optional[_Union[CapabilityPromotionState, str]] = ...,
        facts: _Optional[_Iterable[_Union[CapabilityFact, _Mapping]]] = ...,
        health_fingerprint: _Optional[_Mapping[str, _component_pb2.HealthStatus]] = ...,
    ) -> None: ...

class CapabilityFact(_message.Message):
    __slots__ = ("path", "fact")
    PATH_FIELD_NUMBER: _ClassVar[int]
    FACT_FIELD_NUMBER: _ClassVar[int]
    path: str
    fact: _component_pb2.Fact
    def __init__(
        self,
        path: _Optional[str] = ...,
        fact: _Optional[_Union[_component_pb2.Fact, _Mapping]] = ...,
    ) -> None: ...
