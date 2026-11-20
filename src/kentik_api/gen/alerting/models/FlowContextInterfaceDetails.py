# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowContextInterfaceDetails(BaseModel):
    """
    FlowContextInterfaceDetails model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    snmpId: Optional[str] = Field(
        validation_alias="snmpId",
        default=None,
        description="The SNMP ID of the interface.",
    )

    snmpAlias: Optional[str] = Field(
        validation_alias="snmpAlias",
        default=None,
        description="The SNMP alias of the interface (e.g. 'eth0').",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="The description of the interface.",
    )

    snmpSpeedMbps: Optional[str] = Field(
        validation_alias="snmpSpeedMbps",
        default=None,
        description="The SNMP speed of the interface in Mbps.",
    )
