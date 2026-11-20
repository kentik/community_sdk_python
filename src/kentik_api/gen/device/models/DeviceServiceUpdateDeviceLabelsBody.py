# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List

from pydantic import BaseModel, Field

from .LabelConcise import LabelConcise


class DeviceServiceUpdateDeviceLabelsBody(BaseModel):
    """
    UpdateDeviceLabelsRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    labels: List[LabelConcise] = Field(
        validation_alias="labels",
        description="List of labels to be added to the device",
    )
