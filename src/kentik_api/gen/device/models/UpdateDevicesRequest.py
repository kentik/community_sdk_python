# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List

from pydantic import BaseModel, Field

from .DeviceConcise import DeviceConcise


class UpdateDevicesRequest(BaseModel):
    """
    UpdateDevicesRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    devices: List[DeviceConcise] = Field(
        validation_alias="devices",
        description="List of configurations of devices to be updated",
    )
