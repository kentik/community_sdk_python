# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .DeviceDetailed import DeviceDetailed


class UpdateDevicesResponse(BaseModel):
    """
    UpdateDevicesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    devices: Optional[List[Optional[DeviceDetailed]]] = Field(
        validation_alias="devices",
        default=None,
        description="List of configurations of updated devices",
    )

    failedDevices: Optional[List[str]] = Field(
        validation_alias="failedDevices",
        default=None,
        description="List of IDs of devices that failed to be updated",
    )
