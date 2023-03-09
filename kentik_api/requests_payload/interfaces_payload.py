from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from kentik_api.public.device import Interface, SecondaryIP, TopNextHopASN, VRFAttributes
from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.types import ID
from kentik_api.requests_payload.conversions import (
    convert,
    convert_list_or_none,
    convert_or_none,
    dict_from_json,
    from_dict,
    list_from_json,
)
from kentik_api.requests_payload.validation import validate_fields


@dataclass
class SecondaryIPPayload:
    """This datastructure represents JSON Interface.SecondaryIP payload as it is transmitted to and from KentikAPI"""

    # GET, POST, PUT request/response
    address: str
    netmask: str

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return from_dict(data_class=cls, data=dic)

    @classmethod
    def from_secondary_ip(cls, ip: SecondaryIP):
        return cls(address=ip.address, netmask=ip.netmask)

    def to_secondary_ip(self) -> SecondaryIP:
        return SecondaryIP(address=self.address, netmask=self.netmask)


@dataclass
class TopNextHopASNPayload:
    """This datastructure represents JSON Interface.TopNextHopASN payload as it is transmitted to and from KentikAPI"""

    # GET, POST, PUT request/response
    Asn: int
    Packets: int

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return from_dict(data_class=cls, data=dic)

    def to_top_next_hop_asn(self) -> TopNextHopASN:
        return TopNextHopASN(asn=self.Asn, packets=self.Packets)


@dataclass
class VRFAttributesPayload:
    """This datastructure represents JSON Interface.VRFAttributes payload as it is transmitted to and from KentikAPI"""

    # GET, POST, PUT request/response
    name: str
    route_target: str
    route_distinguisher: str
    description: Optional[str] = None

    # POST, PUT request
    ext_route_distinguisher: Optional[int] = None

    # GET response
    id: Optional[int] = None
    company_id: Optional[str] = None
    device_id: Optional[str] = None

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        # recreate GET/POST/PUT response payload: fill all available fields
        return from_dict(data_class=cls, data=dic)

    @classmethod
    def from_vrf_attributes(cls, vrf: VRFAttributes):
        # prepare POST/PUT request payload: fill only the user-provided fields
        return cls(
            name=vrf.name,
            route_target=vrf.route_target,
            route_distinguisher=vrf.route_distinguisher,
            description=vrf.description,
            ext_route_distinguisher=vrf.ext_route_distinguisher,
        )

    def to_vrf_attributes(self) -> VRFAttributes:
        return VRFAttributes(
            name=self.name,
            description=self.description,
            route_target=self.route_target,
            route_distinguisher=self.route_distinguisher,
            ext_route_distinguisher=self.ext_route_distinguisher,
            id=convert_or_none(self.id, ID),
            company_id=convert_or_none(self.company_id, ID),
            device_id=convert_or_none(self.device_id, ID),
        )


@dataclass
class InterfacePayload:
    """This datastructure represents JSON Interface payload as it is transmitted to and from KentikAPI"""

    snmp_id: Optional[str] = None
    snmp_speed: Optional[int] = None  # caveat: GET returns snmp_speed as str and must be manually converted
    interface_description: Optional[str] = None
    id: Optional[str] = None
    company_id: Optional[str] = None
    device_id: Optional[str] = None
    cdate: Optional[str] = None
    edate: Optional[str] = None
    snmp_alias: Optional[str] = None
    interface_ip: Optional[str] = None
    interface_ip_netmask: Optional[str] = None
    vrf_id: Optional[str] = None
    vrf: Optional[VRFAttributesPayload] = None
    secondary_ips: Optional[List[SecondaryIPPayload]] = None
    initial_snmp_id: Optional[str] = None
    initial_snmp_alias: Optional[str] = None
    initial_interface_description: Optional[str] = None
    initial_snmp_speed: Optional[float] = None
    provider: Any = None
    top_nexthop_asns: Optional[List[TopNextHopASNPayload]] = None

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        required_fields = [
            "id",
            "snmp_id",
            "snmp_speed",
            "interface_description",
            "company_id",
            "device_id",
            "cdate",
            "edate",
        ]
        validate_fields(class_name=cls.__name__, required_fields=required_fields, dic=dic)

        # recreate GET/POST/PUT response payload: fill all available fields
        # warning: snmp_speed comes back as str for GET, but as int for POST/PUT
        # warning: initial_snmp_id comes back as empty string instead of null when not set
        return cls(
            # always returned fields
            id=dic["id"],
            snmp_id=dic["snmp_id"],
            snmp_speed=convert(dic["snmp_speed"], int),
            interface_description=dic["interface_description"],
            company_id=dic["company_id"],
            device_id=dic["device_id"],
            cdate=dic["cdate"],
            edate=dic["edate"],
            # optional fields
            snmp_alias=dic.get("snmp_alias"),
            interface_ip=dic.get("interface_ip"),
            interface_ip_netmask=dic.get("interface_ip_netmask"),
            vrf_id=dic.get("vrf_id"),
            vrf=convert_or_none(dic.get("vrf"), VRFAttributesPayload.from_dict),
            secondary_ips=convert_list_or_none(dic.get("secondary_ips"), SecondaryIPPayload.from_dict),
            initial_snmp_id=dic.get("initial_snmp_id") if dic.get("initial_snmp_id") != "" else None,
            initial_snmp_alias=dic.get("initial_snmp_alias"),
            initial_interface_description=dic.get("initial_interface_description"),
            initial_snmp_speed=dic.get("initial_snmp_speed"),
            provider=dic.get("provider"),
            top_nexthop_asns=convert_list_or_none(dic.get("top_nexthop_asns"), TopNextHopASNPayload.from_dict),
        )

    @classmethod
    def from_interface(cls, interface: Interface):
        # prepare POST/PUT request payload: fill only the user-provided fields
        return cls(
            snmp_id=convert_or_none(interface.snmp_id, str),
            snmp_speed=interface.snmp_speed,
            interface_description=interface.interface_description,
            snmp_alias=interface.snmp_alias,
            interface_ip=interface.interface_ip,
            interface_ip_netmask=interface.interface_ip_netmask,
            vrf_id=convert_or_none(interface.vrf_id, str),
            vrf=convert_or_none(interface.vrf, VRFAttributesPayload.from_vrf_attributes),
            secondary_ips=convert_list_or_none(interface.secondary_ips, SecondaryIPPayload.from_secondary_ip),
        )

    def to_interface(self) -> Interface:
        return Interface(
            id=convert_or_none(self.id, ID),
            snmp_id=convert_or_none(self.snmp_id, ID),
            snmp_speed=self.snmp_speed,
            snmp_alias=self.snmp_alias,
            interface_ip=self.interface_ip,
            interface_ip_netmask=self.interface_ip_netmask,
            interface_description=self.interface_description,
            vrf_id=convert_or_none(self.vrf_id, ID),
            vrf=convert_or_none(self.vrf, VRFAttributesPayload.to_vrf_attributes),
            secondary_ips=convert_list_or_none(self.secondary_ips, SecondaryIPPayload.to_secondary_ip),
            company_id=convert_or_none(self.company_id, ID),
            device_id=convert_or_none(self.device_id, ID),
            created_date=self.cdate,
            updated_date=self.edate,
            initial_snmp_id=convert_or_none(self.initial_snmp_id, ID),
            initial_snmp_alias=self.initial_snmp_alias,
            initial_interface_description=self.initial_interface_description,
            initial_snmp_speed=convert_or_none(self.initial_snmp_speed, int),
            provider=self.provider,
            top_nexthop_asns=convert_list_or_none(self.top_nexthop_asns, TopNextHopASNPayload.to_top_next_hop_asn),
        )


@dataclass()
class GetResponse:
    interface: InterfacePayload

    @classmethod
    def from_json(cls, json_string: str):
        # for GET response the payload json is like: "interface": {...}
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string, root="interface")
        return cls.from_dict(dic)

    @classmethod
    def from_dict(cls, dic: Dict[str, Any]):
        return cls(interface=InterfacePayload.from_dict(dic))

    def to_interface(self) -> Interface:
        return self.interface.to_interface()


@dataclass
class GetAllResponse:
    interfaces: List[GetResponse]

    @classmethod
    def from_json(cls, json_string: str):
        items = list_from_json(class_name=cls.__name__, json_string=json_string)
        interfaces = [GetResponse.from_dict(item) for item in items]
        return cls(interfaces=interfaces)

    def to_interfaces(self) -> List[Interface]:
        return [item.to_interface() for item in self.interfaces]


@dataclass
class CreateRequest(InterfacePayload):
    @classmethod
    def from_interface(cls, interface: Interface):
        CreateRequest.validate(interface)
        return InterfacePayload.from_interface(interface)

    @staticmethod
    def validate(interface: Interface) -> None:
        operation = "Create"
        if interface.snmp_id is None:
            raise IncompleteObjectError(operation, interface.__class__.__name__, "snmp_id is required")
        if interface.snmp_speed is None:
            raise IncompleteObjectError(operation, interface.__class__.__name__, "snmp_speed is required")
        if interface.interface_description is None:
            raise IncompleteObjectError(
                operation,
                interface.__class__.__name__,
                "interface_description is required",
            )


@dataclass
class UpdateRequest(InterfacePayload):
    @classmethod
    def from_interface(cls, interface: Interface):
        # no validation; for update all fields are optional
        return InterfacePayload.from_interface(interface)


@dataclass
class CreateResponse:
    interface: InterfacePayload

    @classmethod
    def from_json(cls, json_string: str):
        dic = dict_from_json(class_name=cls.__name__, json_string=json_string)
        return cls(interface=InterfacePayload.from_dict(dic))

    def to_interface(self) -> Interface:
        return self.interface.to_interface()


UpdateResponse = CreateResponse
