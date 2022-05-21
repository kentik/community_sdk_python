from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from kentik_api.public.device_label import DeviceLabel
from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.plan import Plan
from kentik_api.public.site import Site
from kentik_api.public.types import ID, PermissiveEnumMeta


class DeviceType(Enum, metaclass=PermissiveEnumMeta):
    router = "router"
    host_nprobe_dns_www = "host-nprobe-dns-www"


class DeviceSubtype(Enum, metaclass=PermissiveEnumMeta):
    # for DeviceType = router
    router = "router"
    cisco_asa = "cisco_asa"
    paloalto = "paloalto"
    silverpeak = "silverpeak"
    mpls = "mpls"
    viptela = "viptela"
    pfe_syslog = "pfe_syslog"
    syslog = "syslog"
    meraki = "meraki"
    istio = "istio"
    ios_xr = "ios_xr"
    cisco_zone_based_firewall = "cisco_zone_based_firewall"
    cisco_nbar = "cisco_nbar"
    cisco_asa_syslog = "cisco_asa_syslog"
    advanced_sflow = "advanced_sflow"
    a10_cgn = "a10_cgn"

    # for DeviceType = host_nprobe_dns_www
    kprobe = "kprobe"
    nprobe = "nprobe"
    aws_subnet = "aws_subnet"
    azure_subnet = "azure_subnet"
    gcp_subnet = "gcp_subnet"
    kappa = "kappa"  # not in api documentation
    ibm_subnet = "ibm_subnet"  # not in api documentation


class DeviceBGPType(Enum, metaclass=PermissiveEnumMeta):
    none = "none"
    device = "device"
    other_device = "other_device"


class CDNAttribute(Enum, metaclass=PermissiveEnumMeta):
    none = "None"
    yes = "Y"
    no = "N"


class AuthenticationProtocol(Enum, metaclass=PermissiveEnumMeta):
    no_auth = "NoAuth"
    md5 = "MD5"
    sha = "SHA"


class PrivacyProtocol(Enum, metaclass=PermissiveEnumMeta):
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


class DeviceInterface:
    def __init__(
        self,
        interface_description: str,
        device_id: ID,
        snmp_speed: float,
        initial_snmp_speed: Optional[float] = None,
    ) -> None:
        # read-only
        self._interface_description = interface_description
        self._device_id = device_id
        self._snmp_speed = snmp_speed
        self._initial_snmp_speed = initial_snmp_speed

    def __repr__(self):
        return f"{self.name} (owner: {self.device_id})"

    @property
    def interface_description(self) -> str:
        return self._interface_description

    @property
    def device_id(self) -> ID:
        return self._device_id

    @property
    def snmp_speed(self) -> float:
        return self._snmp_speed

    @property
    def initial_snmp_speed(self) -> Optional[float]:
        return self._initial_snmp_speed

    @property
    def name(self):
        return self._interface_description

    @property
    def speed(self):
        """
        Return effective speed of the interface in bit/s
        :return: interface speed or NaN (if interface speed is not available)
        """
        if self.snmp_speed is None:
            speed = self.initial_snmp_speed
        else:
            speed = self.snmp_speed
        if speed is None:
            return float("NaN")
        return float(speed) * 1e6  # SNMP speed is in Mbits/s, we want bits/s


class Device:
    def __init__(
        self,
        # user-provided when updating device, server-provided when creating device
        id: Optional[ID] = None,
        # user-provided
        plan_id: Optional[ID] = None,
        site_id: Optional[ID] = None,
        device_name: Optional[str] = None,
        device_type: Optional[DeviceType] = None,
        device_subtype: Optional[DeviceSubtype] = None,
        device_description: Optional[str] = None,
        device_sample_rate: Optional[int] = None,
        sending_ips: Optional[List[str]] = None,
        device_snmp_ip: Optional[str] = None,
        device_snmp_community: Optional[str] = None,
        minimize_snmp: Optional[bool] = None,
        device_bgp_type: Optional[DeviceBGPType] = None,
        device_bgp_neighbor_ip: Optional[str] = None,
        device_bgp_neighbor_ip6: Optional[str] = None,
        device_bgp_neighbor_asn: Optional[str] = None,
        device_bgp_flowspec: Optional[bool] = None,
        device_bgp_password: Optional[str] = None,
        use_bgp_device_id: Optional[ID] = None,
        device_snmp_v3_conf: Optional[SNMPv3Conf] = None,
        cdn_attr: Optional[CDNAttribute] = None,
        # server-provided
        device_status: Optional[str] = None,
        device_flow_type: Optional[str] = None,
        company_id: Optional[ID] = None,
        snmp_last_updated: Optional[str] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        bgp_peer_ip4: Optional[str] = None,
        bgp_peer_ip6: Optional[str] = None,
        plan: Optional[Plan] = None,
        site: Optional[Site] = None,
        labels: Optional[List[DeviceLabel]] = None,
        interfaces: Optional[List[DeviceInterface]] = None,
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
        self._interfaces = interfaces
        self._interfaces_by_name: Dict[str, DeviceInterface] = {}
        if self._interfaces:
            self._interfaces_by_name = {i.name: i for i in self._interfaces}

    def __repr__(self):
        return f"{self.device_name} (id: {self.id} type: {self.device_type.value})"

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_id is required")
        return self._id

    @property
    def device_name(self) -> str:
        if self._device_name:
            return self._device_name
        else:
            return f"<id: {self.id}>"

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
    def company_id(self) -> Optional[ID]:
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
        if self._plan is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_plan is required")
        return self._plan

    @property
    def labels(self) -> List[DeviceLabel]:
        return list(self._labels) if self._labels is not None else []

    @property
    def interfaces(self) -> List[DeviceInterface]:
        return list(self._interfaces) if self._interfaces is not None else []

    def get_interface(self, name):
        return self._interfaces_by_name.get(name)

    def has_label(self, label: str):
        return label in [lbl.name for lbl in self.labels]

    @classmethod
    def new_router(
        cls,
        # common required
        device_name: str,
        device_subtype: DeviceSubtype,
        device_sample_rate: int,
        plan_id: ID,
        # router required
        sending_ips: List[str],
        minimize_snmp: bool,
        # router optional
        device_snmp_ip: Optional[str] = None,
        device_snmp_community: Optional[str] = None,
        device_snmp_v3_conf: Optional[SNMPv3Conf] = None,  # when set, overwrites "device_snmp_community"
        # common optional
        device_description: Optional[str] = None,
        site_id: Optional[ID] = None,
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
        plan_id: ID,
        # dns required
        cdn_attr: CDNAttribute,
        # common optional
        device_description: Optional[str] = None,
        site_id: Optional[ID] = None,
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

    def with_bgp_type_other_device(self, use_bgp_device_id: ID):
        """This is alternative to with_bgp_type_device."""
        self.device_bgp_type = DeviceBGPType.other_device
        self.use_bgp_device_id = use_bgp_device_id
        return self


class AppliedLabels:
    def __init__(self, id: ID, device_name: str, labels: List[DeviceLabel]):
        # read-only
        self._id = id
        self._device_name = device_name
        self._labels = labels

    @property
    def id(self) -> ID:
        return self._id

    @property
    def device_name(self) -> str:
        return self._device_name

    @property
    def labels(self) -> List[DeviceLabel]:
        return list(self._labels)


class VRFAttributes:
    def __init__(
        self,
        # user-provided
        name: str,
        route_target: str,
        route_distinguisher: str,
        description: Optional[str] = None,
        ext_route_distinguisher: Optional[int] = None,
        # sever-provided
        id: Optional[ID] = None,
        company_id: Optional[ID] = None,
        device_id: Optional[ID] = None,
    ):
        # read-write properties (can be updated in update call)
        self.name = name
        self.description = description
        self.route_target = route_target
        self.route_distinguisher = route_distinguisher
        self.ext_route_distinguisher = ext_route_distinguisher

        # read-only properties (can't be updated in update call)
        self._id = id
        self._company_id = company_id
        self._device_id = device_id

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_id is required")
        return self._id

    @property
    def company_id(self) -> Optional[ID]:
        return self._company_id

    @property
    def device_id(self) -> Optional[ID]:
        return self._device_id


@dataclass
class SecondaryIP:
    address: str
    netmask: str


@dataclass
class TopNextHopASN:
    asn: int
    packets: int


class Interface:
    def __init__(
        self,
        # user-provided when updating interface, server-provided when creating interface
        id: Optional[ID] = None,
        # user-provided
        snmp_id: Optional[ID] = None,
        snmp_speed: Optional[int] = None,
        snmp_alias: Optional[str] = None,
        interface_ip: Optional[str] = None,
        interface_ip_netmask: Optional[str] = None,
        interface_description: Optional[str] = None,
        vrf_id: Optional[ID] = None,
        vrf: Optional[VRFAttributes] = None,
        secondary_ips: Optional[List[SecondaryIP]] = None,
        # sever-provided
        company_id: Optional[ID] = None,
        device_id: Optional[ID] = None,
        created_date: Optional[str] = None,
        updated_date: Optional[str] = None,
        initial_snmp_id: Optional[ID] = None,
        initial_snmp_alias: Optional[str] = None,
        initial_interface_description: Optional[str] = None,
        initial_snmp_speed: Optional[int] = None,
        provider: Any = None,
        top_nexthop_asns: Optional[List[TopNextHopASN]] = None,
    ):
        # read-write properties (can be updated in update call)
        self.snmp_id = snmp_id
        self.snmp_speed = snmp_speed
        self.snmp_alias = snmp_alias
        self.interface_ip = interface_ip
        self.interface_ip_netmask = interface_ip_netmask
        self.interface_description = interface_description
        self.vrf_id = vrf_id
        self.vrf = vrf
        self.secondary_ips = secondary_ips

        # read-only properties (can't be updated in update call)
        self._id = id
        self._company_id = company_id
        self._device_id = device_id
        self._created_date = created_date
        self._updated_date = updated_date
        self._initial_snmp_id = initial_snmp_id
        self._initial_snmp_alias = initial_snmp_alias
        self._initial_interface_description = initial_interface_description
        self._initial_snmp_speed = initial_snmp_speed
        self._provider = provider
        self._top_nexthop_asns = top_nexthop_asns

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_id is required")
        return self._id

    @property
    def company_id(self) -> Optional[ID]:
        return self._company_id

    @property
    def device_id(self) -> ID:
        if self._device_id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_device_id is required")
        return self._device_id

    @property
    def created_date(self) -> Optional[str]:
        return self._created_date

    @property
    def updated_date(self) -> Optional[str]:
        return self._updated_date

    @property
    def initial_snmp_id(self) -> Optional[ID]:
        return self._initial_snmp_id

    @property
    def initial_snmp_alias(self) -> Optional[str]:
        return self._initial_snmp_alias

    @property
    def initial_interface_description(self) -> Optional[str]:
        return self._initial_interface_description

    @property
    def initial_snmp_speed(self) -> Optional[float]:
        return self._initial_snmp_speed

    @property
    def provider(self) -> Any:
        return self._provider

    @property
    def top_nexthop_asns(self) -> List[TopNextHopASN]:
        return list(self._top_nexthop_asns) if self._top_nexthop_asns is not None else []
