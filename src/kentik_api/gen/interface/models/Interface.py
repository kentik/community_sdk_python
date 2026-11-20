# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .ConnectivityType import ConnectivityType
from .InterfaceVrf import InterfaceVrf
from .NetworkBoundary import NetworkBoundary


class Interface(BaseModel):
    """
    Interface model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="ID of interface."
    )

    deviceId: Optional[str] = Field(
        validation_alias="deviceId",
        default=None,
        description="ID of device with this interface.",
    )

    snmpId: Optional[str] = Field(
        validation_alias="snmpId", default=None, description="SNMP ID."
    )

    snmpSpeed: Optional[int] = Field(
        validation_alias="snmpSpeed", default=None, description="Network speed in Mbps."
    )

    snmpType: Optional[int] = Field(
        validation_alias="snmpType", default=None, description="Snmp Type."
    )

    snmpAlias: Optional[str] = Field(
        validation_alias="snmpAlias", default=None, description="Interface alias."
    )

    interfaceIp: Optional[str] = Field(
        validation_alias="interfaceIp", default=None, description="IP of interface."
    )

    interfaceDescription: Optional[str] = Field(
        validation_alias="interfaceDescription",
        default=None,
        description="Readable string description of interface.",
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Create timestamp."
    )

    edate: Optional[str] = Field(
        validation_alias="edate", default=None, description="Update Timestamp."
    )

    interfaceIpNetmask: Optional[str] = Field(
        validation_alias="interfaceIpNetmask", default=None, description="Subnet mask."
    )

    connectivityType: Optional[ConnectivityType] = Field(
        validation_alias="connectivityType", default=None
    )

    networkBoundary: Optional[NetworkBoundary] = Field(
        validation_alias="networkBoundary", default=None
    )

    topNexthopAsns: Optional[List[int]] = Field(
        validation_alias="topNexthopAsns", default=None, description="Top asn hops."
    )

    provider: Optional[str] = Field(
        validation_alias="provider", default=None, description="Network provider."
    )

    interfaceKvs: Optional[Dict[str, Any]] = Field(
        validation_alias="interfaceKvs", default=None, description="Interface KVs."
    )

    interfaceTags: Optional[Dict[str, Any]] = Field(
        validation_alias="interfaceTags", default=None, description="Interface Tags."
    )

    interfaceStatus: Optional[str] = Field(
        validation_alias="interfaceStatus",
        default=None,
        description="Interface Status.",
    )

    extraInfo: Optional[Dict[str, Any]] = Field(
        validation_alias="extraInfo", default=None, description="Extra Interface Info."
    )

    initialSnmpId: Optional[str] = Field(
        validation_alias="initialSnmpId", default=None, description="Initial SMNP ID."
    )

    initialSnmpAlias: Optional[str] = Field(
        validation_alias="initialSnmpAlias",
        default=None,
        description="Initial Interface Alias.",
    )

    initialInterfaceDescription: Optional[str] = Field(
        validation_alias="initialInterfaceDescription",
        default=None,
        description="Initial Interface Description.",
    )

    initialSnmpSpeed: Optional[int] = Field(
        validation_alias="initialSnmpSpeed",
        default=None,
        description="Inital Network speed in Mbps.",
    )

    secondaryIps: Optional[str] = Field(
        validation_alias="secondaryIps",
        default=None,
        description="Secondary Interface IP.",
    )

    initialConnectivityType: Optional[ConnectivityType] = Field(
        validation_alias="initialConnectivityType", default=None
    )

    initialNetworkBoundary: Optional[NetworkBoundary] = Field(
        validation_alias="initialNetworkBoundary", default=None
    )

    initialProvider: Optional[str] = Field(
        validation_alias="initialProvider",
        default=None,
        description="Initial Network provider.",
    )

    vrfId: Optional[str] = Field(
        validation_alias="vrfId",
        default=None,
        description="VRF_ID is deprecated for the API, use VRF instead\n\nDeprecated: use VRF field instead",
    )

    vrf: Optional[InterfaceVrf] = Field(validation_alias="vrf", default=None)
