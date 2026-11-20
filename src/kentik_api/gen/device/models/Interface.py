# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Interface(BaseModel):
    """
    Interface
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    interfaceDescription: Optional[str] = Field(
        validation_alias="interfaceDescription",
        default=None,
        description="Interface description",
    )

    initialSnmpSpeed: Optional[str] = Field(
        validation_alias="initialSnmpSpeed",
        default=None,
        description="Initial SNMP speed",
    )

    deviceId: Optional[str] = Field(
        validation_alias="deviceId", default=None, description="Device ID"
    )

    snmpSpeed: Optional[str] = Field(
        validation_alias="snmpSpeed", default=None, description="SNMP speed"
    )

    snmpAlias: Optional[str] = Field(
        validation_alias="snmpAlias", default=None, description="SNMP alias"
    )

    snmpId: Optional[str] = Field(
        validation_alias="snmpId", default=None, description="SNMP ID"
    )

    connectivityType: Optional[str] = Field(
        validation_alias="connectivityType",
        default=None,
        description="Connectivity type",
    )

    networkBoundary: Optional[str] = Field(
        validation_alias="networkBoundary", default=None, description="Network boundary"
    )

    provider: Optional[str] = Field(
        validation_alias="provider", default=None, description="Provider"
    )
