# Standard library imports
from dataclasses import dataclass
from typing import List, Union

# Local application imports
from kentik_api.requests_payload.notset import NOTSET, _NOTSET, _NOTSET_, _None_


@dataclass()
class _DeviceSnmpV3Conf:
    UserName: Union[str, None, NOTSET] = _NOTSET
    AuthenticationProtocol: Union[str, None, NOTSET] = _NOTSET
    AuthenticationPassphrase: Union[str, None, NOTSET] = _NOTSET
    PrivacyPassphrase: Union[str, None, NOTSET] = _NOTSET

# pylint: disable=too-many-instance-attributes

@dataclass()
class Device:
    device_name: Union[str, None, NOTSET] = _NOTSET
    device_subtype: Union[str, None, NOTSET] = _NOTSET
    device_description: Union[str, None, NOTSET] = _NOTSET
    sending_ips: Union[List[str], None, NOTSET] = _NOTSET
    device_sample_rate: Union[int, None, NOTSET] = _NOTSET
    plan_id: Union[int, None, NOTSET] = _NOTSET
    minimize_snmp: Union[bool, None, NOTSET] = _NOTSET
    device_snmp_ip: Union[str, None, NOTSET] = _NOTSET
    device_snmp_community: Union[str, None, NOTSET] = _NOTSET
    device_snmp_v3_conf: Union[_DeviceSnmpV3Conf, _NOTSET_, _None_] = _DeviceSnmpV3Conf()
    device_bgp_type: Union[str, None, NOTSET] = _NOTSET
    device_bgp_neighbor_ip: Union[str, None, NOTSET] = _NOTSET
    device_bgp_neighbor_ip6: Union[str, None, NOTSET] = _NOTSET
    device_bgp_neighbor_asn: Union[str, None, NOTSET] = _NOTSET
    device_bgp_password: Union[str, None, NOTSET] = _NOTSET
    device_bgp_flowspec: Union[bool, None, NOTSET] = _NOTSET

# pylint: enable=too-many-instance-attributes