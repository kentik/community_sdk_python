# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class Devices(BaseModel):
    """
    Devices
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    allDevices: Optional[bool] = Field(validation_alias="allDevices", default=None)

    deviceTypes: Optional[List[str]] = Field(
        validation_alias="deviceTypes", default=None
    )

    deviceLabels: Optional[List[int]] = Field(
        validation_alias="deviceLabels", default=None
    )

    deviceSites: Optional[List[int]] = Field(
        validation_alias="deviceSites", default=None
    )

    deviceName: Optional[List[str]] = Field(validation_alias="deviceName", default=None)
