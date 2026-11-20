# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .DeviceNmsSnmpConfig import DeviceNmsSnmpConfig
from .DeviceNmsStConfig import DeviceNmsStConfig


class DeviceNmsConfig(BaseModel):
    """
    DeviceNmsConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agentId: Optional[str] = Field(
        validation_alias="agentId",
        default=None,
        description="ID of the agent that is monitoring this device.",
    )

    ipAddress: Optional[str] = Field(
        validation_alias="ipAddress",
        default=None,
        description="Local IP address of this device.",
    )

    snmp: Optional[DeviceNmsSnmpConfig] = Field(validation_alias="snmp", default=None)

    st: Optional[DeviceNmsStConfig] = Field(validation_alias="st", default=None)
