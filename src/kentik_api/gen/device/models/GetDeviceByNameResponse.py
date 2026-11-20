# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .DeviceDetailed import DeviceDetailed


class GetDeviceByNameResponse(BaseModel):
    """
    GetDeviceByNameResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    device: Optional[DeviceDetailed] = Field(validation_alias="device", default=None)
