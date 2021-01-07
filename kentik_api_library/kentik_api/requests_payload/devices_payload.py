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
)
from kentik_api.public.device_label import DeviceLabel
from kentik_api.requests_payload.sites_payload import GetResponse as SiteGetResponse
from kentik_api.requests_payload.plans_payload import GetResponse as PlanGetResponse

# pylint: disable=too-many-instance-attributes


@dataclass
class SNMPv3ConfGetResponse:
    conf: Dict[str, Any]

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(conf=dic)

    def to_conf(self) -> SNMPv3Conf:
        conf_dict = self.conf

        auth_proto = (
            AuthenticationProtocol(conf_dict["AuthenticationProtocol"])
            if attr_provided("AuthenticationProtocol", conf_dict)
            else None
        )
        auth_pass = conf_dict.get("AuthenticationPassphrase")

        priv_proto = (
            PrivacyProtocol(conf_dict["PrivacyProtocol"]) if attr_provided("PrivacyProtocol", conf_dict) else None
        )
        priv_pass = conf_dict.get("PrivacyPassphrase")

        return SNMPv3Conf(
            user_name=conf_dict["UserName"],
            authentication_protocol=auth_proto,
            authentication_passphrase=auth_pass,
            privacy_protocol=priv_proto,
            privacy_passphrase=priv_pass,
        )


@dataclass
class LabelGetResponse:
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
    labels: List[LabelGetResponse] = field(default_factory=list)
    all_interfaces: List[Any] = field(default_factory=list)
    # optional fields
    cdn_attr: Optional[str] = None
    device_description: Optional[str] = None
    device_snmp_ip: Optional[str] = None
    device_snmp_community: Optional[str] = None
    device_snmp_v3_conf: Optional[SNMPv3ConfGetResponse] = None
    minimize_snmp: Optional[bool] = None
    device_bgp_type: Optional[str] = None
    device_bgp_neighbor_ip: Optional[str] = None
    device_bgp_neighbor_ip6: Optional[str] = None
    device_bgp_neighbor_asn: Optional[int] = None
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
        snmp_v3_conf = (
            SNMPv3ConfGetResponse.from_dict(dic["device_snmp_v3_conf"])
            if attr_provided("device_snmp_v3_conf", dic)
            else None
        )
        site = SiteGetResponse.from_fields(**dic["site"]) if attr_provided("site", dic) else None
        labels = [LabelGetResponse.from_dict(d) for d in dic["labels"]]
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


# pylint: enable=too-many-instance-attributes


def attr_provided(attr: str, dic: Dict[str, Any]) -> bool:
    return attr in dic and dic[attr] is not None and dic[attr] != {}
