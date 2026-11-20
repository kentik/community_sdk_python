# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class DeviceNmsSnmpConfig(BaseModel):
    """
    DeviceNmsSnmpConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    credentialName: Optional[str] = Field(
        validation_alias="credentialName",
        default=None,
        description="Name of the SNMP credentials from the credential vault.",
    )

    port: Optional[int] = Field(
        validation_alias="port",
        default=None,
        description="SNMP port, to override default of 161.",
    )

    timeout: Optional[str] = Field(
        validation_alias="timeout",
        default=None,
        description="Timeout, to override default of 2s.",
    )
