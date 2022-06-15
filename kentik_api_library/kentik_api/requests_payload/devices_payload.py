from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.device import (
    AppliedLabels,
    AuthenticationProtocol,
    CDNAttribute,
    Device,
    DeviceBGPType,
    DeviceInterface,
    DeviceSubtype,
    DeviceType,
    PrivacyProtocol,
    SNMPv3Conf,
)
from kentik_api.public.device_label import DeviceLabel
from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.site import Site
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import (
    convert,
    convert_list_or_none,
    convert_or_none,
    dict_from_json,
    from_dict,
    list_from_json,
    permissive_enum_to_str,
)
from kentik_api.requests_payload.plans_payload import GetResponse as PlanGetResponse
from kentik_api.requests_payload.validation import validate_fields

# pylint: disable=too-many-instance-attributes


@dataclass
class SNMPv3ConfPayload:
    """This datastructure represents JSON Device.SNMPv3Conf payload as it is transmitted to and from KentikAPI"""

    UserName: str
    AuthenticationProtocol: Optional[str] = None
    AuthenticationPassphrase: Optional[str] = None
    PrivacyProtocol: Optional[str] = None
    PrivacyPassphrase: Optional[str] = None

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return from_dict(data_class=cls, data=dic)

    @classmethod
    def from_conf(cls, conf: SNMPv3Conf):
        return cls(
            UserName=conf.user_name,
            AuthenticationProtocol=convert_or_none(conf.authentication_protocol, permissive_enum_to_str),
            AuthenticationPassphrase=conf.authentication_passphrase,
            PrivacyProtocol=convert_or_none(conf.privacy_protocol, permissive_enum_to_str),
            PrivacyPassphrase=conf.privacy_passphrase,
        )

    def to_conf(self) -> SNMPv3Conf:
        return SNMPv3Conf(
            user_name=self.UserName,
            authentication_protocol=convert_or_none(self.AuthenticationProtocol, AuthenticationProtocol),
            authentication_passphrase=self.AuthenticationPassphrase,
            privacy_protocol=convert_or_none(self.PrivacyProtocol, PrivacyProtocol),
            privacy_passphrase=self.PrivacyPassphrase,
        )


@dataclass
class LabelPayload:
    """
    This datastructure represents JSON Device.Label payload as it is transmitted to and from KentikAPI
    LabelPayload embedded under Device differs from standalone LabelPayload in that it lacks devices list,
    and in field names, eg. cdate vs created_date, edate vs updated_date
    """

    id: int
    color: str
    name: str
    user_id: Optional[str]  # yes, user_id can be None
    company_id: str
    cdate: str
    edate: str

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return from_dict(data_class=cls, data=dic)

    def to_device_label(self) -> DeviceLabel:
        return DeviceLabel(
            color=self.color,
            name=self.name,
            _id=convert(self.id, ID),
            _user_id=convert_or_none(self.user_id, ID),
            _company_id=convert(self.company_id, ID),
            _created_date=self.cdate,
            _updated_date=self.edate,
            _devices=[],
        )


@dataclass
class SitePayload:
    """
    This datastructure represents JSON Device.Site payload as it is transmitted to and from KentikAPI.
    SitePayload embeddedd under Device differs from regular SitePayload in that all fields are optional.
    """

    id: Optional[int]
    site_name: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    company_id: Optional[int]

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return from_dict(data_class=cls, data=dic)

    def to_site(self) -> Site:
        return Site(
            site_name=self.site_name,
            latitude=self.lat,
            longitude=self.lon,
            id=convert_or_none(self.id, ID),
            company_id=convert_or_none(self.company_id, ID),
        )


PlanPayload = PlanGetResponse  # Plan payload is same as in Plans API


@dataclass
class DeviceInterfacePayload:
    """This datastructure represents JSON Device.AllInterfaces payload as it is transmitted from KentikAPI"""

    device_id: str
    snmp_speed: str
    interface_description: str
    initial_snmp_speed: Optional[str]

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return from_dict(data_class=cls, data=dic)

    def to_device_interface(self) -> DeviceInterface:
        return DeviceInterface(
            device_id=convert(self.device_id, ID),
            snmp_speed=convert(self.snmp_speed, int),
            interface_description=self.interface_description,
            initial_snmp_speed=convert_or_none(self.initial_snmp_speed, int),
        )


@dataclass
class DevicePayload:
    """This datastructure represents JSON Device payload as it is transmitted to and from KentikAPI"""

    device_name: Optional[str] = None
    device_type: Optional[str] = None
    device_subtype: Optional[str] = None
    device_sample_rate: Optional[str] = None
    sending_ips: Optional[List[str]] = None
    id: Optional[str] = None
    plan: Optional[PlanPayload] = None
    site: Optional[SitePayload] = None
    plan_id: Optional[int] = None
    site_id: Optional[int] = None
    labels: Optional[List[LabelPayload]] = None
    all_interfaces: Optional[List[DeviceInterfacePayload]] = None
    cdn_attr: Optional[str] = None
    device_description: Optional[str] = None
    device_snmp_ip: Optional[str] = None
    device_snmp_community: Optional[str] = None
    device_snmp_v3_conf: Optional[SNMPv3ConfPayload] = None
    minimize_snmp: Optional[bool] = None
    device_bgp_type: Optional[str] = None
    device_bgp_neighbor_ip: Optional[str] = None
    device_bgp_neighbor_ip6: Optional[str] = None
    device_bgp_neighbor_asn: Optional[str] = None
    device_bgp_flowspec: Optional[bool] = None
    device_bgp_password: Optional[str] = None
    use_bgp_device_id: Optional[int] = None
    device_status: Optional[str] = None
    device_flow_type: Optional[str] = None
    company_id: Optional[str] = None
    snmp_last_updated: Optional[str] = None
    created_date: Optional[str] = None
    updated_date: Optional[str] = None
    bgpPeerIP4: Optional[str] = None
    bgpPeerIP6: Optional[str] = None

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        required_fields = [
            "id",
            "company_id",
            "device_name",
            "device_type",
            "device_subtype",
            "plan",
            "device_sample_rate",
            "created_date",
            "updated_date",
        ]
        validate_fields(class_name=cls.__name__, required_fields=required_fields, dic=dic)

        # recreate GET/POST/PUT response payload: fill all available fields
        return cls(
            # always returned fields
            id=dic["id"],
            company_id=dic["company_id"],
            device_name=dic["device_name"],
            device_type=dic["device_type"],
            device_subtype=dic["device_subtype"],
            plan=PlanPayload.from_dict(dic["plan"]),
            device_sample_rate=dic["device_sample_rate"],
            created_date=dic["created_date"],
            updated_date=dic["updated_date"],
            # optional fields
            sending_ips=dic.get("sending_ips"),
            site=convert_or_none(dic.get("site"), SitePayload.from_dict),
            labels=convert_list_or_none(dic.get("labels"), LabelPayload.from_dict),
            all_interfaces=convert_list_or_none(dic.get("all_interfaces"), DeviceInterfacePayload.from_dict),
            cdn_attr=dic.get("cdn_attr"),
            device_description=dic.get("device_description"),
            device_snmp_ip=dic.get("device_snmp_ip"),
            device_snmp_community=dic.get("device_snmp_community"),
            device_snmp_v3_conf=convert_or_none(dic.get("device_snmp_v3_conf"), SNMPv3ConfPayload.from_dict),
            minimize_snmp=dic.get("minimize_snmp"),
            device_bgp_type=dic.get("device_bgp_type"),
            device_bgp_neighbor_ip=dic.get("device_bgp_neighbor_ip"),
            device_bgp_neighbor_ip6=dic.get("device_bgp_neighbor_ip6"),
            device_bgp_neighbor_asn=dic.get("device_bgp_neighbor_asn"),
            device_bgp_flowspec=dic.get("device_bgp_flowspec"),
            device_bgp_password=dic.get("device_bgp_password"),
            use_bgp_device_id=dic.get("use_bgp_device_id"),
            device_status=dic.get("device_status"),
            device_flow_type=dic.get("device_flow_type"),
            snmp_last_updated=dic.get("snmp_last_updated"),
            bgpPeerIP4=dic.get("bgpPeerIP4"),
            bgpPeerIP6=dic.get("bgpPeerIP6"),
        )

    @classmethod
    def from_device(cls, device: Device):
        # prepare POST/PUT request payload: fill only the user-provided fields
        return cls(
            plan_id=convert_or_none(device.plan_id, int),
            site_id=convert_or_none(device.site_id, int),
            device_name=device.device_name,
            device_type=convert_or_none(device.device_type, permissive_enum_to_str),
            device_subtype=convert_or_none(device.device_subtype, permissive_enum_to_str),
            device_description=device.device_description,
            device_sample_rate=convert_or_none(device.device_sample_rate, str),
            sending_ips=device.sending_ips,
            device_snmp_ip=device.device_snmp_ip,
            device_snmp_community=device.device_snmp_community,
            minimize_snmp=device.minimize_snmp,
            device_bgp_type=convert_or_none(device.device_bgp_type, permissive_enum_to_str),
            device_bgp_neighbor_ip=device.device_bgp_neighbor_ip,
            device_bgp_neighbor_ip6=device.device_bgp_neighbor_ip6,
            device_bgp_neighbor_asn=device.device_bgp_neighbor_asn,
            device_bgp_flowspec=device.device_bgp_flowspec,
            device_bgp_password=device.device_bgp_password,
            use_bgp_device_id=convert_or_none(device.use_bgp_device_id, int),
            device_snmp_v3_conf=convert_or_none(device.device_snmp_v3_conf, SNMPv3ConfPayload.from_conf),
            cdn_attr=convert_or_none(device.cdn_attr, permissive_enum_to_str),
        )

    def to_device(self) -> Device:
        return Device(
            id=convert_or_none(self.id, ID),
            plan=convert_or_none(self.plan, PlanPayload.to_plan),
            site=convert_or_none(self.site, SitePayload.to_site),
            device_name=self.device_name,
            device_type=DeviceType(self.device_type),
            device_subtype=DeviceSubtype(self.device_subtype),
            device_sample_rate=convert_or_none(self.device_sample_rate, int),
            sending_ips=self.sending_ips,
            device_description=self.device_description,
            device_snmp_ip=self.device_snmp_ip,
            device_snmp_community=self.device_snmp_community,
            minimize_snmp=self.minimize_snmp,
            device_bgp_type=DeviceBGPType(self.device_bgp_type),
            device_bgp_neighbor_ip=self.device_bgp_neighbor_ip,
            device_bgp_neighbor_ip6=self.device_bgp_neighbor_ip6,
            device_bgp_neighbor_asn=self.device_bgp_neighbor_asn,
            device_bgp_flowspec=self.device_bgp_flowspec,
            device_bgp_password=self.device_bgp_password,
            use_bgp_device_id=convert_or_none(self.use_bgp_device_id, ID),
            device_status=self.device_status,
            device_flow_type=self.device_flow_type,
            company_id=convert_or_none(self.company_id, ID),
            snmp_last_updated=self.snmp_last_updated,
            created_date=self.created_date,
            updated_date=self.updated_date,
            bgp_peer_ip4=self.bgpPeerIP4,
            bgp_peer_ip6=self.bgpPeerIP6,
            labels=convert_list_or_none(self.labels, LabelPayload.to_device_label),
            interfaces=convert_list_or_none(self.all_interfaces, DeviceInterfacePayload.to_device_interface),
            device_snmp_v3_conf=convert_or_none(self.device_snmp_v3_conf, SNMPv3ConfPayload.to_conf),
            cdn_attr=convert_or_none(self.cdn_attr, CDNAttribute),
        )


@dataclass
class GetResponse:
    device: DevicePayload

    @classmethod
    def from_json(cls, json_string: str):
        # for GET response the payload json is like: "device": {...}
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string, root="device")
        return cls.from_dict(dic)

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(device=DevicePayload.from_dict(dic))

    def to_device(self) -> Device:
        return self.device.to_device()


@dataclass
class GetAllResponse:
    devices: List[GetResponse]

    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(class_name=cls.__name__, json_string=json_string, root="devices")
        devices = [GetResponse.from_dict(item) for item in items]
        return cls(devices=devices)

    def to_devices(self) -> List[Device]:
        return [item.to_device() for item in self.devices]


@dataclass
class CreateRequest:
    device: DevicePayload  # request device object is provided under key "device"

    @classmethod
    def from_device(cls, device: Device):
        CreateRequest.validate(device)
        return cls(device=DevicePayload.from_device(device))

    @staticmethod
    def validate(device: Device) -> None:
        operation = "Create"
        if device.device_name is None:
            raise IncompleteObjectError(operation, device.__class__.__name__, "device_name is required")
        if device.device_subtype is None:
            raise IncompleteObjectError(operation, device.__class__.__name__, "device_subtype is required")
        if device.device_sample_rate is None:
            raise IncompleteObjectError(operation, device.__class__.__name__, "device_sample_rate is required")

        validate_device_bgp_snmp_conf(device, operation)


@dataclass
class UpdateRequest:
    device: DevicePayload  # request device object is provided under key "device"

    @classmethod
    def from_device(cls, device: Device):
        UpdateRequest.validate(device)
        return cls(device=DevicePayload.from_device(device))

    @staticmethod
    def validate(device: Device) -> None:
        operation = "Update"
        validate_device_bgp_snmp_conf(device, operation)


def validate_device_bgp_snmp_conf(device: Device, operation: str) -> None:
    """Common validations for CreateRequest and UpdateRequest"""
    class_name = device.__class__.__name__
    # device-specific
    if device.device_type == DeviceType.router:
        if device.sending_ips == []:
            raise IncompleteObjectError(operation, class_name, "for device_type=router, sending_ips is required")
        if device.minimize_snmp is None:
            raise IncompleteObjectError(
                operation,
                class_name,
                "for device_type=router, minimize_snmp is required",
            )
    elif device.device_type == DeviceType.host_nprobe_dns_www:
        if device.cdn_attr is None:
            raise IncompleteObjectError(
                operation,
                class_name,
                "for device_type=host_nprobe_dns_www, cdn_attr is required",
            )

    # bgp-specific
    if device.device_bgp_type == DeviceBGPType.device:
        if device.device_bgp_neighbor_asn is None:
            raise IncompleteObjectError(
                operation,
                class_name,
                "for device_bgp_type=device, device_bgp_neighbor_asn is required",
            )
        if device.device_bgp_neighbor_ip is None and device.device_bgp_neighbor_ip6 is None:
            raise IncompleteObjectError(
                operation,
                class_name,
                "for device_bgp_type=device, either device_bgp_neighbor_ip or device_bgp_neighbor_ip6 is required",
            )
    elif device.device_bgp_type == DeviceBGPType.other_device:
        if device.use_bgp_device_id is None:
            raise IncompleteObjectError(
                operation,
                class_name,
                "for device_bgp_type=other_device, use_bgp_device_id is required",
            )

    # snmp-specific
    if device.device_snmp_v3_conf is not None:
        if device.device_snmp_v3_conf.user_name is None:
            raise IncompleteObjectError(
                operation,
                class_name,
                "for specified device_snmp_v3_conf, user_name is required",
            )
        if (
            device.device_snmp_v3_conf.authentication_protocol != AuthenticationProtocol.no_auth
            and device.device_snmp_v3_conf.authentication_passphrase == ""
        ):
            raise IncompleteObjectError(
                operation,
                class_name,
                "for device_snmp_v3_conf.authentication_protocol != no_auth, authentication_passphrase is required",
            )
        if (
            device.device_snmp_v3_conf.privacy_protocol != PrivacyProtocol.no_priv
            and device.device_snmp_v3_conf.privacy_passphrase == ""
        ):
            raise IncompleteObjectError(
                operation,
                class_name,
                "for device_snmp_v3_conf.privacy_protocol != no_priv, privacy_passphrase is required",
            )


CreateResponse = GetResponse

UpdateResponse = GetResponse


@dataclass
class LabelIDPayload:
    """This datastructure represents JSON ApplyLabels.LabelID payload as it is transmitted to KentikAPI"""

    id: int


@dataclass
class ApplyLabelsRequest:
    """This datastructure represents JSON ApplyLabelsRequest payload as it is transmitted to KentikAPI"""

    labels: List[LabelIDPayload]

    @classmethod
    def from_id_list(cls, ids: List[ID]):
        labels = [LabelIDPayload(id=convert(label_id, int)) for label_id in ids]
        return cls(labels=labels)


@dataclass
class ApplyLabelsResponse:
    """This datastructure represents JSON ApplyLabelsResponse payload as it is transmitted from KentikAPI"""

    id: str
    device_name: str
    labels: List[LabelPayload]

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string)
        required_fields = ["id", "device_name", "labels"]
        validate_fields(class_name=cls.__name__, required_fields=required_fields, dic=dic)
        labels = [LabelPayload.from_dict(item) for item in dic["labels"]]
        return cls(
            id=dic["id"],
            device_name=dic["device_name"],
            labels=labels,
        )

    def to_applied_labels(self) -> AppliedLabels:
        labels = [l.to_device_label() for l in self.labels]
        return AppliedLabels(
            id=convert(self.id, ID),
            device_name=self.device_name,
            labels=labels,
        )


# pylint: enable=too-many-instance-attributes
