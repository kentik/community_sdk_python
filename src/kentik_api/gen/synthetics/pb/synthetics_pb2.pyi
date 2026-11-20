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

DESCRIPTOR: _descriptor.FileDescriptor

class ImplementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IMPLEMENT_TYPE_UNSPECIFIED: _ClassVar[ImplementType]
    IMPLEMENT_TYPE_RUST: _ClassVar[ImplementType]
    IMPLEMENT_TYPE_NODE: _ClassVar[ImplementType]
    IMPLEMENT_TYPE_NETWORK: _ClassVar[ImplementType]

class IPFamily(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IP_FAMILY_UNSPECIFIED: _ClassVar[IPFamily]
    IP_FAMILY_V4: _ClassVar[IPFamily]
    IP_FAMILY_V6: _ClassVar[IPFamily]
    IP_FAMILY_DUAL: _ClassVar[IPFamily]

class TestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEST_STATUS_UNSPECIFIED: _ClassVar[TestStatus]
    TEST_STATUS_ACTIVE: _ClassVar[TestStatus]
    TEST_STATUS_PAUSED: _ClassVar[TestStatus]
    TEST_STATUS_DELETED: _ClassVar[TestStatus]
    TEST_STATUS_PREVIEW: _ClassVar[TestStatus]

class AgentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGENT_STATUS_UNSPECIFIED: _ClassVar[AgentStatus]
    AGENT_STATUS_OK: _ClassVar[AgentStatus]
    AGENT_STATUS_WAIT: _ClassVar[AgentStatus]
    AGENT_STATUS_DELETED: _ClassVar[AgentStatus]

class DNSRecord(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DNS_RECORD_UNSPECIFIED: _ClassVar[DNSRecord]
    DNS_RECORD_A: _ClassVar[DNSRecord]
    DNS_RECORD_AAAA: _ClassVar[DNSRecord]
    DNS_RECORD_CNAME: _ClassVar[DNSRecord]
    DNS_RECORD_DNAME: _ClassVar[DNSRecord]
    DNS_RECORD_NS: _ClassVar[DNSRecord]
    DNS_RECORD_MX: _ClassVar[DNSRecord]
    DNS_RECORD_PTR: _ClassVar[DNSRecord]
    DNS_RECORD_SOA: _ClassVar[DNSRecord]

class AlertingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALERTING_TYPE_UNSPECIFIED: _ClassVar[AlertingType]
    ALERTING_TYPE_AGENT: _ClassVar[AlertingType]
    ALERTING_TYPE_GROUPED: _ClassVar[AlertingType]
    ALERTING_TYPE_SUBTEST: _ClassVar[AlertingType]

class SrcGroupBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SRC_GROUP_BY_UNSPECIFIED: _ClassVar[SrcGroupBy]
    SRC_GROUP_BY_ALL_AGENTS: _ClassVar[SrcGroupBy]
    SRC_GROUP_BY_LABEL: _ClassVar[SrcGroupBy]
    SRC_GROUP_BY_SITE: _ClassVar[SrcGroupBy]

IMPLEMENT_TYPE_UNSPECIFIED: ImplementType
IMPLEMENT_TYPE_RUST: ImplementType
IMPLEMENT_TYPE_NODE: ImplementType
IMPLEMENT_TYPE_NETWORK: ImplementType
IP_FAMILY_UNSPECIFIED: IPFamily
IP_FAMILY_V4: IPFamily
IP_FAMILY_V6: IPFamily
IP_FAMILY_DUAL: IPFamily
TEST_STATUS_UNSPECIFIED: TestStatus
TEST_STATUS_ACTIVE: TestStatus
TEST_STATUS_PAUSED: TestStatus
TEST_STATUS_DELETED: TestStatus
TEST_STATUS_PREVIEW: TestStatus
AGENT_STATUS_UNSPECIFIED: AgentStatus
AGENT_STATUS_OK: AgentStatus
AGENT_STATUS_WAIT: AgentStatus
AGENT_STATUS_DELETED: AgentStatus
DNS_RECORD_UNSPECIFIED: DNSRecord
DNS_RECORD_A: DNSRecord
DNS_RECORD_AAAA: DNSRecord
DNS_RECORD_CNAME: DNSRecord
DNS_RECORD_DNAME: DNSRecord
DNS_RECORD_NS: DNSRecord
DNS_RECORD_MX: DNSRecord
DNS_RECORD_PTR: DNSRecord
DNS_RECORD_SOA: DNSRecord
ALERTING_TYPE_UNSPECIFIED: AlertingType
ALERTING_TYPE_AGENT: AlertingType
ALERTING_TYPE_GROUPED: AlertingType
ALERTING_TYPE_SUBTEST: AlertingType
SRC_GROUP_BY_UNSPECIFIED: SrcGroupBy
SRC_GROUP_BY_ALL_AGENTS: SrcGroupBy
SRC_GROUP_BY_LABEL: SrcGroupBy
SRC_GROUP_BY_SITE: SrcGroupBy

class DisabledMetrics(_message.Message):
    __slots__ = (
        "ping_latency",
        "ping_jitter",
        "ping_packet_loss",
        "http_latency",
        "http_headers",
        "http_codes",
        "http_cert_expiry",
        "transaction_latency",
        "dns_latency",
        "dns_codes",
        "dns_ips",
        "throughput_bandwidth",
    )
    PING_LATENCY_FIELD_NUMBER: _ClassVar[int]
    PING_JITTER_FIELD_NUMBER: _ClassVar[int]
    PING_PACKET_LOSS_FIELD_NUMBER: _ClassVar[int]
    HTTP_LATENCY_FIELD_NUMBER: _ClassVar[int]
    HTTP_HEADERS_FIELD_NUMBER: _ClassVar[int]
    HTTP_CODES_FIELD_NUMBER: _ClassVar[int]
    HTTP_CERT_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_LATENCY_FIELD_NUMBER: _ClassVar[int]
    DNS_LATENCY_FIELD_NUMBER: _ClassVar[int]
    DNS_CODES_FIELD_NUMBER: _ClassVar[int]
    DNS_IPS_FIELD_NUMBER: _ClassVar[int]
    THROUGHPUT_BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    ping_latency: bool
    ping_jitter: bool
    ping_packet_loss: bool
    http_latency: bool
    http_headers: bool
    http_codes: bool
    http_cert_expiry: bool
    transaction_latency: bool
    dns_latency: bool
    dns_codes: bool
    dns_ips: bool
    throughput_bandwidth: bool
    def __init__(
        self,
        ping_latency: _Optional[bool] = ...,
        ping_jitter: _Optional[bool] = ...,
        ping_packet_loss: _Optional[bool] = ...,
        http_latency: _Optional[bool] = ...,
        http_headers: _Optional[bool] = ...,
        http_codes: _Optional[bool] = ...,
        http_cert_expiry: _Optional[bool] = ...,
        transaction_latency: _Optional[bool] = ...,
        dns_latency: _Optional[bool] = ...,
        dns_codes: _Optional[bool] = ...,
        dns_ips: _Optional[bool] = ...,
        throughput_bandwidth: _Optional[bool] = ...,
    ) -> None: ...

class Agent(_message.Message):
    __slots__ = (
        "id",
        "site_name",
        "status",
        "alias",
        "type",
        "os",
        "ip",
        "lat",
        "long",
        "last_authed",
        "family",
        "asn",
        "site_id",
        "version",
        "city",
        "region",
        "country",
        "test_ids",
        "local_ip",
        "cloud_region",
        "cloud_provider",
        "agent_impl",
        "labels",
        "metadata",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    LAST_AUTHED_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    TEST_IDS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_IP_FIELD_NUMBER: _ClassVar[int]
    CLOUD_REGION_FIELD_NUMBER: _ClassVar[int]
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    AGENT_IMPL_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    site_name: str
    status: AgentStatus
    alias: str
    type: str
    os: str
    ip: str
    lat: float
    long: float
    last_authed: _timestamp_pb2.Timestamp
    family: IPFamily
    asn: int
    site_id: str
    version: str
    city: str
    region: str
    country: str
    test_ids: _containers.RepeatedScalarFieldContainer[str]
    local_ip: str
    cloud_region: str
    cloud_provider: str
    agent_impl: ImplementType
    labels: _containers.RepeatedScalarFieldContainer[str]
    metadata: AgentMetadata
    def __init__(
        self,
        id: _Optional[str] = ...,
        site_name: _Optional[str] = ...,
        status: _Optional[_Union[AgentStatus, str]] = ...,
        alias: _Optional[str] = ...,
        type: _Optional[str] = ...,
        os: _Optional[str] = ...,
        ip: _Optional[str] = ...,
        lat: _Optional[float] = ...,
        long: _Optional[float] = ...,
        last_authed: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        family: _Optional[_Union[IPFamily, str]] = ...,
        asn: _Optional[int] = ...,
        site_id: _Optional[str] = ...,
        version: _Optional[str] = ...,
        city: _Optional[str] = ...,
        region: _Optional[str] = ...,
        country: _Optional[str] = ...,
        test_ids: _Optional[_Iterable[str]] = ...,
        local_ip: _Optional[str] = ...,
        cloud_region: _Optional[str] = ...,
        cloud_provider: _Optional[str] = ...,
        agent_impl: _Optional[_Union[ImplementType, str]] = ...,
        labels: _Optional[_Iterable[str]] = ...,
        metadata: _Optional[_Union[AgentMetadata, _Mapping]] = ...,
    ) -> None: ...

class AgentMetadata(_message.Message):
    __slots__ = (
        "private_ipv4_addresses",
        "public_ipv4_addresses",
        "private_ipv6_addresses",
        "public_ipv6_addresses",
        "static_ipv4",
        "static_ipv6",
    )
    class IpValue(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: str
        def __init__(self, value: _Optional[str] = ...) -> None: ...

    PRIVATE_IPV4_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IPV4_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_IPV6_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_IPV6_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    STATIC_IPV4_FIELD_NUMBER: _ClassVar[int]
    STATIC_IPV6_FIELD_NUMBER: _ClassVar[int]
    private_ipv4_addresses: _containers.RepeatedCompositeFieldContainer[
        AgentMetadata.IpValue
    ]
    public_ipv4_addresses: _containers.RepeatedCompositeFieldContainer[
        AgentMetadata.IpValue
    ]
    private_ipv6_addresses: _containers.RepeatedCompositeFieldContainer[
        AgentMetadata.IpValue
    ]
    public_ipv6_addresses: _containers.RepeatedCompositeFieldContainer[
        AgentMetadata.IpValue
    ]
    static_ipv4: bool
    static_ipv6: bool
    def __init__(
        self,
        private_ipv4_addresses: _Optional[
            _Iterable[_Union[AgentMetadata.IpValue, _Mapping]]
        ] = ...,
        public_ipv4_addresses: _Optional[
            _Iterable[_Union[AgentMetadata.IpValue, _Mapping]]
        ] = ...,
        private_ipv6_addresses: _Optional[
            _Iterable[_Union[AgentMetadata.IpValue, _Mapping]]
        ] = ...,
        public_ipv6_addresses: _Optional[
            _Iterable[_Union[AgentMetadata.IpValue, _Mapping]]
        ] = ...,
        static_ipv4: _Optional[bool] = ...,
        static_ipv6: _Optional[bool] = ...,
    ) -> None: ...

class Test(_message.Message):
    __slots__ = (
        "id",
        "name",
        "type",
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
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    status: TestStatus
    settings: TestSettings
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    created_by: _user_info_pb2.UserInfo
    last_updated_by: _user_info_pb2.UserInfo
    labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        type: _Optional[str] = ...,
        status: _Optional[_Union[TestStatus, str]] = ...,
        settings: _Optional[_Union[TestSettings, _Mapping]] = ...,
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

class TestSettings(_message.Message):
    __slots__ = (
        "hostname",
        "ip",
        "agent",
        "flow",
        "dns",
        "url",
        "network_grid",
        "page_load",
        "dns_grid",
        "network_mesh",
        "agent_ids",
        "tasks",
        "health_settings",
        "ping",
        "trace",
        "period",
        "family",
        "notification_channels",
        "notes",
        "throughput",
        "schedule",
        "alerting",
    )
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    FLOW_FIELD_NUMBER: _ClassVar[int]
    DNS_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    NETWORK_GRID_FIELD_NUMBER: _ClassVar[int]
    PAGE_LOAD_FIELD_NUMBER: _ClassVar[int]
    DNS_GRID_FIELD_NUMBER: _ClassVar[int]
    NETWORK_MESH_FIELD_NUMBER: _ClassVar[int]
    AGENT_IDS_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    TRACE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    THROUGHPUT_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    ALERTING_FIELD_NUMBER: _ClassVar[int]
    hostname: HostnameTest
    ip: IpTest
    agent: AgentTest
    flow: FlowTest
    dns: DnsTest
    url: UrlTest
    network_grid: IpTest
    page_load: PageLoadTest
    dns_grid: DnsTest
    network_mesh: NetworkMeshTest
    agent_ids: _containers.RepeatedScalarFieldContainer[str]
    tasks: _containers.RepeatedScalarFieldContainer[str]
    health_settings: HealthSettings
    ping: TestPingSettings
    trace: TestTraceSettings
    period: int
    family: IPFamily
    notification_channels: _containers.RepeatedScalarFieldContainer[str]
    notes: str
    throughput: TestThroughputSettings
    schedule: ScheduleSettings
    alerting: AlertingSettings
    def __init__(
        self,
        hostname: _Optional[_Union[HostnameTest, _Mapping]] = ...,
        ip: _Optional[_Union[IpTest, _Mapping]] = ...,
        agent: _Optional[_Union[AgentTest, _Mapping]] = ...,
        flow: _Optional[_Union[FlowTest, _Mapping]] = ...,
        dns: _Optional[_Union[DnsTest, _Mapping]] = ...,
        url: _Optional[_Union[UrlTest, _Mapping]] = ...,
        network_grid: _Optional[_Union[IpTest, _Mapping]] = ...,
        page_load: _Optional[_Union[PageLoadTest, _Mapping]] = ...,
        dns_grid: _Optional[_Union[DnsTest, _Mapping]] = ...,
        network_mesh: _Optional[_Union[NetworkMeshTest, _Mapping]] = ...,
        agent_ids: _Optional[_Iterable[str]] = ...,
        tasks: _Optional[_Iterable[str]] = ...,
        health_settings: _Optional[_Union[HealthSettings, _Mapping]] = ...,
        ping: _Optional[_Union[TestPingSettings, _Mapping]] = ...,
        trace: _Optional[_Union[TestTraceSettings, _Mapping]] = ...,
        period: _Optional[int] = ...,
        family: _Optional[_Union[IPFamily, str]] = ...,
        notification_channels: _Optional[_Iterable[str]] = ...,
        notes: _Optional[str] = ...,
        throughput: _Optional[_Union[TestThroughputSettings, _Mapping]] = ...,
        schedule: _Optional[_Union[ScheduleSettings, _Mapping]] = ...,
        alerting: _Optional[_Union[AlertingSettings, _Mapping]] = ...,
    ) -> None: ...

class TestPingSettings(_message.Message):
    __slots__ = ("count", "protocol", "port", "timeout", "delay", "dscp")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    DSCP_FIELD_NUMBER: _ClassVar[int]
    count: int
    protocol: str
    port: int
    timeout: int
    delay: float
    dscp: int
    def __init__(
        self,
        count: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
        port: _Optional[int] = ...,
        timeout: _Optional[int] = ...,
        delay: _Optional[float] = ...,
        dscp: _Optional[int] = ...,
    ) -> None: ...

class TestTraceSettings(_message.Message):
    __slots__ = (
        "count",
        "protocol",
        "port",
        "timeout",
        "limit",
        "delay",
        "dscp",
        "mtu",
    )
    COUNT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    DSCP_FIELD_NUMBER: _ClassVar[int]
    MTU_FIELD_NUMBER: _ClassVar[int]
    count: int
    protocol: str
    port: int
    timeout: int
    limit: int
    delay: float
    dscp: int
    mtu: bool
    def __init__(
        self,
        count: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
        port: _Optional[int] = ...,
        timeout: _Optional[int] = ...,
        limit: _Optional[int] = ...,
        delay: _Optional[float] = ...,
        dscp: _Optional[int] = ...,
        mtu: _Optional[bool] = ...,
    ) -> None: ...

class TestThroughputSettings(_message.Message):
    __slots__ = ("port", "omit", "duration", "bandwidth", "protocol")
    PORT_FIELD_NUMBER: _ClassVar[int]
    OMIT_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    BANDWIDTH_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    port: int
    omit: int
    duration: int
    bandwidth: int
    protocol: str
    def __init__(
        self,
        port: _Optional[int] = ...,
        omit: _Optional[int] = ...,
        duration: _Optional[int] = ...,
        bandwidth: _Optional[int] = ...,
        protocol: _Optional[str] = ...,
    ) -> None: ...

class ScheduleSettings(_message.Message):
    __slots__ = ("enabled", "start", "end")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    start: int
    end: int
    def __init__(
        self,
        enabled: _Optional[bool] = ...,
        start: _Optional[int] = ...,
        end: _Optional[int] = ...,
    ) -> None: ...

class GroupedAlertSetting(_message.Message):
    __slots__ = ("metric", "src_group_by", "percent_of_src_group", "filter_ids")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    SRC_GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    PERCENT_OF_SRC_GROUP_FIELD_NUMBER: _ClassVar[int]
    FILTER_IDS_FIELD_NUMBER: _ClassVar[int]
    metric: str
    src_group_by: SrcGroupBy
    percent_of_src_group: int
    filter_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        metric: _Optional[str] = ...,
        src_group_by: _Optional[_Union[SrcGroupBy, str]] = ...,
        percent_of_src_group: _Optional[int] = ...,
        filter_ids: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class GroupedAlertSettings(_message.Message):
    __slots__ = ("default", "overrides")
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    default: GroupedAlertSetting
    overrides: _containers.RepeatedCompositeFieldContainer[GroupedAlertSetting]
    def __init__(
        self,
        default: _Optional[_Union[GroupedAlertSetting, _Mapping]] = ...,
        overrides: _Optional[_Iterable[_Union[GroupedAlertSetting, _Mapping]]] = ...,
    ) -> None: ...

class AlertingSettings(_message.Message):
    __slots__ = (
        "disable_warning_notifications",
        "alerting_type",
        "grouped_alert_settings",
    )
    DISABLE_WARNING_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    ALERTING_TYPE_FIELD_NUMBER: _ClassVar[int]
    GROUPED_ALERT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    disable_warning_notifications: bool
    alerting_type: AlertingType
    grouped_alert_settings: GroupedAlertSettings
    def __init__(
        self,
        disable_warning_notifications: _Optional[bool] = ...,
        alerting_type: _Optional[_Union[AlertingType, str]] = ...,
        grouped_alert_settings: _Optional[_Union[GroupedAlertSettings, _Mapping]] = ...,
    ) -> None: ...

class ActivationSettings(_message.Message):
    __slots__ = ("grace_period", "time_unit", "time_window", "times")
    GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    TIMES_FIELD_NUMBER: _ClassVar[int]
    grace_period: str
    time_unit: str
    time_window: str
    times: str
    def __init__(
        self,
        grace_period: _Optional[str] = ...,
        time_unit: _Optional[str] = ...,
        time_window: _Optional[str] = ...,
        times: _Optional[str] = ...,
    ) -> None: ...

class HealthSettings(_message.Message):
    __slots__ = (
        "latency_critical",
        "latency_warning",
        "packet_loss_critical",
        "packet_loss_warning",
        "jitter_critical",
        "jitter_warning",
        "http_latency_critical",
        "http_latency_warning",
        "http_valid_codes",
        "dns_valid_codes",
        "latency_critical_stddev",
        "latency_warning_stddev",
        "jitter_critical_stddev",
        "jitter_warning_stddev",
        "http_latency_critical_stddev",
        "http_latency_warning_stddev",
        "unhealthy_subtest_threshold",
        "activation",
        "cert_expiry_warning",
        "cert_expiry_critical",
        "dns_valid_ips",
        "dns_latency_critical",
        "dns_latency_warning",
        "dns_latency_critical_stddev",
        "dns_latency_warning_stddev",
        "per_agent_alerting",
        "disabled_metrics",
        "health_disabled",
        "throughput_critical",
        "throughput_warning",
        "throughput_critical_stddev",
        "throughput_warning_stddev",
        "disable_alerts",
    )
    LATENCY_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    LATENCY_WARNING_FIELD_NUMBER: _ClassVar[int]
    PACKET_LOSS_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    PACKET_LOSS_WARNING_FIELD_NUMBER: _ClassVar[int]
    JITTER_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    JITTER_WARNING_FIELD_NUMBER: _ClassVar[int]
    HTTP_LATENCY_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    HTTP_LATENCY_WARNING_FIELD_NUMBER: _ClassVar[int]
    HTTP_VALID_CODES_FIELD_NUMBER: _ClassVar[int]
    DNS_VALID_CODES_FIELD_NUMBER: _ClassVar[int]
    LATENCY_CRITICAL_STDDEV_FIELD_NUMBER: _ClassVar[int]
    LATENCY_WARNING_STDDEV_FIELD_NUMBER: _ClassVar[int]
    JITTER_CRITICAL_STDDEV_FIELD_NUMBER: _ClassVar[int]
    JITTER_WARNING_STDDEV_FIELD_NUMBER: _ClassVar[int]
    HTTP_LATENCY_CRITICAL_STDDEV_FIELD_NUMBER: _ClassVar[int]
    HTTP_LATENCY_WARNING_STDDEV_FIELD_NUMBER: _ClassVar[int]
    UNHEALTHY_SUBTEST_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_FIELD_NUMBER: _ClassVar[int]
    CERT_EXPIRY_WARNING_FIELD_NUMBER: _ClassVar[int]
    CERT_EXPIRY_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    DNS_VALID_IPS_FIELD_NUMBER: _ClassVar[int]
    DNS_LATENCY_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    DNS_LATENCY_WARNING_FIELD_NUMBER: _ClassVar[int]
    DNS_LATENCY_CRITICAL_STDDEV_FIELD_NUMBER: _ClassVar[int]
    DNS_LATENCY_WARNING_STDDEV_FIELD_NUMBER: _ClassVar[int]
    PER_AGENT_ALERTING_FIELD_NUMBER: _ClassVar[int]
    DISABLED_METRICS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_DISABLED_FIELD_NUMBER: _ClassVar[int]
    THROUGHPUT_CRITICAL_FIELD_NUMBER: _ClassVar[int]
    THROUGHPUT_WARNING_FIELD_NUMBER: _ClassVar[int]
    THROUGHPUT_CRITICAL_STDDEV_FIELD_NUMBER: _ClassVar[int]
    THROUGHPUT_WARNING_STDDEV_FIELD_NUMBER: _ClassVar[int]
    DISABLE_ALERTS_FIELD_NUMBER: _ClassVar[int]
    latency_critical: float
    latency_warning: float
    packet_loss_critical: float
    packet_loss_warning: float
    jitter_critical: float
    jitter_warning: float
    http_latency_critical: float
    http_latency_warning: float
    http_valid_codes: _containers.RepeatedScalarFieldContainer[int]
    dns_valid_codes: _containers.RepeatedScalarFieldContainer[int]
    latency_critical_stddev: float
    latency_warning_stddev: float
    jitter_critical_stddev: float
    jitter_warning_stddev: float
    http_latency_critical_stddev: float
    http_latency_warning_stddev: float
    unhealthy_subtest_threshold: int
    activation: ActivationSettings
    cert_expiry_warning: int
    cert_expiry_critical: int
    dns_valid_ips: str
    dns_latency_critical: float
    dns_latency_warning: float
    dns_latency_critical_stddev: float
    dns_latency_warning_stddev: float
    per_agent_alerting: bool
    disabled_metrics: DisabledMetrics
    health_disabled: bool
    throughput_critical: float
    throughput_warning: float
    throughput_critical_stddev: float
    throughput_warning_stddev: float
    disable_alerts: bool
    def __init__(
        self,
        latency_critical: _Optional[float] = ...,
        latency_warning: _Optional[float] = ...,
        packet_loss_critical: _Optional[float] = ...,
        packet_loss_warning: _Optional[float] = ...,
        jitter_critical: _Optional[float] = ...,
        jitter_warning: _Optional[float] = ...,
        http_latency_critical: _Optional[float] = ...,
        http_latency_warning: _Optional[float] = ...,
        http_valid_codes: _Optional[_Iterable[int]] = ...,
        dns_valid_codes: _Optional[_Iterable[int]] = ...,
        latency_critical_stddev: _Optional[float] = ...,
        latency_warning_stddev: _Optional[float] = ...,
        jitter_critical_stddev: _Optional[float] = ...,
        jitter_warning_stddev: _Optional[float] = ...,
        http_latency_critical_stddev: _Optional[float] = ...,
        http_latency_warning_stddev: _Optional[float] = ...,
        unhealthy_subtest_threshold: _Optional[int] = ...,
        activation: _Optional[_Union[ActivationSettings, _Mapping]] = ...,
        cert_expiry_warning: _Optional[int] = ...,
        cert_expiry_critical: _Optional[int] = ...,
        dns_valid_ips: _Optional[str] = ...,
        dns_latency_critical: _Optional[float] = ...,
        dns_latency_warning: _Optional[float] = ...,
        dns_latency_critical_stddev: _Optional[float] = ...,
        dns_latency_warning_stddev: _Optional[float] = ...,
        per_agent_alerting: _Optional[bool] = ...,
        disabled_metrics: _Optional[_Union[DisabledMetrics, _Mapping]] = ...,
        health_disabled: _Optional[bool] = ...,
        throughput_critical: _Optional[float] = ...,
        throughput_warning: _Optional[float] = ...,
        throughput_critical_stddev: _Optional[float] = ...,
        throughput_warning_stddev: _Optional[float] = ...,
        disable_alerts: _Optional[bool] = ...,
    ) -> None: ...

class HostnameTest(_message.Message):
    __slots__ = ("target",)
    TARGET_FIELD_NUMBER: _ClassVar[int]
    target: str
    def __init__(self, target: _Optional[str] = ...) -> None: ...

class IpTest(_message.Message):
    __slots__ = ("targets", "use_local_ip")
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    USE_LOCAL_IP_FIELD_NUMBER: _ClassVar[int]
    targets: _containers.RepeatedScalarFieldContainer[str]
    use_local_ip: bool
    def __init__(
        self,
        targets: _Optional[_Iterable[str]] = ...,
        use_local_ip: _Optional[bool] = ...,
    ) -> None: ...

class AgentTest(_message.Message):
    __slots__ = ("target", "use_local_ip", "reciprocal")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    USE_LOCAL_IP_FIELD_NUMBER: _ClassVar[int]
    RECIPROCAL_FIELD_NUMBER: _ClassVar[int]
    target: str
    use_local_ip: bool
    reciprocal: bool
    def __init__(
        self,
        target: _Optional[str] = ...,
        use_local_ip: _Optional[bool] = ...,
        reciprocal: _Optional[bool] = ...,
    ) -> None: ...

class FlowTest(_message.Message):
    __slots__ = (
        "target",
        "target_refresh_interval_millis",
        "max_providers",
        "max_ip_targets",
        "type",
        "inet_direction",
        "direction",
    )
    TARGET_FIELD_NUMBER: _ClassVar[int]
    TARGET_REFRESH_INTERVAL_MILLIS_FIELD_NUMBER: _ClassVar[int]
    MAX_PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    MAX_IP_TARGETS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INET_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    target: str
    target_refresh_interval_millis: int
    max_providers: int
    max_ip_targets: int
    type: str
    inet_direction: str
    direction: str
    def __init__(
        self,
        target: _Optional[str] = ...,
        target_refresh_interval_millis: _Optional[int] = ...,
        max_providers: _Optional[int] = ...,
        max_ip_targets: _Optional[int] = ...,
        type: _Optional[str] = ...,
        inet_direction: _Optional[str] = ...,
        direction: _Optional[str] = ...,
    ) -> None: ...

class DnsTest(_message.Message):
    __slots__ = ("target", "timeout", "record_type", "servers", "port")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    RECORD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVERS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    target: str
    timeout: int
    record_type: DNSRecord
    servers: _containers.RepeatedScalarFieldContainer[str]
    port: int
    def __init__(
        self,
        target: _Optional[str] = ...,
        timeout: _Optional[int] = ...,
        record_type: _Optional[_Union[DNSRecord, str]] = ...,
        servers: _Optional[_Iterable[str]] = ...,
        port: _Optional[int] = ...,
    ) -> None: ...

class UrlTest(_message.Message):
    __slots__ = ("target", "timeout", "method", "headers", "body", "ignore_tls_errors")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    TARGET_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    IGNORE_TLS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    target: str
    timeout: int
    method: str
    headers: _containers.ScalarMap[str, str]
    body: str
    ignore_tls_errors: bool
    def __init__(
        self,
        target: _Optional[str] = ...,
        timeout: _Optional[int] = ...,
        method: _Optional[str] = ...,
        headers: _Optional[_Mapping[str, str]] = ...,
        body: _Optional[str] = ...,
        ignore_tls_errors: _Optional[bool] = ...,
    ) -> None: ...

class PageLoadTest(_message.Message):
    __slots__ = ("target", "timeout", "headers", "ignore_tls_errors", "css_selectors")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class CssSelectorsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    TARGET_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    IGNORE_TLS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    CSS_SELECTORS_FIELD_NUMBER: _ClassVar[int]
    target: str
    timeout: int
    headers: _containers.ScalarMap[str, str]
    ignore_tls_errors: bool
    css_selectors: _containers.ScalarMap[str, str]
    def __init__(
        self,
        target: _Optional[str] = ...,
        timeout: _Optional[int] = ...,
        headers: _Optional[_Mapping[str, str]] = ...,
        ignore_tls_errors: _Optional[bool] = ...,
        css_selectors: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class NetworkMeshTest(_message.Message):
    __slots__ = ("use_local_ip",)
    USE_LOCAL_IP_FIELD_NUMBER: _ClassVar[int]
    use_local_ip: bool
    def __init__(self, use_local_ip: _Optional[bool] = ...) -> None: ...

class MetricData(_message.Message):
    __slots__ = ("current", "rolling_avg", "rolling_stddev", "health")
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    ROLLING_AVG_FIELD_NUMBER: _ClassVar[int]
    ROLLING_STDDEV_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    current: int
    rolling_avg: int
    rolling_stddev: int
    health: str
    def __init__(
        self,
        current: _Optional[int] = ...,
        rolling_avg: _Optional[int] = ...,
        rolling_stddev: _Optional[int] = ...,
        health: _Optional[str] = ...,
    ) -> None: ...

class PacketLossData(_message.Message):
    __slots__ = ("current", "health")
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    current: float
    health: str
    def __init__(
        self, current: _Optional[float] = ..., health: _Optional[str] = ...
    ) -> None: ...

class PingResults(_message.Message):
    __slots__ = ("target", "packet_loss", "latency", "jitter", "dst_ip")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    PACKET_LOSS_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    JITTER_FIELD_NUMBER: _ClassVar[int]
    DST_IP_FIELD_NUMBER: _ClassVar[int]
    target: str
    packet_loss: PacketLossData
    latency: MetricData
    jitter: MetricData
    dst_ip: str
    def __init__(
        self,
        target: _Optional[str] = ...,
        packet_loss: _Optional[_Union[PacketLossData, _Mapping]] = ...,
        latency: _Optional[_Union[MetricData, _Mapping]] = ...,
        jitter: _Optional[_Union[MetricData, _Mapping]] = ...,
        dst_ip: _Optional[str] = ...,
    ) -> None: ...

class HTTPResponseData(_message.Message):
    __slots__ = ("status", "size", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: int
    size: int
    data: str
    def __init__(
        self,
        status: _Optional[int] = ...,
        size: _Optional[int] = ...,
        data: _Optional[str] = ...,
    ) -> None: ...

class HTTPResults(_message.Message):
    __slots__ = ("target", "latency", "response", "dst_ip")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    DST_IP_FIELD_NUMBER: _ClassVar[int]
    target: str
    latency: MetricData
    response: HTTPResponseData
    dst_ip: str
    def __init__(
        self,
        target: _Optional[str] = ...,
        latency: _Optional[_Union[MetricData, _Mapping]] = ...,
        response: _Optional[_Union[HTTPResponseData, _Mapping]] = ...,
        dst_ip: _Optional[str] = ...,
    ) -> None: ...

class DNSResponseData(_message.Message):
    __slots__ = ("status", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: int
    data: str
    def __init__(
        self, status: _Optional[int] = ..., data: _Optional[str] = ...
    ) -> None: ...

class DNSResults(_message.Message):
    __slots__ = ("target", "server", "latency", "response")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    target: str
    server: str
    latency: MetricData
    response: DNSResponseData
    def __init__(
        self,
        target: _Optional[str] = ...,
        server: _Optional[str] = ...,
        latency: _Optional[_Union[MetricData, _Mapping]] = ...,
        response: _Optional[_Union[DNSResponseData, _Mapping]] = ...,
    ) -> None: ...

class TaskResults(_message.Message):
    __slots__ = ("ping", "http", "dns", "health")
    PING_FIELD_NUMBER: _ClassVar[int]
    HTTP_FIELD_NUMBER: _ClassVar[int]
    DNS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    ping: PingResults
    http: HTTPResults
    dns: DNSResults
    health: str
    def __init__(
        self,
        ping: _Optional[_Union[PingResults, _Mapping]] = ...,
        http: _Optional[_Union[HTTPResults, _Mapping]] = ...,
        dns: _Optional[_Union[DNSResults, _Mapping]] = ...,
        health: _Optional[str] = ...,
    ) -> None: ...

class AgentResults(_message.Message):
    __slots__ = ("agent_id", "health", "tasks")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    health: str
    tasks: _containers.RepeatedCompositeFieldContainer[TaskResults]
    def __init__(
        self,
        agent_id: _Optional[str] = ...,
        health: _Optional[str] = ...,
        tasks: _Optional[_Iterable[_Union[TaskResults, _Mapping]]] = ...,
    ) -> None: ...

class TestResults(_message.Message):
    __slots__ = ("test_id", "time", "health", "agents")
    TEST_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    test_id: str
    time: _timestamp_pb2.Timestamp
    health: str
    agents: _containers.RepeatedCompositeFieldContainer[AgentResults]
    def __init__(
        self,
        test_id: _Optional[str] = ...,
        time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        health: _Optional[str] = ...,
        agents: _Optional[_Iterable[_Union[AgentResults, _Mapping]]] = ...,
    ) -> None: ...

class Stats(_message.Message):
    __slots__ = ("average", "min", "max")
    AVERAGE_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    average: int
    min: int
    max: int
    def __init__(
        self,
        average: _Optional[int] = ...,
        min: _Optional[int] = ...,
        max: _Optional[int] = ...,
    ) -> None: ...

class Location(_message.Message):
    __slots__ = ("latitude", "longitude", "country", "region", "city")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    country: str
    region: str
    city: str
    def __init__(
        self,
        latitude: _Optional[float] = ...,
        longitude: _Optional[float] = ...,
        country: _Optional[str] = ...,
        region: _Optional[str] = ...,
        city: _Optional[str] = ...,
    ) -> None: ...

class NetNode(_message.Message):
    __slots__ = ("ip", "asn", "as_name", "location", "dns_name", "device_id", "site_id")
    IP_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    AS_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    ip: str
    asn: int
    as_name: str
    location: Location
    dns_name: str
    device_id: str
    site_id: str
    def __init__(
        self,
        ip: _Optional[str] = ...,
        asn: _Optional[int] = ...,
        as_name: _Optional[str] = ...,
        location: _Optional[_Union[Location, _Mapping]] = ...,
        dns_name: _Optional[str] = ...,
        device_id: _Optional[str] = ...,
        site_id: _Optional[str] = ...,
    ) -> None: ...

class TraceHop(_message.Message):
    __slots__ = ("latency", "node_id")
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    latency: int
    node_id: str
    def __init__(
        self, latency: _Optional[int] = ..., node_id: _Optional[str] = ...
    ) -> None: ...

class PathTrace(_message.Message):
    __slots__ = ("as_path", "is_complete", "hops")
    AS_PATH_FIELD_NUMBER: _ClassVar[int]
    IS_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    HOPS_FIELD_NUMBER: _ClassVar[int]
    as_path: _containers.RepeatedScalarFieldContainer[int]
    is_complete: bool
    hops: _containers.RepeatedCompositeFieldContainer[TraceHop]
    def __init__(
        self,
        as_path: _Optional[_Iterable[int]] = ...,
        is_complete: _Optional[bool] = ...,
        hops: _Optional[_Iterable[_Union[TraceHop, _Mapping]]] = ...,
    ) -> None: ...

class Path(_message.Message):
    __slots__ = (
        "agent_id",
        "target_ip",
        "hop_count",
        "max_as_path_length",
        "traces",
        "time",
    )
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_IP_FIELD_NUMBER: _ClassVar[int]
    HOP_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_AS_PATH_LENGTH_FIELD_NUMBER: _ClassVar[int]
    TRACES_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    target_ip: str
    hop_count: Stats
    max_as_path_length: int
    traces: _containers.RepeatedCompositeFieldContainer[PathTrace]
    time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        agent_id: _Optional[str] = ...,
        target_ip: _Optional[str] = ...,
        hop_count: _Optional[_Union[Stats, _Mapping]] = ...,
        max_as_path_length: _Optional[int] = ...,
        traces: _Optional[_Iterable[_Union[PathTrace, _Mapping]]] = ...,
        time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class GetResultsForTestsRequest(_message.Message):
    __slots__ = ("ids", "start_time", "end_time", "agent_ids", "targets", "aggregate")
    IDS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    AGENT_IDS_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    agent_ids: _containers.RepeatedScalarFieldContainer[str]
    targets: _containers.RepeatedScalarFieldContainer[str]
    aggregate: bool
    def __init__(
        self,
        ids: _Optional[_Iterable[str]] = ...,
        start_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        agent_ids: _Optional[_Iterable[str]] = ...,
        targets: _Optional[_Iterable[str]] = ...,
        aggregate: _Optional[bool] = ...,
    ) -> None: ...

class GetResultsForTestsCsvRequest(_message.Message):
    __slots__ = ("ids", "start_time", "end_time", "agent_ids", "aggregate")
    IDS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    AGENT_IDS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    agent_ids: _containers.RepeatedScalarFieldContainer[str]
    aggregate: bool
    def __init__(
        self,
        ids: _Optional[_Iterable[str]] = ...,
        start_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        agent_ids: _Optional[_Iterable[str]] = ...,
        aggregate: _Optional[bool] = ...,
    ) -> None: ...

class GetResultsForTestsCsvResponse(_message.Message):
    __slots__ = ("content_type", "data")
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    content_type: str
    data: bytes
    def __init__(
        self, content_type: _Optional[str] = ..., data: _Optional[bytes] = ...
    ) -> None: ...

class GetResultsForTestsResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[TestResults]
    def __init__(
        self, results: _Optional[_Iterable[_Union[TestResults, _Mapping]]] = ...
    ) -> None: ...

class GetTraceForTestRequest(_message.Message):
    __slots__ = ("id", "start_time", "end_time", "agent_ids", "target_ips")
    ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    AGENT_IDS_FIELD_NUMBER: _ClassVar[int]
    TARGET_IPS_FIELD_NUMBER: _ClassVar[int]
    id: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    agent_ids: _containers.RepeatedScalarFieldContainer[str]
    target_ips: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        start_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        end_time: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        agent_ids: _Optional[_Iterable[str]] = ...,
        target_ips: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetTraceForTestResponse(_message.Message):
    __slots__ = ("nodes", "paths")
    class NodesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: NetNode
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[NetNode, _Mapping]] = ...,
        ) -> None: ...

    NODES_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.MessageMap[str, NetNode]
    paths: _containers.RepeatedCompositeFieldContainer[Path]
    def __init__(
        self,
        nodes: _Optional[_Mapping[str, NetNode]] = ...,
        paths: _Optional[_Iterable[_Union[Path, _Mapping]]] = ...,
    ) -> None: ...

class ListAgentsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAgentsResponse(_message.Message):
    __slots__ = ("agents", "invalid_count")
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    agents: _containers.RepeatedCompositeFieldContainer[Agent]
    invalid_count: int
    def __init__(
        self,
        agents: _Optional[_Iterable[_Union[Agent, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetAgentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetAgentResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    def __init__(self, agent: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...

class UpdateAgentRequest(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    def __init__(self, agent: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...

class UpdateAgentResponse(_message.Message):
    __slots__ = ("agent",)
    AGENT_FIELD_NUMBER: _ClassVar[int]
    agent: Agent
    def __init__(self, agent: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...

class DeleteAgentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteAgentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTestsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListTestsResponse(_message.Message):
    __slots__ = ("tests", "invalid_count")
    TESTS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    tests: _containers.RepeatedCompositeFieldContainer[Test]
    invalid_count: int
    def __init__(
        self,
        tests: _Optional[_Iterable[_Union[Test, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class CreateTestRequest(_message.Message):
    __slots__ = ("test",)
    TEST_FIELD_NUMBER: _ClassVar[int]
    test: Test
    def __init__(self, test: _Optional[_Union[Test, _Mapping]] = ...) -> None: ...

class CreateTestResponse(_message.Message):
    __slots__ = ("test",)
    TEST_FIELD_NUMBER: _ClassVar[int]
    test: Test
    def __init__(self, test: _Optional[_Union[Test, _Mapping]] = ...) -> None: ...

class GetTestRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetTestResponse(_message.Message):
    __slots__ = ("test",)
    TEST_FIELD_NUMBER: _ClassVar[int]
    test: Test
    def __init__(self, test: _Optional[_Union[Test, _Mapping]] = ...) -> None: ...

class UpdateTestRequest(_message.Message):
    __slots__ = ("test",)
    TEST_FIELD_NUMBER: _ClassVar[int]
    test: Test
    def __init__(self, test: _Optional[_Union[Test, _Mapping]] = ...) -> None: ...

class UpdateTestResponse(_message.Message):
    __slots__ = ("test",)
    TEST_FIELD_NUMBER: _ClassVar[int]
    test: Test
    def __init__(self, test: _Optional[_Union[Test, _Mapping]] = ...) -> None: ...

class DeleteTestRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteTestResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetTestStatusRequest(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: TestStatus
    def __init__(
        self, id: _Optional[str] = ..., status: _Optional[_Union[TestStatus, str]] = ...
    ) -> None: ...

class SetTestStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AgentAlert(_message.Message):
    __slots__ = (
        "id",
        "threshold_seconds",
        "notification_channel_ids",
        "agent_id",
        "agent_name",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_CHANNEL_IDS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    threshold_seconds: int
    notification_channel_ids: _containers.RepeatedScalarFieldContainer[str]
    agent_id: str
    agent_name: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        threshold_seconds: _Optional[int] = ...,
        notification_channel_ids: _Optional[_Iterable[str]] = ...,
        agent_id: _Optional[str] = ...,
        agent_name: _Optional[str] = ...,
    ) -> None: ...

class CreateAgentAlertRequest(_message.Message):
    __slots__ = ("threshold_seconds", "notification_channel_ids", "agent_id")
    THRESHOLD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_CHANNEL_IDS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    threshold_seconds: int
    notification_channel_ids: _containers.RepeatedScalarFieldContainer[str]
    agent_id: str
    def __init__(
        self,
        threshold_seconds: _Optional[int] = ...,
        notification_channel_ids: _Optional[_Iterable[str]] = ...,
        agent_id: _Optional[str] = ...,
    ) -> None: ...

class CreateAgentAlertResponse(_message.Message):
    __slots__ = ("agent_alert",)
    AGENT_ALERT_FIELD_NUMBER: _ClassVar[int]
    agent_alert: AgentAlert
    def __init__(
        self, agent_alert: _Optional[_Union[AgentAlert, _Mapping]] = ...
    ) -> None: ...

class UpdateAgentAlertRequest(_message.Message):
    __slots__ = ("id", "threshold_seconds", "notification_channel_ids")
    ID_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_CHANNEL_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    threshold_seconds: int
    notification_channel_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        threshold_seconds: _Optional[int] = ...,
        notification_channel_ids: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UpdateAgentAlertResponse(_message.Message):
    __slots__ = ("agent_alert",)
    AGENT_ALERT_FIELD_NUMBER: _ClassVar[int]
    agent_alert: AgentAlert
    def __init__(
        self, agent_alert: _Optional[_Union[AgentAlert, _Mapping]] = ...
    ) -> None: ...

class GetAgentAlertRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetAgentAlertResponse(_message.Message):
    __slots__ = ("agent_alert",)
    AGENT_ALERT_FIELD_NUMBER: _ClassVar[int]
    agent_alert: AgentAlert
    def __init__(
        self, agent_alert: _Optional[_Union[AgentAlert, _Mapping]] = ...
    ) -> None: ...

class ListAgentAlertsRequest(_message.Message):
    __slots__ = ("agent_ids",)
    AGENT_IDS_FIELD_NUMBER: _ClassVar[int]
    agent_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, agent_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListAgentAlertsResponse(_message.Message):
    __slots__ = ("agent_alerts",)
    AGENT_ALERTS_FIELD_NUMBER: _ClassVar[int]
    agent_alerts: _containers.RepeatedCompositeFieldContainer[AgentAlert]
    def __init__(
        self, agent_alerts: _Optional[_Iterable[_Union[AgentAlert, _Mapping]]] = ...
    ) -> None: ...

class DeleteAgentAlertRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteAgentAlertResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
