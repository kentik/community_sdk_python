# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CustomColumnData import CustomColumnData
from .DeviceNmsConfig import DeviceNmsConfig
from .DeviceSnmpV3Conf import DeviceSnmpV3Conf
from .GnmiV1Conf import GnmiV1Conf
from .Interface import Interface
from .Label import Label
from .Plan import Plan
from .Site import Site


class DeviceDetailed(BaseModel):
    """
    DeviceDetailed
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="System generated unique identifier",
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId", default=None, description="Company ID"
    )

    deviceName: Optional[str] = Field(
        validation_alias="deviceName", default=None, description="Device name"
    )

    deviceAlias: Optional[str] = Field(
        validation_alias="deviceAlias", default=None, description="Device alias"
    )

    deviceType: Optional[str] = Field(
        validation_alias="deviceType", default=None, description="Device type"
    )

    deviceDescription: Optional[str] = Field(
        validation_alias="deviceDescription",
        default=None,
        description="Device description",
    )

    site: Optional[Site] = Field(validation_alias="site", default=None)

    plan: Optional[Plan] = Field(validation_alias="plan", default=None)

    labels: Optional[List[Optional[Label]]] = Field(
        validation_alias="labels", default=None, description="List of labels"
    )

    allInterfaces: Optional[List[Optional[Interface]]] = Field(
        validation_alias="allInterfaces", default=None, description="List of interfaces"
    )

    deviceFlowType: Optional[str] = Field(
        validation_alias="deviceFlowType", default=None, description="Device flow type"
    )

    deviceSampleRate: Optional[str] = Field(
        validation_alias="deviceSampleRate",
        default=None,
        description="Device sample rate",
    )

    sendingIps: Optional[List[str]] = Field(
        validation_alias="sendingIps", default=None, description="List of sending IPs"
    )

    deviceSnmpIp: Optional[str] = Field(
        validation_alias="deviceSnmpIp", default=None, description="Device SNMP IP"
    )

    deviceSnmpCommunity: Optional[str] = Field(
        validation_alias="deviceSnmpCommunity",
        default=None,
        description="Keeping these tokens so we can give the user a useful error.  They are removed from DeviceRequest\n\nDevice SNMP community",
    )

    minimizeSnmp: Optional[bool] = Field(
        validation_alias="minimizeSnmp", default=None, description="Minimize SNMP"
    )

    deviceBgpType: Optional[str] = Field(
        validation_alias="deviceBgpType", default=None, description="Device BGP type"
    )

    deviceBgpNeighborIp: Optional[str] = Field(
        validation_alias="deviceBgpNeighborIp",
        default=None,
        description="Device BGP neighbor IP",
    )

    deviceBgpNeighborIp6: Optional[str] = Field(
        validation_alias="deviceBgpNeighborIp6",
        default=None,
        description="Device BGP neighbor IP6",
    )

    deviceBgpNeighborAsn: Optional[str] = Field(
        validation_alias="deviceBgpNeighborAsn",
        default=None,
        description="Device BGP neighbor ASN",
    )

    deviceBgpFlowspec: Optional[bool] = Field(
        validation_alias="deviceBgpFlowspec",
        default=None,
        description="Device BGP flowspec",
    )

    deviceBgpPassword: Optional[str] = Field(
        validation_alias="deviceBgpPassword",
        default=None,
        description="Keeping these tokens so we can give the user a useful error.  They are removed from DeviceRequest\n\nDevice BGP password",
    )

    deviceBgpLabelUnicast: Optional[bool] = Field(
        validation_alias="deviceBgpLabelUnicast",
        default=None,
        description="Device BGP label unicast",
    )

    bgpLookupStrategy: Optional[str] = Field(
        validation_alias="bgpLookupStrategy",
        default=None,
        description="BGP lookup strategy",
    )

    deviceStatus: Optional[str] = Field(
        validation_alias="deviceStatus", default=None, description="Device status"
    )

    useBgpDeviceId: Optional[str] = Field(
        validation_alias="useBgpDeviceId", default=None, description="Use BGP device ID"
    )

    customColumns: Optional[str] = Field(
        validation_alias="customColumns", default=None, description="Custom columns"
    )

    customColumnData: Optional[List[Optional[CustomColumnData]]] = Field(
        validation_alias="customColumnData",
        default=None,
        description="Custom column data",
    )

    deviceChfClientPort: Optional[str] = Field(
        validation_alias="deviceChfClientPort",
        default=None,
        description="Device CHF client port",
    )

    deviceChfClientProtocol: Optional[str] = Field(
        validation_alias="deviceChfClientProtocol",
        default=None,
        description="Device CHF client protocol",
    )

    deviceChfInterface: Optional[str] = Field(
        validation_alias="deviceChfInterface",
        default=None,
        description="Device CHF interface",
    )

    deviceAgentType: Optional[str] = Field(
        validation_alias="deviceAgentType",
        default=None,
        description="Device agent type",
    )

    maxFlowRate: Optional[int] = Field(
        validation_alias="maxFlowRate", default=None, description="Max flow rate"
    )

    maxBigFlowRate: Optional[int] = Field(
        validation_alias="maxBigFlowRate", default=None, description="Max big flow rate"
    )

    deviceProxyBgp: Optional[str] = Field(
        validation_alias="deviceProxyBgp", default=None, description="Device proxy BGP"
    )

    deviceProxyBgp6: Optional[str] = Field(
        validation_alias="deviceProxyBgp6",
        default=None,
        description="Device proxy BGP6",
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="Creation timestamp (UTC)",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="Last modification timestamp (UTC)",
    )

    deviceSnmpV3ConfEnabled: Optional[bool] = Field(
        validation_alias="deviceSnmpV3ConfEnabled",
        default=None,
        description="Device SNMP v3 configuration enabled",
    )

    deviceSnmpV3Conf: Optional[DeviceSnmpV3Conf] = Field(
        validation_alias="deviceSnmpV3Conf", default=None
    )

    cdnAttr: Optional[str] = Field(
        validation_alias="cdnAttr", default=None, description="CDN attributes"
    )

    bgpPeerIp4: Optional[str] = Field(
        validation_alias="bgpPeerIp4", default=None, description="BGP peer IP4"
    )

    bgpPeerIp6: Optional[str] = Field(
        validation_alias="bgpPeerIp6", default=None, description="BGP peer IP6"
    )

    deviceSubtype: Optional[str] = Field(
        validation_alias="deviceSubtype", default=None, description="Device subtype"
    )

    deviceVendorType: Optional[str] = Field(
        validation_alias="deviceVendorType",
        default=None,
        description="Device vendor type",
    )

    deviceModelType: Optional[str] = Field(
        validation_alias="deviceModelType",
        default=None,
        description="Device model type",
    )

    cloudExportId: Optional[str] = Field(
        validation_alias="cloudExportId", default=None, description="Cloud export ID"
    )

    deviceKproxy: Optional[str] = Field(
        validation_alias="deviceKproxy", default=None, description="Device KProxy"
    )

    snmpEnabled: Optional[str] = Field(
        validation_alias="snmpEnabled", default=None, description="SNMP enabled"
    )

    snmpDisabledReason: Optional[str] = Field(
        validation_alias="snmpDisabledReason",
        default=None,
        description="SNMP disabled reason",
    )

    snmpDisabledReasonOther: Optional[str] = Field(
        validation_alias="snmpDisabledReasonOther",
        default=None,
        description="SNMP disabled reason other",
    )

    bgpDisabledReason: Optional[str] = Field(
        validation_alias="bgpDisabledReason",
        default=None,
        description="BGP disabled reason",
    )

    bgpDisabledReasonOther: Optional[str] = Field(
        validation_alias="bgpDisabledReasonOther",
        default=None,
        description="BGP disabled reason other",
    )

    deviceManufacturer: Optional[str] = Field(
        validation_alias="deviceManufacturer",
        default=None,
        description="Device manufacturer",
    )

    deviceAlert: Optional[str] = Field(
        validation_alias="deviceAlert", default=None, description="Device alert"
    )

    role: Optional[str] = Field(
        validation_alias="role", default=None, description="Role"
    )

    deviceGnmiV1Conf: Optional[GnmiV1Conf] = Field(
        validation_alias="deviceGnmiV1Conf", default=None
    )

    useAsnFromFlow: Optional[bool] = Field(
        validation_alias="useAsnFromFlow", default=None, description="Use ASN from flow"
    )

    maxInterface: Optional[int] = Field(
        validation_alias="maxInterface", default=None, description="Max interface"
    )

    maxInterfaceCheck: Optional[int] = Field(
        validation_alias="maxInterfaceCheck",
        default=None,
        description="Max interface check",
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

    osName: Optional[str] = Field(
        validation_alias="osName", default=None, description="Operating system name"
    )

    osVersion: Optional[str] = Field(
        validation_alias="osVersion",
        default=None,
        description="Operating system version",
    )

    serialNumber: Optional[str] = Field(
        validation_alias="serialNumber", default=None, description="Serial number"
    )
