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

DESCRIPTOR: _descriptor.FileDescriptor

class LifecyclePhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LIFECYCLE_PHASE_UNSPECIFIED: _ClassVar[LifecyclePhase]
    LIFECYCLE_PHASE_INITIALIZING: _ClassVar[LifecyclePhase]
    LIFECYCLE_PHASE_RUNNING: _ClassVar[LifecyclePhase]
    LIFECYCLE_PHASE_TERMINATING: _ClassVar[LifecyclePhase]
    LIFECYCLE_PHASE_TERMINATED: _ClassVar[LifecyclePhase]

class HealthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTH_STATUS_UNSPECIFIED: _ClassVar[HealthStatus]
    HEALTH_STATUS_HEALTHY: _ClassVar[HealthStatus]
    HEALTH_STATUS_WARNING: _ClassVar[HealthStatus]
    HEALTH_STATUS_DEGRADED: _ClassVar[HealthStatus]
    HEALTH_STATUS_CRITICAL: _ClassVar[HealthStatus]
    HEALTH_STATUS_DOWN: _ClassVar[HealthStatus]

class MetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_TYPE_UNSPECIFIED: _ClassVar[MetricType]
    METRIC_TYPE_GAUGE: _ClassVar[MetricType]
    METRIC_TYPE_COUNTER: _ClassVar[MetricType]
    METRIC_TYPE_HISTOGRAM: _ClassVar[MetricType]

class MetricEntity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_ENTITY_UNSPECIFIED: _ClassVar[MetricEntity]
    METRIC_ENTITY_REQUESTS: _ClassVar[MetricEntity]
    METRIC_ENTITY_QUERIES: _ClassVar[MetricEntity]
    METRIC_ENTITY_FLOWS: _ClassVar[MetricEntity]
    METRIC_ENTITY_CONNECTIONS: _ClassVar[MetricEntity]
    METRIC_ENTITY_PACKETS: _ClassVar[MetricEntity]
    METRIC_ENTITY_BYTES: _ClassVar[MetricEntity]
    METRIC_ENTITY_READS: _ClassVar[MetricEntity]
    METRIC_ENTITY_WRITES: _ClassVar[MetricEntity]
    METRIC_ENTITY_TRANSACTIONS: _ClassVar[MetricEntity]
    METRIC_ENTITY_RECORDS: _ClassVar[MetricEntity]
    METRIC_ENTITY_MESSAGES: _ClassVar[MetricEntity]
    METRIC_ENTITY_EVENTS: _ClassVar[MetricEntity]
    METRIC_ENTITY_LOGS: _ClassVar[MetricEntity]
    METRIC_ENTITY_TASKS: _ClassVar[MetricEntity]
    METRIC_ENTITY_OPERATIONS: _ClassVar[MetricEntity]
    METRIC_ENTITY_BATCHES: _ClassVar[MetricEntity]
    METRIC_ENTITY_ITEMS: _ClassVar[MetricEntity]
    METRIC_ENTITY_DATA: _ClassVar[MetricEntity]
    METRIC_ENTITY_BLOCKS: _ClassVar[MetricEntity]
    METRIC_ENTITY_REPLICAS: _ClassVar[MetricEntity]
    METRIC_ENTITY_SNAPSHOTS: _ClassVar[MetricEntity]
    METRIC_ENTITY_THREADS: _ClassVar[MetricEntity]
    METRIC_ENTITY_PROCESSES: _ClassVar[MetricEntity]
    METRIC_ENTITY_GOROUTINES: _ClassVar[MetricEntity]
    METRIC_ENTITY_LOCKS: _ClassVar[MetricEntity]
    METRIC_ENTITY_SESSIONS: _ClassVar[MetricEntity]
    METRIC_ENTITY_USERS: _ClassVar[MetricEntity]
    METRIC_ENTITY_CLIENTS: _ClassVar[MetricEntity]
    METRIC_ENTITY_ERRORS: _ClassVar[MetricEntity]
    METRIC_ENTITY_SPANS: _ClassVar[MetricEntity]
    METRIC_ENTITY_ALERTS: _ClassVar[MetricEntity]

class MetricMeasurement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_MEASUREMENT_UNSPECIFIED: _ClassVar[MetricMeasurement]
    METRIC_MEASUREMENT_COUNT: _ClassVar[MetricMeasurement]
    METRIC_MEASUREMENT_DURATION: _ClassVar[MetricMeasurement]
    METRIC_MEASUREMENT_SIZE: _ClassVar[MetricMeasurement]
    METRIC_MEASUREMENT_RATIO: _ClassVar[MetricMeasurement]

class MetricDurationUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_DURATION_UNIT_UNSPECIFIED: _ClassVar[MetricDurationUnit]
    METRIC_DURATION_UNIT_NANOSECONDS: _ClassVar[MetricDurationUnit]
    METRIC_DURATION_UNIT_MICROSECONDS: _ClassVar[MetricDurationUnit]
    METRIC_DURATION_UNIT_MILLISECONDS: _ClassVar[MetricDurationUnit]
    METRIC_DURATION_UNIT_SECONDS: _ClassVar[MetricDurationUnit]
    METRIC_DURATION_UNIT_MINUTES: _ClassVar[MetricDurationUnit]
    METRIC_DURATION_UNIT_HOURS: _ClassVar[MetricDurationUnit]

class MetricRateUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_RATE_UNIT_UNSPECIFIED: _ClassVar[MetricRateUnit]
    METRIC_RATE_UNIT_PER_SECOND: _ClassVar[MetricRateUnit]
    METRIC_RATE_UNIT_PER_MINUTE: _ClassVar[MetricRateUnit]
    METRIC_RATE_UNIT_PER_HOUR: _ClassVar[MetricRateUnit]

class MetricCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_CATEGORY_UNSPECIFIED: _ClassVar[MetricCategory]
    METRIC_CATEGORY_UTILIZATION: _ClassVar[MetricCategory]
    METRIC_CATEGORY_SATURATION: _ClassVar[MetricCategory]
    METRIC_CATEGORY_ERRORS: _ClassVar[MetricCategory]
    METRIC_CATEGORY_LATENCY: _ClassVar[MetricCategory]
    METRIC_CATEGORY_TRAFFIC: _ClassVar[MetricCategory]
    METRIC_CATEGORY_AVAILABILITY: _ClassVar[MetricCategory]

class ComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMPONENT_TYPE_UNSPECIFIED: _ClassVar[ComponentType]
    COMPONENT_TYPE_GENERIC: _ClassVar[ComponentType]
    COMPONENT_TYPE_GROUP: _ClassVar[ComponentType]
    COMPONENT_TYPE_BACKEND: _ClassVar[ComponentType]
    COMPONENT_TYPE_FRONTEND: _ClassVar[ComponentType]
    COMPONENT_TYPE_CLUSTER: _ClassVar[ComponentType]
    COMPONENT_TYPE_NODE: _ClassVar[ComponentType]
    COMPONENT_TYPE_AGENT: _ClassVar[ComponentType]
    COMPONENT_TYPE_CAPABILITY: _ClassVar[ComponentType]
    COMPONENT_TYPE_RECEIVER: _ClassVar[ComponentType]
    COMPONENT_TYPE_FILTER: _ClassVar[ComponentType]
    COMPONENT_TYPE_PROCESSOR: _ClassVar[ComponentType]
    COMPONENT_TYPE_POLLER: _ClassVar[ComponentType]
    COMPONENT_TYPE_SCHEDULER: _ClassVar[ComponentType]
    COMPONENT_TYPE_ORCHESTRATOR: _ClassVar[ComponentType]
    COMPONENT_TYPE_SENDER: _ClassVar[ComponentType]
    COMPONENT_TYPE_PROXY: _ClassVar[ComponentType]
    COMPONENT_TYPE_ROUTER: _ClassVar[ComponentType]
    COMPONENT_TYPE_WORKER: _ClassVar[ComponentType]
    COMPONENT_TYPE_CHANNEL: _ClassVar[ComponentType]
    COMPONENT_TYPE_BUFFER: _ClassVar[ComponentType]
    COMPONENT_TYPE_SINK: _ClassVar[ComponentType]
    COMPONENT_TYPE_CONNECTION: _ClassVar[ComponentType]
    COMPONENT_TYPE_RECONCILER: _ClassVar[ComponentType]
    COMPONENT_TYPE_EVENT_LOOP: _ClassVar[ComponentType]
    COMPONENT_TYPE_CONFIG_MANAGER: _ClassVar[ComponentType]
    COMPONENT_TYPE_SUPERVISOR: _ClassVar[ComponentType]
    COMPONENT_TYPE_CACHE: _ClassVar[ComponentType]
    COMPONENT_TYPE_QUEUE: _ClassVar[ComponentType]
    COMPONENT_TYPE_DATABASE: _ClassVar[ComponentType]
    COMPONENT_TYPE_OBJECT_STORAGE: _ClassVar[ComponentType]
    COMPONENT_TYPE_TIMESERIES_DATABASE: _ClassVar[ComponentType]
    COMPONENT_TYPE_KEY_VALUE_STORE: _ClassVar[ComponentType]
    COMPONENT_TYPE_DOCUMENT_DATABASE: _ClassVar[ComponentType]
    COMPONENT_TYPE_SEARCH_INDEX: _ClassVar[ComponentType]
    COMPONENT_TYPE_STREAM: _ClassVar[ComponentType]
    COMPONENT_TYPE_MEMORY: _ClassVar[ComponentType]
    COMPONENT_TYPE_DISK: _ClassVar[ComponentType]
    COMPONENT_TYPE_FILESYSTEM: _ClassVar[ComponentType]
    COMPONENT_TYPE_NETWORK: _ClassVar[ComponentType]
    COMPONENT_TYPE_CPU: _ClassVar[ComponentType]
    COMPONENT_TYPE_GPU: _ClassVar[ComponentType]
    COMPONENT_TYPE_CLOCK: _ClassVar[ComponentType]
    COMPONENT_TYPE_SERVER: _ClassVar[ComponentType]
    COMPONENT_TYPE_VM: _ClassVar[ComponentType]
    COMPONENT_TYPE_CONTAINER: _ClassVar[ComponentType]
    COMPONENT_TYPE_POD: _ClassVar[ComponentType]
    COMPONENT_TYPE_NAMESPACE: _ClassVar[ComponentType]
    COMPONENT_TYPE_JAIL: _ClassVar[ComponentType]
    COMPONENT_TYPE_LAMBDA: _ClassVar[ComponentType]
    COMPONENT_TYPE_LOAD_BALANCER: _ClassVar[ComponentType]
    COMPONENT_TYPE_FIREWALL: _ClassVar[ComponentType]
    COMPONENT_TYPE_VPN: _ClassVar[ComponentType]
    COMPONENT_TYPE_SWITCH: _ClassVar[ComponentType]
    COMPONENT_TYPE_PHYSICAL_ROUTER: _ClassVar[ComponentType]
    COMPONENT_TYPE_DNS: _ClassVar[ComponentType]
    COMPONENT_TYPE_CDN: _ClassVar[ComponentType]
    COMPONENT_TYPE_TUNNEL: _ClassVar[ComponentType]
    COMPONENT_TYPE_EXTERNAL_API: _ClassVar[ComponentType]
    COMPONENT_TYPE_CLOUD_SERVICE: _ClassVar[ComponentType]
    COMPONENT_TYPE_SAAS: _ClassVar[ComponentType]
    COMPONENT_TYPE_CONFIG: _ClassVar[ComponentType]
    COMPONENT_TYPE_SCHEMA: _ClassVar[ComponentType]
    COMPONENT_TYPE_CERTIFICATE: _ClassVar[ComponentType]
    COMPONENT_TYPE_CREDENTIAL: _ClassVar[ComponentType]

class Audience(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUDIENCE_UNSPECIFIED: _ClassVar[Audience]
    AUDIENCE_CUSTOMER: _ClassVar[Audience]
    AUDIENCE_INTERNAL: _ClassVar[Audience]

class LinkType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LINK_TYPE_UNSPECIFIED: _ClassVar[LinkType]
    LINK_TYPE_DASHBOARD: _ClassVar[LinkType]
    LINK_TYPE_LOGS: _ClassVar[LinkType]
    LINK_TYPE_TRACES: _ClassVar[LinkType]
    LINK_TYPE_DOCUMENTATION: _ClassVar[LinkType]
    LINK_TYPE_RUNBOOK: _ClassVar[LinkType]
    LINK_TYPE_SOURCE_CODE: _ClassVar[LinkType]
    LINK_TYPE_TICKET: _ClassVar[LinkType]
    LINK_TYPE_ALERTING: _ClassVar[LinkType]
    LINK_TYPE_EXTERNAL: _ClassVar[LinkType]

LIFECYCLE_PHASE_UNSPECIFIED: LifecyclePhase
LIFECYCLE_PHASE_INITIALIZING: LifecyclePhase
LIFECYCLE_PHASE_RUNNING: LifecyclePhase
LIFECYCLE_PHASE_TERMINATING: LifecyclePhase
LIFECYCLE_PHASE_TERMINATED: LifecyclePhase
HEALTH_STATUS_UNSPECIFIED: HealthStatus
HEALTH_STATUS_HEALTHY: HealthStatus
HEALTH_STATUS_WARNING: HealthStatus
HEALTH_STATUS_DEGRADED: HealthStatus
HEALTH_STATUS_CRITICAL: HealthStatus
HEALTH_STATUS_DOWN: HealthStatus
METRIC_TYPE_UNSPECIFIED: MetricType
METRIC_TYPE_GAUGE: MetricType
METRIC_TYPE_COUNTER: MetricType
METRIC_TYPE_HISTOGRAM: MetricType
METRIC_ENTITY_UNSPECIFIED: MetricEntity
METRIC_ENTITY_REQUESTS: MetricEntity
METRIC_ENTITY_QUERIES: MetricEntity
METRIC_ENTITY_FLOWS: MetricEntity
METRIC_ENTITY_CONNECTIONS: MetricEntity
METRIC_ENTITY_PACKETS: MetricEntity
METRIC_ENTITY_BYTES: MetricEntity
METRIC_ENTITY_READS: MetricEntity
METRIC_ENTITY_WRITES: MetricEntity
METRIC_ENTITY_TRANSACTIONS: MetricEntity
METRIC_ENTITY_RECORDS: MetricEntity
METRIC_ENTITY_MESSAGES: MetricEntity
METRIC_ENTITY_EVENTS: MetricEntity
METRIC_ENTITY_LOGS: MetricEntity
METRIC_ENTITY_TASKS: MetricEntity
METRIC_ENTITY_OPERATIONS: MetricEntity
METRIC_ENTITY_BATCHES: MetricEntity
METRIC_ENTITY_ITEMS: MetricEntity
METRIC_ENTITY_DATA: MetricEntity
METRIC_ENTITY_BLOCKS: MetricEntity
METRIC_ENTITY_REPLICAS: MetricEntity
METRIC_ENTITY_SNAPSHOTS: MetricEntity
METRIC_ENTITY_THREADS: MetricEntity
METRIC_ENTITY_PROCESSES: MetricEntity
METRIC_ENTITY_GOROUTINES: MetricEntity
METRIC_ENTITY_LOCKS: MetricEntity
METRIC_ENTITY_SESSIONS: MetricEntity
METRIC_ENTITY_USERS: MetricEntity
METRIC_ENTITY_CLIENTS: MetricEntity
METRIC_ENTITY_ERRORS: MetricEntity
METRIC_ENTITY_SPANS: MetricEntity
METRIC_ENTITY_ALERTS: MetricEntity
METRIC_MEASUREMENT_UNSPECIFIED: MetricMeasurement
METRIC_MEASUREMENT_COUNT: MetricMeasurement
METRIC_MEASUREMENT_DURATION: MetricMeasurement
METRIC_MEASUREMENT_SIZE: MetricMeasurement
METRIC_MEASUREMENT_RATIO: MetricMeasurement
METRIC_DURATION_UNIT_UNSPECIFIED: MetricDurationUnit
METRIC_DURATION_UNIT_NANOSECONDS: MetricDurationUnit
METRIC_DURATION_UNIT_MICROSECONDS: MetricDurationUnit
METRIC_DURATION_UNIT_MILLISECONDS: MetricDurationUnit
METRIC_DURATION_UNIT_SECONDS: MetricDurationUnit
METRIC_DURATION_UNIT_MINUTES: MetricDurationUnit
METRIC_DURATION_UNIT_HOURS: MetricDurationUnit
METRIC_RATE_UNIT_UNSPECIFIED: MetricRateUnit
METRIC_RATE_UNIT_PER_SECOND: MetricRateUnit
METRIC_RATE_UNIT_PER_MINUTE: MetricRateUnit
METRIC_RATE_UNIT_PER_HOUR: MetricRateUnit
METRIC_CATEGORY_UNSPECIFIED: MetricCategory
METRIC_CATEGORY_UTILIZATION: MetricCategory
METRIC_CATEGORY_SATURATION: MetricCategory
METRIC_CATEGORY_ERRORS: MetricCategory
METRIC_CATEGORY_LATENCY: MetricCategory
METRIC_CATEGORY_TRAFFIC: MetricCategory
METRIC_CATEGORY_AVAILABILITY: MetricCategory
COMPONENT_TYPE_UNSPECIFIED: ComponentType
COMPONENT_TYPE_GENERIC: ComponentType
COMPONENT_TYPE_GROUP: ComponentType
COMPONENT_TYPE_BACKEND: ComponentType
COMPONENT_TYPE_FRONTEND: ComponentType
COMPONENT_TYPE_CLUSTER: ComponentType
COMPONENT_TYPE_NODE: ComponentType
COMPONENT_TYPE_AGENT: ComponentType
COMPONENT_TYPE_CAPABILITY: ComponentType
COMPONENT_TYPE_RECEIVER: ComponentType
COMPONENT_TYPE_FILTER: ComponentType
COMPONENT_TYPE_PROCESSOR: ComponentType
COMPONENT_TYPE_POLLER: ComponentType
COMPONENT_TYPE_SCHEDULER: ComponentType
COMPONENT_TYPE_ORCHESTRATOR: ComponentType
COMPONENT_TYPE_SENDER: ComponentType
COMPONENT_TYPE_PROXY: ComponentType
COMPONENT_TYPE_ROUTER: ComponentType
COMPONENT_TYPE_WORKER: ComponentType
COMPONENT_TYPE_CHANNEL: ComponentType
COMPONENT_TYPE_BUFFER: ComponentType
COMPONENT_TYPE_SINK: ComponentType
COMPONENT_TYPE_CONNECTION: ComponentType
COMPONENT_TYPE_RECONCILER: ComponentType
COMPONENT_TYPE_EVENT_LOOP: ComponentType
COMPONENT_TYPE_CONFIG_MANAGER: ComponentType
COMPONENT_TYPE_SUPERVISOR: ComponentType
COMPONENT_TYPE_CACHE: ComponentType
COMPONENT_TYPE_QUEUE: ComponentType
COMPONENT_TYPE_DATABASE: ComponentType
COMPONENT_TYPE_OBJECT_STORAGE: ComponentType
COMPONENT_TYPE_TIMESERIES_DATABASE: ComponentType
COMPONENT_TYPE_KEY_VALUE_STORE: ComponentType
COMPONENT_TYPE_DOCUMENT_DATABASE: ComponentType
COMPONENT_TYPE_SEARCH_INDEX: ComponentType
COMPONENT_TYPE_STREAM: ComponentType
COMPONENT_TYPE_MEMORY: ComponentType
COMPONENT_TYPE_DISK: ComponentType
COMPONENT_TYPE_FILESYSTEM: ComponentType
COMPONENT_TYPE_NETWORK: ComponentType
COMPONENT_TYPE_CPU: ComponentType
COMPONENT_TYPE_GPU: ComponentType
COMPONENT_TYPE_CLOCK: ComponentType
COMPONENT_TYPE_SERVER: ComponentType
COMPONENT_TYPE_VM: ComponentType
COMPONENT_TYPE_CONTAINER: ComponentType
COMPONENT_TYPE_POD: ComponentType
COMPONENT_TYPE_NAMESPACE: ComponentType
COMPONENT_TYPE_JAIL: ComponentType
COMPONENT_TYPE_LAMBDA: ComponentType
COMPONENT_TYPE_LOAD_BALANCER: ComponentType
COMPONENT_TYPE_FIREWALL: ComponentType
COMPONENT_TYPE_VPN: ComponentType
COMPONENT_TYPE_SWITCH: ComponentType
COMPONENT_TYPE_PHYSICAL_ROUTER: ComponentType
COMPONENT_TYPE_DNS: ComponentType
COMPONENT_TYPE_CDN: ComponentType
COMPONENT_TYPE_TUNNEL: ComponentType
COMPONENT_TYPE_EXTERNAL_API: ComponentType
COMPONENT_TYPE_CLOUD_SERVICE: ComponentType
COMPONENT_TYPE_SAAS: ComponentType
COMPONENT_TYPE_CONFIG: ComponentType
COMPONENT_TYPE_SCHEMA: ComponentType
COMPONENT_TYPE_CERTIFICATE: ComponentType
COMPONENT_TYPE_CREDENTIAL: ComponentType
AUDIENCE_UNSPECIFIED: Audience
AUDIENCE_CUSTOMER: Audience
AUDIENCE_INTERNAL: Audience
LINK_TYPE_UNSPECIFIED: LinkType
LINK_TYPE_DASHBOARD: LinkType
LINK_TYPE_LOGS: LinkType
LINK_TYPE_TRACES: LinkType
LINK_TYPE_DOCUMENTATION: LinkType
LINK_TYPE_RUNBOOK: LinkType
LINK_TYPE_SOURCE_CODE: LinkType
LINK_TYPE_TICKET: LinkType
LINK_TYPE_ALERTING: LinkType
LINK_TYPE_EXTERNAL: LinkType

class Probe(_message.Message):
    __slots__ = ("ok", "message")
    OK_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    message: str
    def __init__(
        self, ok: _Optional[bool] = ..., message: _Optional[str] = ...
    ) -> None: ...

class Probes(_message.Message):
    __slots__ = ("startup", "liveness", "readiness")
    STARTUP_FIELD_NUMBER: _ClassVar[int]
    LIVENESS_FIELD_NUMBER: _ClassVar[int]
    READINESS_FIELD_NUMBER: _ClassVar[int]
    startup: Probe
    liveness: Probe
    readiness: Probe
    def __init__(
        self,
        startup: _Optional[_Union[Probe, _Mapping]] = ...,
        liveness: _Optional[_Union[Probe, _Mapping]] = ...,
        readiness: _Optional[_Union[Probe, _Mapping]] = ...,
    ) -> None: ...

class Health(_message.Message):
    __slots__ = ("status", "score", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: HealthStatus
    score: float
    message: str
    def __init__(
        self,
        status: _Optional[_Union[HealthStatus, str]] = ...,
        score: _Optional[float] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class MetricDefinition(_message.Message):
    __slots__ = (
        "name",
        "description",
        "entity",
        "measurement",
        "duration_unit",
        "rate_unit",
        "type",
        "category",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    DURATION_UNIT_FIELD_NUMBER: _ClassVar[int]
    RATE_UNIT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    entity: MetricEntity
    measurement: MetricMeasurement
    duration_unit: MetricDurationUnit
    rate_unit: MetricRateUnit
    type: MetricType
    category: MetricCategory
    def __init__(
        self,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        entity: _Optional[_Union[MetricEntity, str]] = ...,
        measurement: _Optional[_Union[MetricMeasurement, str]] = ...,
        duration_unit: _Optional[_Union[MetricDurationUnit, str]] = ...,
        rate_unit: _Optional[_Union[MetricRateUnit, str]] = ...,
        type: _Optional[_Union[MetricType, str]] = ...,
        category: _Optional[_Union[MetricCategory, str]] = ...,
    ) -> None: ...

class Percentile(_message.Message):
    __slots__ = ("quantile", "value")
    QUANTILE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    quantile: float
    value: float
    def __init__(
        self, quantile: _Optional[float] = ..., value: _Optional[float] = ...
    ) -> None: ...

class HistogramValue(_message.Message):
    __slots__ = ("sample_count", "sample_sum", "percentiles")
    SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SUM_FIELD_NUMBER: _ClassVar[int]
    PERCENTILES_FIELD_NUMBER: _ClassVar[int]
    sample_count: int
    sample_sum: float
    percentiles: _containers.RepeatedCompositeFieldContainer[Percentile]
    def __init__(
        self,
        sample_count: _Optional[int] = ...,
        sample_sum: _Optional[float] = ...,
        percentiles: _Optional[_Iterable[_Union[Percentile, _Mapping]]] = ...,
    ) -> None: ...

class MetricValue(_message.Message):
    __slots__ = ("scalar", "histogram")
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    HISTOGRAM_FIELD_NUMBER: _ClassVar[int]
    scalar: float
    histogram: HistogramValue
    def __init__(
        self,
        scalar: _Optional[float] = ...,
        histogram: _Optional[_Union[HistogramValue, _Mapping]] = ...,
    ) -> None: ...

class MetricSample(_message.Message):
    __slots__ = ("labels", "value")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    LABELS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.ScalarMap[str, str]
    value: MetricValue
    def __init__(
        self,
        labels: _Optional[_Mapping[str, str]] = ...,
        value: _Optional[_Union[MetricValue, _Mapping]] = ...,
    ) -> None: ...

class Metric(_message.Message):
    __slots__ = ("definition", "samples")
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    SAMPLES_FIELD_NUMBER: _ClassVar[int]
    definition: MetricDefinition
    samples: _containers.RepeatedCompositeFieldContainer[MetricSample]
    def __init__(
        self,
        definition: _Optional[_Union[MetricDefinition, _Mapping]] = ...,
        samples: _Optional[_Iterable[_Union[MetricSample, _Mapping]]] = ...,
    ) -> None: ...

class Link(_message.Message):
    __slots__ = ("type", "title", "url")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    type: LinkType
    title: str
    url: str
    def __init__(
        self,
        type: _Optional[_Union[LinkType, str]] = ...,
        title: _Optional[str] = ...,
        url: _Optional[str] = ...,
    ) -> None: ...

class Fact(_message.Message):
    __slots__ = ("key", "value", "description", "cohort")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COHORT_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    description: str
    cohort: bool
    def __init__(
        self,
        key: _Optional[str] = ...,
        value: _Optional[str] = ...,
        description: _Optional[str] = ...,
        cohort: _Optional[bool] = ...,
    ) -> None: ...

class ComponentState(_message.Message):
    __slots__ = (
        "name",
        "type",
        "description",
        "lifecycle_phase",
        "probes",
        "health",
        "children",
        "metrics",
        "labels",
        "links",
        "facts",
        "timestamp",
        "audience",
        "version_independent",
    )
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LIFECYCLE_PHASE_FIELD_NUMBER: _ClassVar[int]
    PROBES_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    VERSION_INDEPENDENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: ComponentType
    description: str
    lifecycle_phase: LifecyclePhase
    probes: Probes
    health: Health
    children: _containers.RepeatedCompositeFieldContainer[ComponentState]
    metrics: _containers.RepeatedCompositeFieldContainer[Metric]
    labels: _containers.ScalarMap[str, str]
    links: _containers.RepeatedCompositeFieldContainer[Link]
    facts: _containers.RepeatedCompositeFieldContainer[Fact]
    timestamp: _timestamp_pb2.Timestamp
    audience: Audience
    version_independent: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[_Union[ComponentType, str]] = ...,
        description: _Optional[str] = ...,
        lifecycle_phase: _Optional[_Union[LifecyclePhase, str]] = ...,
        probes: _Optional[_Union[Probes, _Mapping]] = ...,
        health: _Optional[_Union[Health, _Mapping]] = ...,
        children: _Optional[_Iterable[_Union[ComponentState, _Mapping]]] = ...,
        metrics: _Optional[_Iterable[_Union[Metric, _Mapping]]] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...,
        facts: _Optional[_Iterable[_Union[Fact, _Mapping]]] = ...,
        timestamp: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        audience: _Optional[_Union[Audience, str]] = ...,
        version_independent: _Optional[bool] = ...,
    ) -> None: ...
