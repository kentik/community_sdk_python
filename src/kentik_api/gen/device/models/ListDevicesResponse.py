# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .DeviceDetailed import DeviceDetailed


class ListDevicesResponse(BaseModel):
    """
    ListDevicesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    devices: Optional[List[Optional[DeviceDetailed]]] = Field(
        validation_alias="devices",
        default=None,
        description="List of configurations of devices",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
