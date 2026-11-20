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

class DeviceSubtype(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEVICE_SUBTYPE_UNSPECIFIED: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_A10_CGN: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_ADVANCED_SFLOW: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_AWS_SUBNET: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_AZURE_SUBNET: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_CISCO_ASA: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_CISCO_ASA_SYSLOG: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_CISCO_NBAR: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_CISCO_NVZFLOW: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_CISCO_SDWAN_XE: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_CISCO_ZONE_BASED_FIREWALL: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_DARKNET: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_FORTINET_FORTIGATE: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_GCP_CLOUD_RUN: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_GCP_SUBNET: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_GIGAMON: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_IBM_SUBNET: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_IOS_XR: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_ISTIO: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_JUNIPER_DDOS: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_KAGENT: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_KAPPA: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_KMETRICS: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_KPROBE: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_KROBE_TAP: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_KPROXY: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_MERAKI: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_MPLS: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_NOKIALAYER2: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_NPROBE: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_OCI_FLOW_LOG: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_OCI_SUBNET: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_OPEN_NMS: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_PALOALTO: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_PALOALTO_PRISMASDWAN: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_PFE_SYSLOG: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_ROUTER: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_SFLOW_TUNNEL: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_SILVERPEAK: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_SYSLOG: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_VERSA: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_VIPTELA: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_VMWARE_VELOCLOUD: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_VMWARE_VSPHERE: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_VXLAN: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_KSYNTH: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_SDM_LEADER: _ClassVar[DeviceSubtype]
    DEVICE_SUBTYPE_HOST_NPROBE_DNS_WWW: _ClassVar[DeviceSubtype]

DEVICE_SUBTYPE_UNSPECIFIED: DeviceSubtype
DEVICE_SUBTYPE_A10_CGN: DeviceSubtype
DEVICE_SUBTYPE_ADVANCED_SFLOW: DeviceSubtype
DEVICE_SUBTYPE_AWS_SUBNET: DeviceSubtype
DEVICE_SUBTYPE_AZURE_SUBNET: DeviceSubtype
DEVICE_SUBTYPE_CISCO_ASA: DeviceSubtype
DEVICE_SUBTYPE_CISCO_ASA_SYSLOG: DeviceSubtype
DEVICE_SUBTYPE_CISCO_NBAR: DeviceSubtype
DEVICE_SUBTYPE_CISCO_NVZFLOW: DeviceSubtype
DEVICE_SUBTYPE_CISCO_SDWAN_XE: DeviceSubtype
DEVICE_SUBTYPE_CISCO_ZONE_BASED_FIREWALL: DeviceSubtype
DEVICE_SUBTYPE_DARKNET: DeviceSubtype
DEVICE_SUBTYPE_FORTINET_FORTIGATE: DeviceSubtype
DEVICE_SUBTYPE_GCP_CLOUD_RUN: DeviceSubtype
DEVICE_SUBTYPE_GCP_SUBNET: DeviceSubtype
DEVICE_SUBTYPE_GIGAMON: DeviceSubtype
DEVICE_SUBTYPE_IBM_SUBNET: DeviceSubtype
DEVICE_SUBTYPE_IOS_XR: DeviceSubtype
DEVICE_SUBTYPE_ISTIO: DeviceSubtype
DEVICE_SUBTYPE_JUNIPER_DDOS: DeviceSubtype
DEVICE_SUBTYPE_KAGENT: DeviceSubtype
DEVICE_SUBTYPE_KAPPA: DeviceSubtype
DEVICE_SUBTYPE_KMETRICS: DeviceSubtype
DEVICE_SUBTYPE_KPROBE: DeviceSubtype
DEVICE_SUBTYPE_KROBE_TAP: DeviceSubtype
DEVICE_SUBTYPE_KPROXY: DeviceSubtype
DEVICE_SUBTYPE_MERAKI: DeviceSubtype
DEVICE_SUBTYPE_MPLS: DeviceSubtype
DEVICE_SUBTYPE_NOKIALAYER2: DeviceSubtype
DEVICE_SUBTYPE_NPROBE: DeviceSubtype
DEVICE_SUBTYPE_OCI_FLOW_LOG: DeviceSubtype
DEVICE_SUBTYPE_OCI_SUBNET: DeviceSubtype
DEVICE_SUBTYPE_OPEN_NMS: DeviceSubtype
DEVICE_SUBTYPE_PALOALTO: DeviceSubtype
DEVICE_SUBTYPE_PALOALTO_PRISMASDWAN: DeviceSubtype
DEVICE_SUBTYPE_PFE_SYSLOG: DeviceSubtype
DEVICE_SUBTYPE_ROUTER: DeviceSubtype
DEVICE_SUBTYPE_SFLOW_TUNNEL: DeviceSubtype
DEVICE_SUBTYPE_SILVERPEAK: DeviceSubtype
DEVICE_SUBTYPE_SYSLOG: DeviceSubtype
DEVICE_SUBTYPE_VERSA: DeviceSubtype
DEVICE_SUBTYPE_VIPTELA: DeviceSubtype
DEVICE_SUBTYPE_VMWARE_VELOCLOUD: DeviceSubtype
DEVICE_SUBTYPE_VMWARE_VSPHERE: DeviceSubtype
DEVICE_SUBTYPE_VXLAN: DeviceSubtype
DEVICE_SUBTYPE_KSYNTH: DeviceSubtype
DEVICE_SUBTYPE_SDM_LEADER: DeviceSubtype
DEVICE_SUBTYPE_HOST_NPROBE_DNS_WWW: DeviceSubtype

class PlanDevice(_message.Message):
    __slots__ = ("id", "device_name", "device_subtype", "device_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_SUBTYPE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    device_name: str
    device_subtype: DeviceSubtype
    device_type: DeviceSubtype
    def __init__(
        self,
        id: _Optional[str] = ...,
        device_name: _Optional[str] = ...,
        device_subtype: _Optional[_Union[DeviceSubtype, str]] = ...,
        device_type: _Optional[_Union[DeviceSubtype, str]] = ...,
    ) -> None: ...

class Plan(_message.Message):
    __slots__ = (
        "id",
        "company_id",
        "name",
        "description",
        "active",
        "max_devices",
        "max_fps",
        "bgp_enabled",
        "fast_retention",
        "full_retention",
        "created_date",
        "updated_date",
        "max_bigdata_fps",
        "device_types",
        "devices",
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
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MAX_DEVICES_FIELD_NUMBER: _ClassVar[int]
    MAX_FPS_FIELD_NUMBER: _ClassVar[int]
    BGP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    FAST_RETENTION_FIELD_NUMBER: _ClassVar[int]
    FULL_RETENTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    MAX_BIGDATA_FPS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPES_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    company_id: str
    name: str
    description: str
    active: bool
    max_devices: int
    max_fps: int
    bgp_enabled: bool
    fast_retention: int
    full_retention: int
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    max_bigdata_fps: int
    device_types: _containers.RepeatedScalarFieldContainer[DeviceSubtype]
    devices: _containers.RepeatedCompositeFieldContainer[PlanDevice]
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        company_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        active: _Optional[bool] = ...,
        max_devices: _Optional[int] = ...,
        max_fps: _Optional[int] = ...,
        bgp_enabled: _Optional[bool] = ...,
        fast_retention: _Optional[int] = ...,
        full_retention: _Optional[int] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        max_bigdata_fps: _Optional[int] = ...,
        device_types: _Optional[_Iterable[_Union[DeviceSubtype, str]]] = ...,
        devices: _Optional[_Iterable[_Union[PlanDevice, _Mapping]]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...
