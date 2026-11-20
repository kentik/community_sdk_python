# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class FlowContextDeviceDetails(BaseModel):
    """
    FlowContextDeviceDetails model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="The ID of the device."
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="The name of the device."
    )

    type: Optional[str] = Field(
        validation_alias="type",
        default=None,
        description="The type of the device (e.g. 'router').",
    )

    labels: Optional[List[str]] = Field(
        validation_alias="labels",
        default=None,
        description="The labels associated with the device.",
    )
