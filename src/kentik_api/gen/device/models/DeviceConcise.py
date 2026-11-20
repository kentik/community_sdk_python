# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .DeviceNmsConfig import DeviceNmsConfig
from .DeviceSnmpV3Conf import DeviceSnmpV3Conf


class DeviceConcise(BaseModel):
    """
    DeviceConcise
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="id\n\nSystem generated unique identifier",
    )

    deviceName: Optional[str] = Field(
        validation_alias="deviceName",
        default=None,
        description="Device name (device_name) - The name of the device. Valid characters: alphanumeric and underscores. Length: min=4, max=60.",
    )

    deviceSubtype: Optional[str] = Field(
        validation_alias="deviceSubtype",
        default=None,
        description="Device subtype (device_subtype) - The device subtype.",
    )

    cdnAttr: Optional[str] = Field(
        validation_alias="cdnAttr",
        default=None,
        description='CDN attributes (cdn_attr) - If this is a DNS server, you can contribute its queries to Kentik\'s CDN attribution database. Valid values: "Y" or "N". ** cdn_attr is required when the device subtype\'s parent type is "host-nprobe-dns-www"',
    )

    deviceDescription: Optional[str] = Field(
        validation_alias="deviceDescription",
        default=None,
        description="Description (device_description) - The device description. Valid characters: any. Length: max=128.",
    )

    sendingIps: Optional[List[str]] = Field(
        validation_alias="sendingIps",
        default=None,
        description='Device ip (sending_ips) - Array containing one or more IP address(es), from which the device is sending flow. ** sending_ips is required when the device subtype\'s parent type is "router"',
    )

    deviceSampleRate: Optional[float] = Field(
        validation_alias="deviceSampleRate",
        default=None,
        description='Sample rate (device_sample_rate) - The rate at which the device is sampling flows. Valid values: integer bigger than 1. Recommended rate varies depending on flow volume; see https://kb.kentik.com/Ab02.htm#Ab02-Flow_Sampling. ** device_sample_rate is required when the device subtype\'s parent type is "router"',
    )

    planId: Optional[int] = Field(
        validation_alias="planId",
        default=None,
        description="Plan (plan_id) - The ID of the plan to which this device is assigned. Available plan(s) can be found via the Plans API. Valid value: integer.",
    )

    siteId: Optional[int] = Field(
        validation_alias="siteId",
        default=None,
        description="Site (site_id) - The ID of the site (if any) to which this device is assigned. Site IDs are system generated when a site is created. Valid value: integer.",
    )

    minimizeSnmp: Optional[bool] = Field(
        validation_alias="minimizeSnmp",
        default=None,
        description='SNMP polling (minimize_snmp) - The interval at which SNMP will be polled. If "false" (Standard), interface counter will be polled every 10 minutes and interface description every 30 minutes. If "true" (Minimum) (Minimum), interface counter won\'t be polled and interface description will be polled every 6 hours. ** minimize_snmp is required when the device subtype\'s parent type is "router"',
    )

    deviceSnmpIp: Optional[str] = Field(
        validation_alias="deviceSnmpIp",
        default=None,
        description='Device SNMP IP (device_snmp_ip) - The SNMP IP to use when polling the device. device_snmp_ip is ignored unless the device subtype\'s parent type is "router"',
    )

    deviceSnmpCommunity: Optional[str] = Field(
        validation_alias="deviceSnmpCommunity",
        default=None,
        description='SNMP community (device_snmp_community) - The SNMP community to use when polling the device. device_snmp_community is ignored unless the device subtype\'s parent type is "router"',
    )

    deviceSnmpV3Conf: Optional[DeviceSnmpV3Conf] = Field(
        validation_alias="deviceSnmpV3Conf", default=None
    )

    deviceBgpType: Optional[str] = Field(
        validation_alias="deviceBgpType",
        default=None,
        description='BGP (device_bgp_type) - Device bgp type. Valid values: "none" (use generic IP/ASN mapping), "device" (peer with the device itself), "other_device" (share routing table of existing peered device)',
    )

    deviceBgpNeighborIp: Optional[str] = Field(
        validation_alias="deviceBgpNeighborIp",
        default=None,
        description='Your IPv4 peering address (device_bgp_neighbor_ip) - A valid IPv4 address to use for peering with the device. ** An IPv4 and/or IPv6 peering address is required when device_bgp_type is set to "device"',
    )

    deviceBgpNeighborIp6: Optional[str] = Field(
        validation_alias="deviceBgpNeighborIp6",
        default=None,
        description='Your IPv6 peering address (device_bgp_neighbor_ip6) - A valid IPv6 address to use for peering with the device. ** An IPv4 and/or IPv6 peering address is required when device_bgp_type is set to "device"',
    )

    deviceBgpNeighborAsn: Optional[str] = Field(
        validation_alias="deviceBgpNeighborAsn",
        default=None,
        description='Your ASN (device_bgp_neighbor_asn) - The valid AS number (ASN) of the autonomous system that this device belongs to. ** device_bgp_neighbor_asn is required when device_bgp_type is set to "device"',
    )

    deviceBgpPassword: Optional[str] = Field(
        validation_alias="deviceBgpPassword",
        default=None,
        description='BGP md5 password (device_bgp_password) - Optional BGP MD5 password (shared authentication password for BGP peering). Valid characters: printable ASCII excluding space and question mark. Length: 32. device_bgp_password is optional when device_bgp_type is set to "device"',
    )

    useBgpDeviceId: Optional[str] = Field(
        validation_alias="useBgpDeviceId",
        default=None,
        description='Select master BGP device (use_bgp_device_id) - The ID of the device whose BGP table should be shared with this device. ** use_bgp_device_id is required when device_bgp_type is set to "other_device"). Valid value: a system-generated device_id',
    )

    deviceBgpFlowspec: Optional[bool] = Field(
        validation_alias="deviceBgpFlowspec",
        default=None,
        description="BGP Flowspec Compatibility (device_bgp_flowspec) - Toggle BGP Flowspec Compatibility for device.",
    )

    nms: Optional[DeviceNmsConfig] = Field(validation_alias="nms", default=None)

    deviceBgpCredentialName: Optional[str] = Field(
        validation_alias="deviceBgpCredentialName",
        default=None,
        description="BGP Credential Name (device_bgp_credential_name) - Unsupported Field. Use device_bgp_password instead.",
    )

    flowSnmpCredentialName: Optional[str] = Field(
        validation_alias="flowSnmpCredentialName",
        default=None,
        description="Snmp Credential Name (flow_snmp_credential_name) - Optional Credential Name (Credential for Flow Snmp peering). Valid characters: alphanumeric. Length: 32.",
    )

    monitoringTemplateId: Optional[int] = Field(
        validation_alias="monitoringTemplateId",
        default=None,
        description="Monitoring template - The ID of the monitoring template assigned to this device.",
    )

    deviceAlert: Optional[str] = Field(
        validation_alias="deviceAlert",
        default=None,
        description="Device alert - The device alert endpoint URL.",
    )
