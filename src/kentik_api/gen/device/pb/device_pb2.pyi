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

DESCRIPTOR: _descriptor.FileDescriptor

class DeviceView(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEVICE_VIEW_UNSPECIFIED: _ClassVar[DeviceView]
    DEVICE_VIEW_FULL: _ClassVar[DeviceView]
    DEVICE_VIEW_BASIC: _ClassVar[DeviceView]
    DEVICE_VIEW_ID_ONLY: _ClassVar[DeviceView]

DEVICE_VIEW_UNSPECIFIED: DeviceView
DEVICE_VIEW_FULL: DeviceView
DEVICE_VIEW_BASIC: DeviceView
DEVICE_VIEW_ID_ONLY: DeviceView

class DeviceSnmpV3Conf(_message.Message):
    __slots__ = (
        "username",
        "authentication_protocol",
        "authentication_passphrase",
        "privacy_protocol",
        "privacy_passphrase",
    )
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_PASSPHRASE_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_PASSPHRASE_FIELD_NUMBER: _ClassVar[int]
    username: str
    authentication_protocol: str
    authentication_passphrase: str
    privacy_protocol: str
    privacy_passphrase: str
    def __init__(
        self,
        username: _Optional[str] = ...,
        authentication_protocol: _Optional[str] = ...,
        authentication_passphrase: _Optional[str] = ...,
        privacy_protocol: _Optional[str] = ...,
        privacy_passphrase: _Optional[str] = ...,
    ) -> None: ...

class DeviceNmsConfig(_message.Message):
    __slots__ = ("agent_id", "ip_address", "snmp", "st")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SNMP_FIELD_NUMBER: _ClassVar[int]
    ST_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    ip_address: str
    snmp: DeviceNmsSnmpConfig
    st: DeviceNmsStConfig
    def __init__(
        self,
        agent_id: _Optional[str] = ...,
        ip_address: _Optional[str] = ...,
        snmp: _Optional[_Union[DeviceNmsSnmpConfig, _Mapping]] = ...,
        st: _Optional[_Union[DeviceNmsStConfig, _Mapping]] = ...,
    ) -> None: ...

class DeviceNmsSnmpConfig(_message.Message):
    __slots__ = ("credential_name", "port", "timeout")
    CREDENTIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    credential_name: str
    port: int
    timeout: _duration_pb2.Duration
    def __init__(
        self,
        credential_name: _Optional[str] = ...,
        port: _Optional[int] = ...,
        timeout: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
    ) -> None: ...

class DeviceNmsStConfig(_message.Message):
    __slots__ = ("credential_name", "port", "timeout", "secure")
    CREDENTIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    SECURE_FIELD_NUMBER: _ClassVar[int]
    credential_name: str
    port: int
    timeout: _duration_pb2.Duration
    secure: bool
    def __init__(
        self,
        credential_name: _Optional[str] = ...,
        port: _Optional[int] = ...,
        timeout: _Optional[
            _Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]
        ] = ...,
        secure: _Optional[bool] = ...,
    ) -> None: ...

class DeviceConcise(_message.Message):
    __slots__ = (
        "id",
        "device_name",
        "device_subtype",
        "cdn_attr",
        "device_description",
        "sending_ips",
        "device_sample_rate",
        "plan_id",
        "site_id",
        "minimize_snmp",
        "device_snmp_ip",
        "device_snmp_community",
        "device_snmp_v3_conf",
        "device_bgp_type",
        "device_bgp_neighbor_ip",
        "device_bgp_neighbor_ip6",
        "device_bgp_neighbor_asn",
        "device_bgp_password",
        "use_bgp_device_id",
        "device_bgp_flowspec",
        "nms",
        "device_bgp_credential_name",
        "flow_snmp_credential_name",
        "monitoring_template_id",
        "device_alert",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    CDN_ATTR_FIELD_NUMBER: _ClassVar[int]
    DEVICE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SENDING_IPS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    MINIMIZE_SNMP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SNMP_IP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SNMP_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SNMP_V3_CONF_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_NEIGHBOR_IP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_NEIGHBOR_IP6_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_NEIGHBOR_ASN_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USE_BGP_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_FLOWSPEC_FIELD_NUMBER: _ClassVar[int]
    NMS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_CREDENTIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    FLOW_SNMP_CREDENTIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    MONITORING_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ALERT_FIELD_NUMBER: _ClassVar[int]
    id: str
    device_name: str
    device_subtype: str
    cdn_attr: str
    device_description: str
    sending_ips: _containers.RepeatedScalarFieldContainer[str]
    device_sample_rate: float
    plan_id: int
    site_id: int
    minimize_snmp: bool
    device_snmp_ip: str
    device_snmp_community: str
    device_snmp_v3_conf: DeviceSnmpV3Conf
    device_bgp_type: str
    device_bgp_neighbor_ip: str
    device_bgp_neighbor_ip6: str
    device_bgp_neighbor_asn: str
    device_bgp_password: str
    use_bgp_device_id: str
    device_bgp_flowspec: bool
    nms: DeviceNmsConfig
    device_bgp_credential_name: str
    flow_snmp_credential_name: str
    monitoring_template_id: int
    device_alert: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        device_name: _Optional[str] = ...,
        device_subtype: _Optional[str] = ...,
        cdn_attr: _Optional[str] = ...,
        device_description: _Optional[str] = ...,
        sending_ips: _Optional[_Iterable[str]] = ...,
        device_sample_rate: _Optional[float] = ...,
        plan_id: _Optional[int] = ...,
        site_id: _Optional[int] = ...,
        minimize_snmp: _Optional[bool] = ...,
        device_snmp_ip: _Optional[str] = ...,
        device_snmp_community: _Optional[str] = ...,
        device_snmp_v3_conf: _Optional[_Union[DeviceSnmpV3Conf, _Mapping]] = ...,
        device_bgp_type: _Optional[str] = ...,
        device_bgp_neighbor_ip: _Optional[str] = ...,
        device_bgp_neighbor_ip6: _Optional[str] = ...,
        device_bgp_neighbor_asn: _Optional[str] = ...,
        device_bgp_password: _Optional[str] = ...,
        use_bgp_device_id: _Optional[str] = ...,
        device_bgp_flowspec: _Optional[bool] = ...,
        nms: _Optional[_Union[DeviceNmsConfig, _Mapping]] = ...,
        device_bgp_credential_name: _Optional[str] = ...,
        flow_snmp_credential_name: _Optional[str] = ...,
        monitoring_template_id: _Optional[int] = ...,
        device_alert: _Optional[str] = ...,
    ) -> None: ...

class Site(_message.Message):
    __slots__ = ("id", "site_name", "lat", "lon", "company_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SITE_NAME_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    site_name: str
    lat: float
    lon: float
    company_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        site_name: _Optional[str] = ...,
        lat: _Optional[float] = ...,
        lon: _Optional[float] = ...,
        company_id: _Optional[str] = ...,
    ) -> None: ...

class Plan(_message.Message):
    __slots__ = (
        "id",
        "name",
        "active",
        "bgp",
        "company_id",
        "description",
        "device_types",
        "devices",
        "fast_retention",
        "full_retention",
        "max_bigdata_fps",
        "max_devices",
        "max_fps",
        "cdate",
        "edate",
        "metadata",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    BGP_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPES_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    FAST_RETENTION_FIELD_NUMBER: _ClassVar[int]
    FULL_RETENTION_FIELD_NUMBER: _ClassVar[int]
    MAX_BIGDATA_FPS_FIELD_NUMBER: _ClassVar[int]
    MAX_DEVICES_FIELD_NUMBER: _ClassVar[int]
    MAX_FPS_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    active: bool
    bgp: bool
    company_id: str
    description: str
    device_types: _containers.RepeatedScalarFieldContainer[str]
    devices: _containers.RepeatedScalarFieldContainer[str]
    fast_retention: int
    full_retention: int
    max_bigdata_fps: int
    max_devices: int
    max_fps: int
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        active: _Optional[bool] = ...,
        bgp: _Optional[bool] = ...,
        company_id: _Optional[str] = ...,
        description: _Optional[str] = ...,
        device_types: _Optional[_Iterable[str]] = ...,
        devices: _Optional[_Iterable[str]] = ...,
        fast_retention: _Optional[int] = ...,
        full_retention: _Optional[int] = ...,
        max_bigdata_fps: _Optional[int] = ...,
        max_devices: _Optional[int] = ...,
        max_fps: _Optional[int] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class Label(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "edate",
        "cdate",
        "user_id",
        "company_id",
        "color",
        "order",
        "pivot_device_id",
        "pivot_label_id",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PIVOT_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    PIVOT_LABEL_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    edate: _timestamp_pb2.Timestamp
    cdate: _timestamp_pb2.Timestamp
    user_id: str
    company_id: str
    color: str
    order: str
    pivot_device_id: str
    pivot_label_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        user_id: _Optional[str] = ...,
        company_id: _Optional[str] = ...,
        color: _Optional[str] = ...,
        order: _Optional[str] = ...,
        pivot_device_id: _Optional[str] = ...,
        pivot_label_id: _Optional[str] = ...,
    ) -> None: ...

class Interface(_message.Message):
    __slots__ = (
        "interface_description",
        "initial_snmp_speed",
        "device_id",
        "snmp_speed",
        "snmp_alias",
        "snmp_id",
        "connectivity_type",
        "network_boundary",
        "provider",
    )
    INTERFACE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SNMP_SPEED_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SNMP_SPEED_FIELD_NUMBER: _ClassVar[int]
    SNMP_ALIAS_FIELD_NUMBER: _ClassVar[int]
    SNMP_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    interface_description: str
    initial_snmp_speed: str
    device_id: str
    snmp_speed: str
    snmp_alias: str
    snmp_id: str
    connectivity_type: str
    network_boundary: str
    provider: str
    def __init__(
        self,
        interface_description: _Optional[str] = ...,
        initial_snmp_speed: _Optional[str] = ...,
        device_id: _Optional[str] = ...,
        snmp_speed: _Optional[str] = ...,
        snmp_alias: _Optional[str] = ...,
        snmp_id: _Optional[str] = ...,
        connectivity_type: _Optional[str] = ...,
        network_boundary: _Optional[str] = ...,
        provider: _Optional[str] = ...,
    ) -> None: ...

class CustomColumnData(_message.Message):
    __slots__ = (
        "device_id",
        "field_id",
        "col_name",
        "description",
        "col_type",
        "device_type",
    )
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    COL_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COL_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    field_id: str
    col_name: str
    description: str
    col_type: str
    device_type: str
    def __init__(
        self,
        device_id: _Optional[str] = ...,
        field_id: _Optional[str] = ...,
        col_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        col_type: _Optional[str] = ...,
        device_type: _Optional[str] = ...,
    ) -> None: ...

class GnmiV1Conf(_message.Message):
    __slots__ = ("dialout_server",)
    DIALOUT_SERVER_FIELD_NUMBER: _ClassVar[int]
    dialout_server: str
    def __init__(self, dialout_server: _Optional[str] = ...) -> None: ...

class DeviceDetailed(_message.Message):
    __slots__ = (
        "id",
        "company_id",
        "device_name",
        "device_alias",
        "device_type",
        "device_description",
        "site",
        "plan",
        "labels",
        "all_interfaces",
        "device_flow_type",
        "device_sample_rate",
        "sending_ips",
        "device_snmp_ip",
        "device_snmp_community",
        "minimize_snmp",
        "device_bgp_type",
        "device_bgp_neighbor_ip",
        "device_bgp_neighbor_ip6",
        "device_bgp_neighbor_asn",
        "device_bgp_flowspec",
        "device_bgp_password",
        "device_bgp_label_unicast",
        "bgp_lookup_strategy",
        "device_status",
        "use_bgp_device_id",
        "custom_columns",
        "custom_column_data",
        "device_chf_client_port",
        "device_chf_client_protocol",
        "device_chf_interface",
        "device_agent_type",
        "max_flow_rate",
        "max_big_flow_rate",
        "device_proxy_bgp",
        "device_proxy_bgp6",
        "created_date",
        "updated_date",
        "device_snmp_v3_conf_enabled",
        "device_snmp_v3_conf",
        "cdn_attr",
        "bgp_peer_ip4",
        "bgp_peer_ip6",
        "device_subtype",
        "device_vendor_type",
        "device_model_type",
        "cloud_export_id",
        "device_kproxy",
        "snmp_enabled",
        "snmp_disabled_reason",
        "snmp_disabled_reason_other",
        "bgp_disabled_reason",
        "bgp_disabled_reason_other",
        "device_manufacturer",
        "device_alert",
        "role",
        "device_gnmi_v1_conf",
        "use_asn_from_flow",
        "max_interface",
        "max_interface_check",
        "nms",
        "device_bgp_credential_name",
        "flow_snmp_credential_name",
        "monitoring_template_id",
        "os_name",
        "os_version",
        "serial_number",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ALIAS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SITE_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ALL_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FLOW_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    SENDING_IPS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SNMP_IP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SNMP_COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    MINIMIZE_SNMP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_NEIGHBOR_IP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_NEIGHBOR_IP6_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_NEIGHBOR_ASN_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_FLOWSPEC_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_LABEL_UNICAST_FIELD_NUMBER: _ClassVar[int]
    BGP_LOOKUP_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    DEVICE_STATUS_FIELD_NUMBER: _ClassVar[int]
    USE_BGP_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_COLUMN_DATA_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CHF_CLIENT_PORT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CHF_CLIENT_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CHF_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_AGENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAX_FLOW_RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_BIG_FLOW_RATE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_PROXY_BGP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_PROXY_BGP6_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SNMP_V3_CONF_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SNMP_V3_CONF_FIELD_NUMBER: _ClassVar[int]
    CDN_ATTR_FIELD_NUMBER: _ClassVar[int]
    BGP_PEER_IP4_FIELD_NUMBER: _ClassVar[int]
    BGP_PEER_IP6_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_VENDOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MODEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLOUD_EXPORT_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_KPROXY_FIELD_NUMBER: _ClassVar[int]
    SNMP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SNMP_DISABLED_REASON_FIELD_NUMBER: _ClassVar[int]
    SNMP_DISABLED_REASON_OTHER_FIELD_NUMBER: _ClassVar[int]
    BGP_DISABLED_REASON_FIELD_NUMBER: _ClassVar[int]
    BGP_DISABLED_REASON_OTHER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ALERT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_GNMI_V1_CONF_FIELD_NUMBER: _ClassVar[int]
    USE_ASN_FROM_FLOW_FIELD_NUMBER: _ClassVar[int]
    MAX_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MAX_INTERFACE_CHECK_FIELD_NUMBER: _ClassVar[int]
    NMS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_BGP_CREDENTIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    FLOW_SNMP_CREDENTIAL_NAME_FIELD_NUMBER: _ClassVar[int]
    MONITORING_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    OS_NAME_FIELD_NUMBER: _ClassVar[int]
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    id: str
    company_id: str
    device_name: str
    device_alias: str
    device_type: str
    device_description: str
    site: Site
    plan: Plan
    labels: _containers.RepeatedCompositeFieldContainer[Label]
    all_interfaces: _containers.RepeatedCompositeFieldContainer[Interface]
    device_flow_type: str
    device_sample_rate: str
    sending_ips: _containers.RepeatedScalarFieldContainer[str]
    device_snmp_ip: str
    device_snmp_community: str
    minimize_snmp: bool
    device_bgp_type: str
    device_bgp_neighbor_ip: str
    device_bgp_neighbor_ip6: str
    device_bgp_neighbor_asn: str
    device_bgp_flowspec: bool
    device_bgp_password: str
    device_bgp_label_unicast: bool
    bgp_lookup_strategy: str
    device_status: str
    use_bgp_device_id: str
    custom_columns: str
    custom_column_data: _containers.RepeatedCompositeFieldContainer[CustomColumnData]
    device_chf_client_port: str
    device_chf_client_protocol: str
    device_chf_interface: str
    device_agent_type: str
    max_flow_rate: int
    max_big_flow_rate: int
    device_proxy_bgp: str
    device_proxy_bgp6: str
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    device_snmp_v3_conf_enabled: bool
    device_snmp_v3_conf: DeviceSnmpV3Conf
    cdn_attr: str
    bgp_peer_ip4: str
    bgp_peer_ip6: str
    device_subtype: str
    device_vendor_type: str
    device_model_type: str
    cloud_export_id: str
    device_kproxy: str
    snmp_enabled: str
    snmp_disabled_reason: str
    snmp_disabled_reason_other: str
    bgp_disabled_reason: str
    bgp_disabled_reason_other: str
    device_manufacturer: str
    device_alert: str
    role: str
    device_gnmi_v1_conf: GnmiV1Conf
    use_asn_from_flow: bool
    max_interface: int
    max_interface_check: int
    nms: DeviceNmsConfig
    device_bgp_credential_name: str
    flow_snmp_credential_name: str
    monitoring_template_id: int
    os_name: str
    os_version: str
    serial_number: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        company_id: _Optional[str] = ...,
        device_name: _Optional[str] = ...,
        device_alias: _Optional[str] = ...,
        device_type: _Optional[str] = ...,
        device_description: _Optional[str] = ...,
        site: _Optional[_Union[Site, _Mapping]] = ...,
        plan: _Optional[_Union[Plan, _Mapping]] = ...,
        labels: _Optional[_Iterable[_Union[Label, _Mapping]]] = ...,
        all_interfaces: _Optional[_Iterable[_Union[Interface, _Mapping]]] = ...,
        device_flow_type: _Optional[str] = ...,
        device_sample_rate: _Optional[str] = ...,
        sending_ips: _Optional[_Iterable[str]] = ...,
        device_snmp_ip: _Optional[str] = ...,
        device_snmp_community: _Optional[str] = ...,
        minimize_snmp: _Optional[bool] = ...,
        device_bgp_type: _Optional[str] = ...,
        device_bgp_neighbor_ip: _Optional[str] = ...,
        device_bgp_neighbor_ip6: _Optional[str] = ...,
        device_bgp_neighbor_asn: _Optional[str] = ...,
        device_bgp_flowspec: _Optional[bool] = ...,
        device_bgp_password: _Optional[str] = ...,
        device_bgp_label_unicast: _Optional[bool] = ...,
        bgp_lookup_strategy: _Optional[str] = ...,
        device_status: _Optional[str] = ...,
        use_bgp_device_id: _Optional[str] = ...,
        custom_columns: _Optional[str] = ...,
        custom_column_data: _Optional[
            _Iterable[_Union[CustomColumnData, _Mapping]]
        ] = ...,
        device_chf_client_port: _Optional[str] = ...,
        device_chf_client_protocol: _Optional[str] = ...,
        device_chf_interface: _Optional[str] = ...,
        device_agent_type: _Optional[str] = ...,
        max_flow_rate: _Optional[int] = ...,
        max_big_flow_rate: _Optional[int] = ...,
        device_proxy_bgp: _Optional[str] = ...,
        device_proxy_bgp6: _Optional[str] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        device_snmp_v3_conf_enabled: _Optional[bool] = ...,
        device_snmp_v3_conf: _Optional[_Union[DeviceSnmpV3Conf, _Mapping]] = ...,
        cdn_attr: _Optional[str] = ...,
        bgp_peer_ip4: _Optional[str] = ...,
        bgp_peer_ip6: _Optional[str] = ...,
        device_subtype: _Optional[str] = ...,
        device_vendor_type: _Optional[str] = ...,
        device_model_type: _Optional[str] = ...,
        cloud_export_id: _Optional[str] = ...,
        device_kproxy: _Optional[str] = ...,
        snmp_enabled: _Optional[str] = ...,
        snmp_disabled_reason: _Optional[str] = ...,
        snmp_disabled_reason_other: _Optional[str] = ...,
        bgp_disabled_reason: _Optional[str] = ...,
        bgp_disabled_reason_other: _Optional[str] = ...,
        device_manufacturer: _Optional[str] = ...,
        device_alert: _Optional[str] = ...,
        role: _Optional[str] = ...,
        device_gnmi_v1_conf: _Optional[_Union[GnmiV1Conf, _Mapping]] = ...,
        use_asn_from_flow: _Optional[bool] = ...,
        max_interface: _Optional[int] = ...,
        max_interface_check: _Optional[int] = ...,
        nms: _Optional[_Union[DeviceNmsConfig, _Mapping]] = ...,
        device_bgp_credential_name: _Optional[str] = ...,
        flow_snmp_credential_name: _Optional[str] = ...,
        monitoring_template_id: _Optional[int] = ...,
        os_name: _Optional[str] = ...,
        os_version: _Optional[str] = ...,
        serial_number: _Optional[str] = ...,
    ) -> None: ...

class DeviceQuery(_message.Message):
    __slots__ = ("no_custom_columns",)
    NO_CUSTOM_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    no_custom_columns: bool
    def __init__(self, no_custom_columns: _Optional[bool] = ...) -> None: ...

class LabelConcise(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ListDevicesRequest(_message.Message):
    __slots__ = ("query", "view")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    VIEW_FIELD_NUMBER: _ClassVar[int]
    query: DeviceQuery
    view: DeviceView
    def __init__(
        self,
        query: _Optional[_Union[DeviceQuery, _Mapping]] = ...,
        view: _Optional[_Union[DeviceView, str]] = ...,
    ) -> None: ...

class ListDevicesResponse(_message.Message):
    __slots__ = ("devices", "invalid_count")
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[DeviceDetailed]
    invalid_count: int
    def __init__(
        self,
        devices: _Optional[_Iterable[_Union[DeviceDetailed, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetDeviceRequest(_message.Message):
    __slots__ = ("id", "query")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    id: str
    query: DeviceQuery
    def __init__(
        self,
        id: _Optional[str] = ...,
        query: _Optional[_Union[DeviceQuery, _Mapping]] = ...,
    ) -> None: ...

class GetDeviceResponse(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: DeviceDetailed
    def __init__(
        self, device: _Optional[_Union[DeviceDetailed, _Mapping]] = ...
    ) -> None: ...

class GetDeviceByNameRequest(_message.Message):
    __slots__ = ("device_name", "query")
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    query: DeviceQuery
    def __init__(
        self,
        device_name: _Optional[str] = ...,
        query: _Optional[_Union[DeviceQuery, _Mapping]] = ...,
    ) -> None: ...

class GetDeviceByNameResponse(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: DeviceDetailed
    def __init__(
        self, device: _Optional[_Union[DeviceDetailed, _Mapping]] = ...
    ) -> None: ...

class CreateDeviceRequest(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: DeviceConcise
    def __init__(
        self, device: _Optional[_Union[DeviceConcise, _Mapping]] = ...
    ) -> None: ...

class CreateDeviceResponse(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: DeviceDetailed
    def __init__(
        self, device: _Optional[_Union[DeviceDetailed, _Mapping]] = ...
    ) -> None: ...

class CreateDevicesRequest(_message.Message):
    __slots__ = ("devices",)
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[DeviceConcise]
    def __init__(
        self, devices: _Optional[_Iterable[_Union[DeviceConcise, _Mapping]]] = ...
    ) -> None: ...

class CreateDevicesResponse(_message.Message):
    __slots__ = ("devices", "failed_devices")
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    FAILED_DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[DeviceDetailed]
    failed_devices: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        devices: _Optional[_Iterable[_Union[DeviceDetailed, _Mapping]]] = ...,
        failed_devices: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UpdateDeviceRequest(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: DeviceConcise
    def __init__(
        self, device: _Optional[_Union[DeviceConcise, _Mapping]] = ...
    ) -> None: ...

class UpdateDeviceResponse(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: DeviceDetailed
    def __init__(
        self, device: _Optional[_Union[DeviceDetailed, _Mapping]] = ...
    ) -> None: ...

class UpdateDevicesRequest(_message.Message):
    __slots__ = ("devices",)
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[DeviceConcise]
    def __init__(
        self, devices: _Optional[_Iterable[_Union[DeviceConcise, _Mapping]]] = ...
    ) -> None: ...

class UpdateDevicesResponse(_message.Message):
    __slots__ = ("devices", "failed_devices")
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    FAILED_DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[DeviceDetailed]
    failed_devices: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        devices: _Optional[_Iterable[_Union[DeviceDetailed, _Mapping]]] = ...,
        failed_devices: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UpdateDeviceLabelsRequest(_message.Message):
    __slots__ = ("id", "labels")
    ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    id: str
    labels: _containers.RepeatedCompositeFieldContainer[LabelConcise]
    def __init__(
        self,
        id: _Optional[str] = ...,
        labels: _Optional[_Iterable[_Union[LabelConcise, _Mapping]]] = ...,
    ) -> None: ...

class UpdateDeviceLabelsResponse(_message.Message):
    __slots__ = ("device",)
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: DeviceDetailed
    def __init__(
        self, device: _Optional[_Union[DeviceDetailed, _Mapping]] = ...
    ) -> None: ...

class DeleteDeviceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDeviceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteDevicesRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteDevicesResponse(_message.Message):
    __slots__ = ("failed_devices",)
    FAILED_DEVICES_FIELD_NUMBER: _ClassVar[int]
    failed_devices: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, failed_devices: _Optional[_Iterable[str]] = ...) -> None: ...
