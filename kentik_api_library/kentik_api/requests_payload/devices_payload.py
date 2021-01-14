import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


from kentik_api.public.device import (
    Device,
    DeviceType,
    DeviceSubtype,
    DeviceBGPType,
    SNMPv3Conf,
    PrivacyProtocol,
    AuthenticationProtocol,
    CDNAttribute,
    AppliedLabels,
)
from kentik_api.public.device_label import DeviceLabel
from kentik_api.requests_payload.sites_payload import GetResponse as SiteGetResponse
from kentik_api.requests_payload.plans_payload import GetResponse as PlanGetResponse

# pylint: disable=too-many-instance-attributes


@dataclass
class _SNMPv3Conf:
    UserName: str
    AuthenticationProtocol: Optional[str] = None
    AuthenticationPassphrase: Optional[str] = None
    PrivacyProtocol: Optional[str] = None
    PrivacyPassphrase: Optional[str] = None

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(**dic)

    @classmethod
    def from_conf(cls, conf: SNMPv3Conf):
        auth_proto = conf.authentication_protocol.value if conf.authentication_protocol is not None else None
        priv_proto = conf.privacy_protocol.value if conf.privacy_protocol is not None else None
        return cls(
            UserName=conf.user_name,
            AuthenticationProtocol=auth_proto,
            AuthenticationPassphrase=conf.authentication_passphrase,
            PrivacyProtocol=priv_proto,
            PrivacyPassphrase=conf.privacy_passphrase,
        )

    def to_conf(self) -> SNMPv3Conf:
        auth_proto = (
            AuthenticationProtocol(self.AuthenticationProtocol) if self.AuthenticationProtocol is not None else None
        )
        priv_proto = PrivacyProtocol(self.PrivacyProtocol) if self.PrivacyProtocol is not None else None
        return SNMPv3Conf(
            user_name=self.UserName,
            authentication_protocol=auth_proto,
            authentication_passphrase=self.AuthenticationPassphrase,
            privacy_protocol=priv_proto,
            privacy_passphrase=self.PrivacyPassphrase,
        )


@dataclass
class _Label:
    label: Dict[str, Any]

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(label=dic)

    def to_label(self) -> DeviceLabel:
        label_dict = self.label

        label = DeviceLabel(
            id=int(label_dict["id"]),
            color=label_dict["color"],
            name=label_dict["name"],
            user_id=label_dict["user_id"],
            company_id=label_dict["company_id"],
            created_date=label_dict["cdate"],
            updated_date=label_dict["edate"],
            devices=None,
        )
        return label


@dataclass()
class GetResponse:
    # reguired fields
    id: int
    plan: PlanGetResponse
    site: SiteGetResponse
    device_name: str
    device_type: str
    device_subtype: str
    device_sample_rate: int
    sending_ips: List[str]
    labels: List[_Label] = field(default_factory=list)
    all_interfaces: List[Any] = field(default_factory=list)
    # optional fields
    cdn_attr: Optional[str] = None
    device_description: Optional[str] = None
    device_snmp_ip: Optional[str] = None
    device_snmp_community: Optional[str] = None
    device_snmp_v3_conf: Optional[_SNMPv3Conf] = None
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
    def from_json(cls, json_string):
        dic = json.loads(json_string)["device"]
        return cls.from_dict(dic)

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        snmp_v3_conf = (
            _SNMPv3Conf.from_dict(dic["device_snmp_v3_conf"]) if attr_provided("device_snmp_v3_conf", dic) else None
        )
        site = SiteGetResponse.from_fields(**dic["site"]) if attr_provided("site", dic) else None
        labels = [_Label.from_dict(d) for d in dic["labels"]]
        return cls(
            id=int(dic["id"]),
            plan=PlanGetResponse.from_dict(dic["plan"]),
            site=site,
            device_name=dic["device_name"],
            device_type=dic["device_type"],
            device_subtype=dic["device_subtype"],
            device_sample_rate=dic["device_sample_rate"],
            sending_ips=dic["sending_ips"],
            labels=labels,
            all_interfaces=dic["all_interfaces"],
            cdn_attr=dic.get("cdn_attr"),
            device_description=dic.get("device_description"),
            device_snmp_ip=dic.get("device_snmp_ip"),
            device_snmp_community=dic.get("device_snmp_community"),
            device_snmp_v3_conf=snmp_v3_conf,
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
            company_id=dic.get("company_id"),
            snmp_last_updated=dic.get("snmp_last_updated"),
            created_date=dic.get("created_date"),
            updated_date=dic.get("updated_date"),
            bgpPeerIP4=dic.get("bgpPeerIP4"),
            bgpPeerIP6=dic.get("bgpPeerIP6"),
        )

    def to_device(self) -> Device:
        snmp_v3_conf = self.device_snmp_v3_conf.to_conf() if self.device_snmp_v3_conf is not None else None
        site = self.site.to_site() if self.site is not None else None
        labels = [l.to_label() for l in self.labels]
        return Device(
            id=self.id,
            plan=self.plan.to_plan(),
            site=site,
            device_name=self.device_name,
            device_type=DeviceType(self.device_type),
            device_subtype=DeviceSubtype(self.device_subtype),
            device_sample_rate=self.device_sample_rate,
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
            use_bgp_device_id=self.use_bgp_device_id,
            device_status=self.device_status,
            device_flow_type=self.device_flow_type,
            company_id=self.company_id,
            snmp_last_updated=self.snmp_last_updated,
            created_date=self.created_date,
            updated_date=self.updated_date,
            bgp_peer_ip4=self.bgpPeerIP4,
            bgp_peer_ip6=self.bgpPeerIP6,
            labels=labels,
            all_interfaces=self.all_interfaces,
            device_snmp_v3_conf=snmp_v3_conf,
            cdn_attr=CDNAttribute(self.cdn_attr) if self.cdn_attr is not None else None,
        )


@dataclass
class GetAllResponse:
    devices: List[GetResponse]

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        devices = list()
        for item in dic["devices"]:
            d = GetResponse.from_dict(item)
            devices.append(d)
        return cls(devices=devices)

    def to_devices(self) -> List[Device]:
        return [d.to_device() for d in self.devices]


@dataclass
class _RequestDevice:
    plan_id: Optional[int] = None
    site_id: Optional[int] = None
    device_name: Optional[str] = None
    device_type: Optional[DeviceType] = None
    device_subtype: Optional[DeviceSubtype] = None
    device_description: Optional[str] = None
    device_sample_rate: Optional[int] = None
    sending_ips: List[str] = field(default_factory=list)
    device_snmp_ip: Optional[str] = None
    device_snmp_community: Optional[str] = None
    minimize_snmp: Optional[bool] = None
    device_bgp_type: Optional[DeviceBGPType] = None
    device_bgp_neighbor_ip: Optional[str] = None
    device_bgp_neighbor_ip6: Optional[str] = None
    device_bgp_neighbor_asn: Optional[str] = None
    device_bgp_flowspec: Optional[bool] = None
    device_bgp_password: Optional[str] = None
    use_bgp_device_id: Optional[int] = None
    device_snmp_v3_conf: Optional[_SNMPv3Conf] = None
    cdn_attr: Optional[CDNAttribute] = None

    @classmethod
    def from_device(cls, device: Device):
        snmp_v3_conf = (
            _SNMPv3Conf.from_conf(device.device_snmp_v3_conf) if device.device_snmp_v3_conf is not None else None
        )
        return cls(
            plan_id=device.plan_id,
            site_id=device.site_id,
            device_name=device.device_name,
            device_type=device.device_type,
            device_subtype=device.device_subtype,
            device_description=device.device_description,
            device_sample_rate=device.device_sample_rate,
            sending_ips=device.sending_ips,
            device_snmp_ip=device.device_snmp_ip,
            device_snmp_community=device.device_snmp_community,
            minimize_snmp=device.minimize_snmp,
            device_bgp_type=device.device_bgp_type,
            device_bgp_neighbor_ip=device.device_bgp_neighbor_ip,
            device_bgp_neighbor_ip6=device.device_bgp_neighbor_ip6,
            device_bgp_neighbor_asn=device.device_bgp_neighbor_asn,
            device_bgp_flowspec=device.device_bgp_flowspec,
            device_bgp_password=device.device_bgp_password,
            use_bgp_device_id=device.use_bgp_device_id,
            device_snmp_v3_conf=snmp_v3_conf,
            cdn_attr=device.cdn_attr,
        )


@dataclass
class CreateRequest:
    device: _RequestDevice  # request device object is provided under key "device"

    @classmethod
    def from_device(cls, device: Device):
        return cls(device=_RequestDevice.from_device(device))


CreateResponse = GetResponse

UpdateRequest = CreateRequest
UpdateResponse = GetResponse


@dataclass
class LabelID:
    id: int


@dataclass
class ApplyLabelsRequest:
    labels: List[LabelID]

    @classmethod
    def from_id_list(cls, ids: List[int]):
        labels = [LabelID(id=label_id) for label_id in ids]
        return cls(labels=labels)


@dataclass
class ApplyLabelsResponse:
    id: str
    device_name: str
    labels: List[_Label]

    @classmethod
    def from_json(cls, json_string: str):
        dic = json.loads(json_string)
        labels = [_Label.from_dict(d) for d in dic["labels"]]
        return cls(id=dic["id"], device_name=dic["device_name"], labels=labels)

    def to_applied_labels(self) -> AppliedLabels:
        labels = [l.to_label() for l in self.labels]
        return AppliedLabels(id=self.id, device_name=self.device_name, labels=labels)


# pylint: enable=too-many-instance-attributes


def attr_provided(attr: str, dic: Dict[str, Any]) -> bool:
    return attr in dic and dic[attr] is not None and dic[attr] != {}
