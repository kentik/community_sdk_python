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

class ConnectivityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECTIVITY_TYPE_UNSPECIFIED: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_AGGREGATION_INTERCONNECT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_AVAILABLE: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_BACKBONE: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_CLOUD_INTERCONNECT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_CUSTOMER: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_DATACENTER_FABRIC: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_DATACENTER_INTERCONNECT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_EMBEDDED_CACHE: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_FREE_PNI: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_HOST: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_IX: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_OTHER: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_PAID_PNI: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_RESERVED: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_TRANSIT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_VIRTUAL_CROSS_CONNECT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_IPX_INTERCONNECT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_SIP_INTERCONNECT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_DDOS_EXT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_DDOS_INT: _ClassVar[ConnectivityType]
    CONNECTIVITY_TYPE_MGT: _ClassVar[ConnectivityType]

class NetworkBoundary(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NETWORK_BOUNDARY_UNSPECIFIED: _ClassVar[NetworkBoundary]
    NETWORK_BOUNDARY_AUTO: _ClassVar[NetworkBoundary]
    NETWORK_BOUNDARY_INTERNAL: _ClassVar[NetworkBoundary]
    NETWORK_BOUNDARY_EXTERNAL: _ClassVar[NetworkBoundary]
    NETWORK_BOUNDARY_NONE: _ClassVar[NetworkBoundary]

class IpFilter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IP_FILTER_UNSPECIFIED: _ClassVar[IpFilter]
    IP_FILTER_PRIVATE: _ClassVar[IpFilter]
    IP_FILTER_PUBLIC: _ClassVar[IpFilter]
    IP_FILTER_UNSET: _ClassVar[IpFilter]

class MatchAttribute(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MATCH_ATTRIBUTE_UNSPECIFIED: _ClassVar[MatchAttribute]
    MATCH_ATTRIBUTE_INTERFACE_DESCRIPTION: _ClassVar[MatchAttribute]
    MATCH_ATTRIBUTE_SNMP_ALIAS: _ClassVar[MatchAttribute]
    MATCH_ATTRIBUTE_INTERFACE_IP: _ClassVar[MatchAttribute]

class Operator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATOR_UNSPECIFIED: _ClassVar[Operator]
    OPERATOR_EQUALS: _ClassVar[Operator]
    OPERATOR_CONTAINS: _ClassVar[Operator]
    OPERATOR_REGEX: _ClassVar[Operator]
    OPERATOR_CONTAINED_IN_SUBNET: _ClassVar[Operator]
    OPERATOR_IS_PUBLIC_IP: _ClassVar[Operator]
    OPERATOR_IS_PRIVATE_IP: _ClassVar[Operator]
    OPERATOR_NO_IP: _ClassVar[Operator]

CONNECTIVITY_TYPE_UNSPECIFIED: ConnectivityType
CONNECTIVITY_TYPE_AGGREGATION_INTERCONNECT: ConnectivityType
CONNECTIVITY_TYPE_AVAILABLE: ConnectivityType
CONNECTIVITY_TYPE_BACKBONE: ConnectivityType
CONNECTIVITY_TYPE_CLOUD_INTERCONNECT: ConnectivityType
CONNECTIVITY_TYPE_CUSTOMER: ConnectivityType
CONNECTIVITY_TYPE_DATACENTER_FABRIC: ConnectivityType
CONNECTIVITY_TYPE_DATACENTER_INTERCONNECT: ConnectivityType
CONNECTIVITY_TYPE_EMBEDDED_CACHE: ConnectivityType
CONNECTIVITY_TYPE_FREE_PNI: ConnectivityType
CONNECTIVITY_TYPE_HOST: ConnectivityType
CONNECTIVITY_TYPE_IX: ConnectivityType
CONNECTIVITY_TYPE_OTHER: ConnectivityType
CONNECTIVITY_TYPE_PAID_PNI: ConnectivityType
CONNECTIVITY_TYPE_RESERVED: ConnectivityType
CONNECTIVITY_TYPE_TRANSIT: ConnectivityType
CONNECTIVITY_TYPE_VIRTUAL_CROSS_CONNECT: ConnectivityType
CONNECTIVITY_TYPE_IPX_INTERCONNECT: ConnectivityType
CONNECTIVITY_TYPE_SIP_INTERCONNECT: ConnectivityType
CONNECTIVITY_TYPE_DDOS_EXT: ConnectivityType
CONNECTIVITY_TYPE_DDOS_INT: ConnectivityType
CONNECTIVITY_TYPE_MGT: ConnectivityType
NETWORK_BOUNDARY_UNSPECIFIED: NetworkBoundary
NETWORK_BOUNDARY_AUTO: NetworkBoundary
NETWORK_BOUNDARY_INTERNAL: NetworkBoundary
NETWORK_BOUNDARY_EXTERNAL: NetworkBoundary
NETWORK_BOUNDARY_NONE: NetworkBoundary
IP_FILTER_UNSPECIFIED: IpFilter
IP_FILTER_PRIVATE: IpFilter
IP_FILTER_PUBLIC: IpFilter
IP_FILTER_UNSET: IpFilter
MATCH_ATTRIBUTE_UNSPECIFIED: MatchAttribute
MATCH_ATTRIBUTE_INTERFACE_DESCRIPTION: MatchAttribute
MATCH_ATTRIBUTE_SNMP_ALIAS: MatchAttribute
MATCH_ATTRIBUTE_INTERFACE_IP: MatchAttribute
OPERATOR_UNSPECIFIED: Operator
OPERATOR_EQUALS: Operator
OPERATOR_CONTAINS: Operator
OPERATOR_REGEX: Operator
OPERATOR_CONTAINED_IN_SUBNET: Operator
OPERATOR_IS_PUBLIC_IP: Operator
OPERATOR_IS_PRIVATE_IP: Operator
OPERATOR_NO_IP: Operator

class InterfaceVrf(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "route_distinguisher",
        "ext_route_distinguisher",
        "route_target",
        "route_targets",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ROUTE_DISTINGUISHER_FIELD_NUMBER: _ClassVar[int]
    EXT_ROUTE_DISTINGUISHER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_TARGET_FIELD_NUMBER: _ClassVar[int]
    ROUTE_TARGETS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    route_distinguisher: str
    ext_route_distinguisher: int
    route_target: str
    route_targets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        route_distinguisher: _Optional[str] = ...,
        ext_route_distinguisher: _Optional[int] = ...,
        route_target: _Optional[str] = ...,
        route_targets: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class Interface(_message.Message):
    __slots__ = (
        "id",
        "device_id",
        "snmp_id",
        "snmp_speed",
        "snmp_type",
        "snmp_alias",
        "interface_ip",
        "interface_description",
        "cdate",
        "edate",
        "interface_ip_netmask",
        "connectivity_type",
        "network_boundary",
        "top_nexthop_asns",
        "provider",
        "interface_kvs",
        "interface_tags",
        "interface_status",
        "extra_info",
        "initial_snmp_id",
        "initial_snmp_alias",
        "initial_interface_description",
        "initial_snmp_speed",
        "secondary_ips",
        "initial_connectivity_type",
        "initial_network_boundary",
        "initial_provider",
        "vrf_id",
        "vrf",
    )
    class InterfaceKvsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class InterfaceTagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    class ExtraInfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SNMP_ID_FIELD_NUMBER: _ClassVar[int]
    SNMP_SPEED_FIELD_NUMBER: _ClassVar[int]
    SNMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    SNMP_ALIAS_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_IP_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_IP_NETMASK_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    TOP_NEXTHOP_ASNS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_KVS_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_TAGS_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_STATUS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFO_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SNMP_ID_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SNMP_ALIAS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_INTERFACE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SNMP_SPEED_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_IPS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_CONNECTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_NETWORK_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    INITIAL_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    VRF_ID_FIELD_NUMBER: _ClassVar[int]
    VRF_FIELD_NUMBER: _ClassVar[int]
    id: str
    device_id: str
    snmp_id: str
    snmp_speed: int
    snmp_type: int
    snmp_alias: str
    interface_ip: str
    interface_description: str
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    interface_ip_netmask: str
    connectivity_type: ConnectivityType
    network_boundary: NetworkBoundary
    top_nexthop_asns: _containers.RepeatedScalarFieldContainer[int]
    provider: str
    interface_kvs: _containers.ScalarMap[str, str]
    interface_tags: _containers.ScalarMap[str, str]
    interface_status: str
    extra_info: _containers.ScalarMap[str, str]
    initial_snmp_id: str
    initial_snmp_alias: str
    initial_interface_description: str
    initial_snmp_speed: int
    secondary_ips: str
    initial_connectivity_type: ConnectivityType
    initial_network_boundary: NetworkBoundary
    initial_provider: str
    vrf_id: str
    vrf: InterfaceVrf
    def __init__(
        self,
        id: _Optional[str] = ...,
        device_id: _Optional[str] = ...,
        snmp_id: _Optional[str] = ...,
        snmp_speed: _Optional[int] = ...,
        snmp_type: _Optional[int] = ...,
        snmp_alias: _Optional[str] = ...,
        interface_ip: _Optional[str] = ...,
        interface_description: _Optional[str] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        interface_ip_netmask: _Optional[str] = ...,
        connectivity_type: _Optional[_Union[ConnectivityType, str]] = ...,
        network_boundary: _Optional[_Union[NetworkBoundary, str]] = ...,
        top_nexthop_asns: _Optional[_Iterable[int]] = ...,
        provider: _Optional[str] = ...,
        interface_kvs: _Optional[_Mapping[str, str]] = ...,
        interface_tags: _Optional[_Mapping[str, str]] = ...,
        interface_status: _Optional[str] = ...,
        extra_info: _Optional[_Mapping[str, str]] = ...,
        initial_snmp_id: _Optional[str] = ...,
        initial_snmp_alias: _Optional[str] = ...,
        initial_interface_description: _Optional[str] = ...,
        initial_snmp_speed: _Optional[int] = ...,
        secondary_ips: _Optional[str] = ...,
        initial_connectivity_type: _Optional[_Union[ConnectivityType, str]] = ...,
        initial_network_boundary: _Optional[_Union[NetworkBoundary, str]] = ...,
        initial_provider: _Optional[str] = ...,
        vrf_id: _Optional[str] = ...,
        vrf: _Optional[_Union[InterfaceVrf, _Mapping]] = ...,
    ) -> None: ...

class InterfaceClassification(_message.Message):
    __slots__ = ("classified", "connectivity_type", "network_boundary")
    CLASSIFIED_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    classified: bool
    connectivity_type: ConnectivityType
    network_boundary: NetworkBoundary
    def __init__(
        self,
        classified: _Optional[bool] = ...,
        connectivity_type: _Optional[_Union[ConnectivityType, str]] = ...,
        network_boundary: _Optional[_Union[NetworkBoundary, str]] = ...,
    ) -> None: ...

class ClassifyCounter(_message.Message):
    __slots__ = (
        "count",
        "external_count",
        "free_pni_count",
        "ix_count",
        "provider_count",
        "transit_count",
    )
    COUNT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    FREE_PNI_COUNT_FIELD_NUMBER: _ClassVar[int]
    IX_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    external_count: int
    free_pni_count: int
    ix_count: int
    provider_count: int
    transit_count: int
    def __init__(
        self,
        count: _Optional[int] = ...,
        external_count: _Optional[int] = ...,
        free_pni_count: _Optional[int] = ...,
        ix_count: _Optional[int] = ...,
        provider_count: _Optional[int] = ...,
        transit_count: _Optional[int] = ...,
    ) -> None: ...

class InterfaceClassifyInfo(_message.Message):
    __slots__ = (
        "device_id",
        "snmp_id",
        "snmp_alias",
        "interface_ip",
        "interface_ip_asn",
        "is_internal_ip",
        "is_internal_asn",
        "top_nexthop_asns",
        "pdb_global_name",
        "auto_classification",
        "previous_classification",
        "provider",
        "network_boundary_confidence",
        "connectivity_type_confidence",
        "provider_confidence",
        "auto_classified_provider",
        "previously_classified_provider",
        "previously_classified_external",
        "ip_asn_matched",
        "ix_matched",
        "nexthop_matched",
        "connectivity_type_matched",
        "provider_matched",
        "changed_classification",
    )
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SNMP_ID_FIELD_NUMBER: _ClassVar[int]
    SNMP_ALIAS_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_IP_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_IP_ASN_FIELD_NUMBER: _ClassVar[int]
    IS_INTERNAL_IP_FIELD_NUMBER: _ClassVar[int]
    IS_INTERNAL_ASN_FIELD_NUMBER: _ClassVar[int]
    TOP_NEXTHOP_ASNS_FIELD_NUMBER: _ClassVar[int]
    PDB_GLOBAL_NAME_FIELD_NUMBER: _ClassVar[int]
    AUTO_CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    NETWORK_BOUNDARY_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPE_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    AUTO_CLASSIFIED_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PREVIOUSLY_CLASSIFIED_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    PREVIOUSLY_CLASSIFIED_EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    IP_ASN_MATCHED_FIELD_NUMBER: _ClassVar[int]
    IX_MATCHED_FIELD_NUMBER: _ClassVar[int]
    NEXTHOP_MATCHED_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPE_MATCHED_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_MATCHED_FIELD_NUMBER: _ClassVar[int]
    CHANGED_CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    snmp_id: str
    snmp_alias: str
    interface_ip: str
    interface_ip_asn: str
    is_internal_ip: bool
    is_internal_asn: bool
    top_nexthop_asns: _containers.RepeatedScalarFieldContainer[str]
    pdb_global_name: str
    auto_classification: InterfaceClassification
    previous_classification: InterfaceClassification
    provider: str
    network_boundary_confidence: int
    connectivity_type_confidence: int
    provider_confidence: int
    auto_classified_provider: bool
    previously_classified_provider: str
    previously_classified_external: bool
    ip_asn_matched: bool
    ix_matched: bool
    nexthop_matched: bool
    connectivity_type_matched: bool
    provider_matched: bool
    changed_classification: bool
    def __init__(
        self,
        device_id: _Optional[str] = ...,
        snmp_id: _Optional[str] = ...,
        snmp_alias: _Optional[str] = ...,
        interface_ip: _Optional[str] = ...,
        interface_ip_asn: _Optional[str] = ...,
        is_internal_ip: _Optional[bool] = ...,
        is_internal_asn: _Optional[bool] = ...,
        top_nexthop_asns: _Optional[_Iterable[str]] = ...,
        pdb_global_name: _Optional[str] = ...,
        auto_classification: _Optional[_Union[InterfaceClassification, _Mapping]] = ...,
        previous_classification: _Optional[
            _Union[InterfaceClassification, _Mapping]
        ] = ...,
        provider: _Optional[str] = ...,
        network_boundary_confidence: _Optional[int] = ...,
        connectivity_type_confidence: _Optional[int] = ...,
        provider_confidence: _Optional[int] = ...,
        auto_classified_provider: _Optional[bool] = ...,
        previously_classified_provider: _Optional[str] = ...,
        previously_classified_external: _Optional[bool] = ...,
        ip_asn_matched: _Optional[bool] = ...,
        ix_matched: _Optional[bool] = ...,
        nexthop_matched: _Optional[bool] = ...,
        connectivity_type_matched: _Optional[bool] = ...,
        provider_matched: _Optional[bool] = ...,
        changed_classification: _Optional[bool] = ...,
    ) -> None: ...

class DeviceClassifyInfo(_message.Message):
    __slots__ = (
        "device_id",
        "total_interfaces",
        "previously_classified_counter",
        "auto_classified_counter",
        "changed_classification_count",
        "ip_asn_matched_count",
        "ix_matched_count",
        "nexthop_matched_count",
        "connectivity_type_matched_count",
        "provider_matched_count",
        "interfaces",
    )
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    PREVIOUSLY_CLASSIFIED_COUNTER_FIELD_NUMBER: _ClassVar[int]
    AUTO_CLASSIFIED_COUNTER_FIELD_NUMBER: _ClassVar[int]
    CHANGED_CLASSIFICATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    IP_ASN_MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    IX_MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    NEXTHOP_MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPE_MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    total_interfaces: int
    previously_classified_counter: ClassifyCounter
    auto_classified_counter: ClassifyCounter
    changed_classification_count: int
    ip_asn_matched_count: int
    ix_matched_count: int
    nexthop_matched_count: int
    connectivity_type_matched_count: int
    provider_matched_count: int
    interfaces: _containers.RepeatedCompositeFieldContainer[InterfaceClassifyInfo]
    def __init__(
        self,
        device_id: _Optional[str] = ...,
        total_interfaces: _Optional[int] = ...,
        previously_classified_counter: _Optional[
            _Union[ClassifyCounter, _Mapping]
        ] = ...,
        auto_classified_counter: _Optional[_Union[ClassifyCounter, _Mapping]] = ...,
        changed_classification_count: _Optional[int] = ...,
        ip_asn_matched_count: _Optional[int] = ...,
        ix_matched_count: _Optional[int] = ...,
        nexthop_matched_count: _Optional[int] = ...,
        connectivity_type_matched_count: _Optional[int] = ...,
        provider_matched_count: _Optional[int] = ...,
        interfaces: _Optional[_Iterable[_Union[InterfaceClassifyInfo, _Mapping]]] = ...,
    ) -> None: ...

class InterfaceFilter(_message.Message):
    __slots__ = (
        "text",
        "device_ids",
        "connectivity_types",
        "network_boundaries",
        "providers",
        "snmp_speeds",
        "ip_types",
    )
    TEXT_FIELD_NUMBER: _ClassVar[int]
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPES_FIELD_NUMBER: _ClassVar[int]
    NETWORK_BOUNDARIES_FIELD_NUMBER: _ClassVar[int]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    SNMP_SPEEDS_FIELD_NUMBER: _ClassVar[int]
    IP_TYPES_FIELD_NUMBER: _ClassVar[int]
    text: str
    device_ids: _containers.RepeatedScalarFieldContainer[str]
    connectivity_types: _containers.RepeatedScalarFieldContainer[ConnectivityType]
    network_boundaries: _containers.RepeatedScalarFieldContainer[NetworkBoundary]
    providers: _containers.RepeatedScalarFieldContainer[str]
    snmp_speeds: _containers.RepeatedScalarFieldContainer[int]
    ip_types: _containers.RepeatedScalarFieldContainer[IpFilter]
    def __init__(
        self,
        text: _Optional[str] = ...,
        device_ids: _Optional[_Iterable[str]] = ...,
        connectivity_types: _Optional[_Iterable[_Union[ConnectivityType, str]]] = ...,
        network_boundaries: _Optional[_Iterable[_Union[NetworkBoundary, str]]] = ...,
        providers: _Optional[_Iterable[str]] = ...,
        snmp_speeds: _Optional[_Iterable[int]] = ...,
        ip_types: _Optional[_Iterable[_Union[IpFilter, str]]] = ...,
    ) -> None: ...

class AutoClassifyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AutoClassifyResponse(_message.Message):
    __slots__ = (
        "perc_auto_classified",
        "net_changed_transit",
        "net_changed_ix",
        "net_changed_provider",
        "total_changed_classification_count",
        "total_auto_classify_count",
        "total_auto_classify_counter",
        "total_previous_counter",
        "total_interfaces",
        "devices",
    )
    PERC_AUTO_CLASSIFIED_FIELD_NUMBER: _ClassVar[int]
    NET_CHANGED_TRANSIT_FIELD_NUMBER: _ClassVar[int]
    NET_CHANGED_IX_FIELD_NUMBER: _ClassVar[int]
    NET_CHANGED_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CHANGED_CLASSIFICATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AUTO_CLASSIFY_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AUTO_CLASSIFY_COUNTER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PREVIOUS_COUNTER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    perc_auto_classified: float
    net_changed_transit: int
    net_changed_ix: int
    net_changed_provider: int
    total_changed_classification_count: int
    total_auto_classify_count: int
    total_auto_classify_counter: ClassifyCounter
    total_previous_counter: ClassifyCounter
    total_interfaces: int
    devices: _containers.RepeatedCompositeFieldContainer[DeviceClassifyInfo]
    def __init__(
        self,
        perc_auto_classified: _Optional[float] = ...,
        net_changed_transit: _Optional[int] = ...,
        net_changed_ix: _Optional[int] = ...,
        net_changed_provider: _Optional[int] = ...,
        total_changed_classification_count: _Optional[int] = ...,
        total_auto_classify_count: _Optional[int] = ...,
        total_auto_classify_counter: _Optional[_Union[ClassifyCounter, _Mapping]] = ...,
        total_previous_counter: _Optional[_Union[ClassifyCounter, _Mapping]] = ...,
        total_interfaces: _Optional[int] = ...,
        devices: _Optional[_Iterable[_Union[DeviceClassifyInfo, _Mapping]]] = ...,
    ) -> None: ...

class ManualClassifyRequest(_message.Message):
    __slots__ = ("interface_ids", "connectivity_type", "network_boundary", "provider")
    INTERFACE_IDS_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    interface_ids: _containers.RepeatedScalarFieldContainer[str]
    connectivity_type: ConnectivityType
    network_boundary: NetworkBoundary
    provider: str
    def __init__(
        self,
        interface_ids: _Optional[_Iterable[str]] = ...,
        connectivity_type: _Optional[_Union[ConnectivityType, str]] = ...,
        network_boundary: _Optional[_Union[NetworkBoundary, str]] = ...,
        provider: _Optional[str] = ...,
    ) -> None: ...

class ManualClassifyResponse(_message.Message):
    __slots__ = ("device_ids",)
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    device_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, device_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListInterfaceRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: InterfaceFilter
    def __init__(
        self, filters: _Optional[_Union[InterfaceFilter, _Mapping]] = ...
    ) -> None: ...

class ListInterfaceResponse(_message.Message):
    __slots__ = ("interfaces", "total_count", "invalid_count")
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    interfaces: _containers.RepeatedCompositeFieldContainer[Interface]
    total_count: int
    invalid_count: int
    def __init__(
        self,
        interfaces: _Optional[_Iterable[_Union[Interface, _Mapping]]] = ...,
        total_count: _Optional[int] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetInterfaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetInterfaceResponse(_message.Message):
    __slots__ = ("interface",)
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    def __init__(
        self, interface: _Optional[_Union[Interface, _Mapping]] = ...
    ) -> None: ...

class CreateInterfaceRequest(_message.Message):
    __slots__ = ("interface",)
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    def __init__(
        self, interface: _Optional[_Union[Interface, _Mapping]] = ...
    ) -> None: ...

class CreateInterfaceResponse(_message.Message):
    __slots__ = ("interface",)
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    def __init__(
        self, interface: _Optional[_Union[Interface, _Mapping]] = ...
    ) -> None: ...

class UpdateInterfaceRequest(_message.Message):
    __slots__ = ("interface",)
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    def __init__(
        self, interface: _Optional[_Union[Interface, _Mapping]] = ...
    ) -> None: ...

class UpdateInterfaceResponse(_message.Message):
    __slots__ = ("interface",)
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    def __init__(
        self, interface: _Optional[_Union[Interface, _Mapping]] = ...
    ) -> None: ...

class DeleteInterfaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteInterfaceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Match(_message.Message):
    __slots__ = ("match_attribute", "match_operator", "pattern")
    MATCH_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    MATCH_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    match_attribute: MatchAttribute
    match_operator: Operator
    pattern: str
    def __init__(
        self,
        match_attribute: _Optional[_Union[MatchAttribute, str]] = ...,
        match_operator: _Optional[_Union[Operator, str]] = ...,
        pattern: _Optional[str] = ...,
    ) -> None: ...

class Action(_message.Message):
    __slots__ = (
        "set_connectivity_type",
        "set_network_boundary",
        "set_connected_asns",
        "set_provider",
    )
    SET_CONNECTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SET_NETWORK_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    SET_CONNECTED_ASNS_FIELD_NUMBER: _ClassVar[int]
    SET_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    set_connectivity_type: ConnectivityType
    set_network_boundary: NetworkBoundary
    set_connected_asns: str
    set_provider: str
    def __init__(
        self,
        set_connectivity_type: _Optional[_Union[ConnectivityType, str]] = ...,
        set_network_boundary: _Optional[_Union[NetworkBoundary, str]] = ...,
        set_connected_asns: _Optional[str] = ...,
        set_provider: _Optional[str] = ...,
    ) -> None: ...

class DeviceFilter(_message.Message):
    __slots__ = (
        "all_devices",
        "device_name",
        "device_labels",
        "device_rules",
        "device_types",
    )
    ALL_DEVICES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_LABELS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_RULES_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPES_FIELD_NUMBER: _ClassVar[int]
    all_devices: bool
    device_name: _containers.RepeatedScalarFieldContainer[str]
    device_labels: _containers.RepeatedScalarFieldContainer[str]
    device_rules: _containers.RepeatedScalarFieldContainer[str]
    device_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        all_devices: _Optional[bool] = ...,
        device_name: _Optional[_Iterable[str]] = ...,
        device_labels: _Optional[_Iterable[str]] = ...,
        device_rules: _Optional[_Iterable[str]] = ...,
        device_types: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class Rule(_message.Message):
    __slots__ = (
        "id",
        "enabled",
        "rank",
        "match_clause",
        "action_set",
        "cdate",
        "edate",
        "included_devices",
        "excluded_devices",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    MATCH_CLAUSE_FIELD_NUMBER: _ClassVar[int]
    ACTION_SET_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    INCLUDED_DEVICES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_DEVICES_FIELD_NUMBER: _ClassVar[int]
    id: str
    enabled: bool
    rank: int
    match_clause: Match
    action_set: Action
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    included_devices: DeviceFilter
    excluded_devices: DeviceFilter
    def __init__(
        self,
        id: _Optional[str] = ...,
        enabled: _Optional[bool] = ...,
        rank: _Optional[int] = ...,
        match_clause: _Optional[_Union[Match, _Mapping]] = ...,
        action_set: _Optional[_Union[Action, _Mapping]] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        included_devices: _Optional[_Union[DeviceFilter, _Mapping]] = ...,
        excluded_devices: _Optional[_Union[DeviceFilter, _Mapping]] = ...,
    ) -> None: ...
