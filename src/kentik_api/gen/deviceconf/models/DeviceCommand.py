# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class DeviceCommand(BaseModel):
    """
    DeviceCommand model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceId: Optional[str] = Field(validation_alias="deviceId", default=None)

    command: Optional[str] = Field(validation_alias="command", default=None)
