# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .DeviceSubtype import DeviceSubtype


class PlanDevice(BaseModel):
    """
    Represents a device that is associated with a plan.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The system-assigned unique ID of a device associated with this plan.",
    )

    deviceName: str = Field(
        validation_alias="deviceName",
        description="The user-assigned name of a device associated with this plan.",
    )

    deviceSubtype: DeviceSubtype = Field(validation_alias="deviceSubtype")

    deviceType: DeviceSubtype = Field(validation_alias="deviceType")
