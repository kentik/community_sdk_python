# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .DeviceDetailed import DeviceDetailed


class CreateDevicesResponse(BaseModel):
    """
    CreateDevicesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    devices: Optional[List[Optional[DeviceDetailed]]] = Field(
        validation_alias="devices",
        default=None,
        description="List of configurations of newly created devices",
    )

    failedDevices: Optional[List[str]] = Field(
        validation_alias="failedDevices",
        default=None,
        description="List of names of devices that failed to be created",
    )
