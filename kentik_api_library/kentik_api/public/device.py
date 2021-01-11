from typing import Optional, List, Any
from enum import Enum
from dataclasses import dataclass

from kentik_api.public.site import Site
from kentik_api.public.plan import Plan

from kentik_api.public.device_label import DeviceLabel


class DeviceType(Enum):
    router = "router"
    host_nprobe_dns_www = "host-nprobe-dns-www"


class DeviceSubtype(Enum):
    # for DeviceType = router
    router = "router"
    cisco_asa = "cisco_asa"
    paloalto = "paloalto"
    silverpeak = "silverpeak"

    # for DeviceType = host_nprobe_dns_www
    aws_subnet = "aws_subnet"
    azure_subnet = "azure_subnet"
    gcp_subnet = "gcp_subnet"


class DeviceBGPType(Enum):
    none = "none"
    device = "device"
    other_device = "other_device"


class CDNAttribute(Enum):
    none = "None"
    yes = "Y"
    no = "N"


class AuthenticationProtocol(Enum):
    no_auth = "NoAuth"
    md5 = "MD5"
    sha = "SHA"


class PrivacyProtocol(Enum):
    no_priv = "NoPriv"
    des = "DES"
    aes = "AES"


@dataclass
class SNMPv3Conf:
    user_name: str
    authentication_protocol: Optional[AuthenticationProtocol] = None
    authentication_passphrase: Optional[str] = None
    privacy_protocol: Optional[PrivacyProtocol] = None
    privacy_passphrase: Optional[str] = None

    @classmethod
    def new(cls, user_name: str):
        return cls(user_name=user_name)

    def with_authentication(self, protocol: AuthenticationProtocol, passphrase: str):
        self.authentication_protocol = protocol
        self.authentication_passphrase = passphrase
        return self

    def with_privacy(self, protocol: PrivacyProtocol, passphrase: str):
        self.privacy_protocol = protocol
        self.privacy_passphrase = passphrase
        return self


class Device:
    def __init__(
        self,
        # user-provided when updating device, server-provided when creating device
        id: Optional[int] = None,
        # user-provided
        plan_id: Optional[int] = None,
        site_id: Optional[int] = None,
        device_name: Optional[str] = None,
        device_type: Optional[DeviceType] = None,
        device_subtype: Optional[DeviceSubtype] = None,
        device_description: Optional[str] = None,
        device_sample_rate: Optional[int] = None,
        sending_ips: List[str] = [],
        device_snmp_ip: Optional[str] = None,
        device_snmp_community: Optional[str] = None,
        minimize_snmp: Optional[bool] = None,
        device_bgp_type: Optional[DeviceBGPType] = None,
        device_bgp_neighbor_ip: Optional[str] = None,
        device_bgp_neighbor_ip6: Optional[str] = None,
        device_bgp_neighbor_asn: Optional[str] = None,
        device_bgp_flowspec: Optional[bool] = None,
        device_bgp_password: Optional[str] = None,
        use_bgp_device_id: Optional[int] = None,
        device_snmp_v3_conf: Optional[SNMPv3Conf] = None,
        cdn_attr: Optional[CDNAttribute] = None,
        # server-provided
        device_status: Optional[str] = None,
        device_flow_type: Optional[str] = None,
        company_id: Optional[str] = None,
        snmp_last_updated: Optional[str] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        bgp_peer_ip4: Optional[str] = None,
        bgp_peer_ip6: Optional[str] = None,
        plan: Optional[Plan] = None,
        site: Optional[Site] = None,
        labels: List[DeviceLabel] = [],
        all_interfaces: List[Any] = [],
    ) -> None:
        """Note: plan_id and site_id is being sent to API, plan and site gets returned"""

        # read-write properties (can be updated in update call)
        self.plan_id = plan_id
        self.site_id = site_id
        self.device_description = device_description
        self.device_sample_rate = device_sample_rate
        self.sending_ips = sending_ips
        self.device_snmp_ip = device_snmp_ip
        self.device_snmp_community = device_snmp_community
        self.minimize_snmp = minimize_snmp
        self.device_bgp_type = device_bgp_type
        self.device_bgp_neighbor_ip = device_bgp_neighbor_ip
        self.device_bgp_neighbor_ip6 = device_bgp_neighbor_ip6
        self.device_bgp_neighbor_asn = device_bgp_neighbor_asn
        self.device_bgp_flowspec = device_bgp_flowspec
        self.device_bgp_password = device_bgp_password
        self.use_bgp_device_id = use_bgp_device_id
        self.device_snmp_v3_conf = device_snmp_v3_conf
        self.cdn_attr = cdn_attr
        # read-only properties (can't be updated in update call)
        self._id = id
        self._device_name = device_name
        self._device_type = device_type
        self._device_subtype = device_subtype
        self._device_status = device_status
        self._device_flow_type = device_flow_type
        self._company_id = company_id
        self._snmp_last_updated = snmp_last_updated
        self._created_date = created_date
        self._updated_date = updated_date
        self._bgp_peer_ip4 = bgp_peer_ip4
        self._bgp_peer_ip6 = bgp_peer_ip6
        self._plan = plan
        self._site = site
        self._labels = labels
        self._all_interfaces = all_interfaces

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

    @property
    def device_name(self) -> Optional[str]:
        return self._device_name

    @property
    def device_type(self) -> Optional[DeviceType]:
        return self._device_type

    @property
    def device_subtype(self) -> Optional[DeviceSubtype]:
        return self._device_subtype

    @property
    def device_status(self) -> Optional[str]:
        return self._device_status

    @property
    def device_flow_type(self) -> Optional[str]:
        return self._device_flow_type

    @property
    def company_id(self) -> Optional[str]:
        return self._company_id

    @property
    def snmp_last_updated(self) -> Optional[str]:
        return self._snmp_last_updated

    @property
    def created_date(self) -> Optional[str]:
        return self._created_date

    @property
    def updated_date(self) -> Optional[str]:
        return self._updated_date

    @property
    def bgp_peer_ip4(self) -> Optional[str]:
        return self._bgp_peer_ip4

    @property
    def bgp_peer_ip6(self) -> Optional[str]:
        return self._bgp_peer_ip6

    @property
    def site(self) -> Optional[Site]:
        return self._site

    @property
    def plan(self) -> Plan:
        assert self._plan is not None
        return self._plan

    @property
    def labels(self) -> List[DeviceLabel]:
        return list(self._labels)

    @property
    def all_interfaces(self) -> List[Any]:
        return self._all_interfaces

    @classmethod
    def new_router(
        cls,
        # common required
        device_name: str,
        device_subtype: DeviceSubtype,
        device_sample_rate: int,
        plan_id: int,
        # router required
        sending_ips: List[str],
        minimize_snmp: bool,
        # router optional
        device_snmp_ip: Optional[str] = None,
        device_snmp_community: Optional[str] = None,
        device_snmp_v3_conf: Optional[SNMPv3Conf] = None,  # when set, overwrites "device_snmp_community"
        # common optional
        device_description: Optional[str] = None,
        site_id: Optional[int] = None,
        device_bgp_flowspec: Optional[bool] = None,
    ):
        return cls(
            device_type=DeviceType.router,
            device_name=device_name,
            device_subtype=device_subtype,
            device_sample_rate=device_sample_rate,
            plan_id=plan_id,
            sending_ips=sending_ips,
            minimize_snmp=minimize_snmp,
            device_snmp_ip=device_snmp_ip,
            device_snmp_community=device_snmp_community,
            device_snmp_v3_conf=device_snmp_v3_conf,
            device_description=device_description,
            site_id=site_id,
            device_bgp_flowspec=device_bgp_flowspec,
            device_bgp_type=DeviceBGPType.none,
        )

    @classmethod
    def new_dns(
        cls,
        # common required
        device_name: str,
        device_subtype: DeviceSubtype,
        device_sample_rate: int,
        plan_id: int,
        # dns required
        cdn_attr: CDNAttribute,
        # common optional
        device_description: Optional[str] = None,
        site_id: Optional[int] = None,
        device_bgp_flowspec: Optional[bool] = None,
    ):
        return cls(
            device_type=DeviceType.host_nprobe_dns_www,
            device_name=device_name,
            device_subtype=device_subtype,
            device_sample_rate=device_sample_rate,
            plan_id=plan_id,
            cdn_attr=cdn_attr,
            device_description=device_description,
            site_id=site_id,
            device_bgp_flowspec=device_bgp_flowspec,
            device_bgp_type=DeviceBGPType.none,
        )

    def with_bgp_type_device(
        self,
        device_bgp_neighbor_asn: str,
        device_bgp_neighbor_ip: Optional[str] = None,
        device_bgp_neighbor_ip6: Optional[str] = None,
        device_bgp_password: Optional[str] = None,
    ):
        """
        This is alternative to with_bgp_type_other_device.
        Note: either device_bgp_neighbor_ip or device_bgp_neighbor_ip6 is required.
        """
        self.device_bgp_type = DeviceBGPType.device
        self.device_bgp_neighbor_ip = device_bgp_neighbor_ip
        self.device_bgp_neighbor_ip6 = device_bgp_neighbor_ip6
        self.device_bgp_password = device_bgp_password
        self.device_bgp_neighbor_asn = device_bgp_neighbor_asn
        return self

    def with_bgp_type_other_device(self, use_bgp_device_id: int):
        """ This is alternative to with_bgp_type_device. """
        self.device_bgp_type = DeviceBGPType.other_device
        self.use_bgp_device_id = use_bgp_device_id
        return self


class AppliedLabels:
    def __init__(self, id: str, device_name: str, labels: List[DeviceLabel]):
        # read-only
        self._id = id
        self._device_name = device_name
        self._labels = labels

    @property
    def id(self) -> str:
        return self._id

    @property
    def device_name(self) -> str:
        return self._device_name

    @property
    def labels(self) -> List[DeviceLabel]:
        return self._labels