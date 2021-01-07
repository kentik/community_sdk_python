# Standard library imports
import json
from typing import List, Union, Optional
from dataclasses import dataclass

# Local application imports
# from kentik_api.requests_payload.notset import NOTSET, _NOTSET, _NOTSET_, _None_


from kentik_api.public.device import Device, DeviceType, DeviceSubtype, DeviceBGPType


# @dataclass()
# class _DeviceSnmpV3Conf:
#     UserName: Union[str, None, NOTSET] = _NOTSET
#     AuthenticationProtocol: Union[str, None, NOTSET] = _NOTSET
#     AuthenticationPassphrase: Union[str, None, NOTSET] = _NOTSET
#     PrivacyPassphrase: Union[str, None, NOTSET] = _NOTSET


# pylint: disable=too-many-instance-attributes


@dataclass()
class GetResponse:
    # user-provided when updating the device, server-provided when creating a device
    id: Optional[int] = None
    # user-provided
    plan_id: Optional[int] = None
    site_id: Optional[int] = None
    device_name: Optional[str] = None
    device_type: Optional[DeviceType] = None
    device_subtype: Optional[DeviceSubtype] = None
    device_description: Optional[str] = None
    device_sample_rate: Optional[int] = None
    sending_ips: List[str] = []
    device_snmp_ip: Optional[str] = None
    device_snmp_community: Optional[str] = None
    minimize_snmp: Optional[bool] = None
    device_bgp_type: Optional[DeviceBGPType] = None
    device_bgp_neighbor_ip: Optional[str] = None
    device_bgp_neighbor_ip6: Optional[str] = None
    device_bgp_neighbor_asn: Optional[int] = None
    device_bgp_flowspec: Optional[bool] = None
    device_bgp_password: Optional[str] = None
    use_bgp_device_id: Optional[int] = None
    # server-provided
    device_status: Optional[str] = None
    device_flow_type: Optional[str] = None
    company_id: Optional[str] = None
    snmp_last_updated: Optional[str] = None
    created_date: Optional[str] = None
    updated_date: Optional[str] = None
    bgp_peer_ip4: Optional[str] = None
    bgp_peer_ip6: Optional[str] = None

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_device(self) -> Device:
        return Device()


# @dataclass()
# class Device:
#     device_name: Union[str, None, NOTSET] = _NOTSET
#     device_subtype: Union[str, None, NOTSET] = _NOTSET
#     device_description: Union[str, None, NOTSET] = _NOTSET
#     sending_ips: Union[List[str], None, NOTSET] = _NOTSET
#     device_sample_rate: Union[int, None, NOTSET] = _NOTSET
#     plan_id: Union[int, None, NOTSET] = _NOTSET
#     minimize_snmp: Union[bool, None, NOTSET] = _NOTSET
#     device_snmp_ip: Union[str, None, NOTSET] = _NOTSET
#     device_snmp_community: Union[str, None, NOTSET] = _NOTSET
#     device_snmp_v3_conf: Union[_DeviceSnmpV3Conf, _NOTSET_, _None_] = _DeviceSnmpV3Conf()
#     device_bgp_type: Union[str, None, NOTSET] = _NOTSET
#     device_bgp_neighbor_ip: Union[str, None, NOTSET] = _NOTSET
#     device_bgp_neighbor_ip6: Union[str, None, NOTSET] = _NOTSET
#     device_bgp_neighbor_asn: Union[str, None, NOTSET] = _NOTSET
#     device_bgp_password: Union[str, None, NOTSET] = _NOTSET
#     device_bgp_flowspec: Union[bool, None, NOTSET] = _NOTSET


# pylint: enable=too-many-instance-attributes
