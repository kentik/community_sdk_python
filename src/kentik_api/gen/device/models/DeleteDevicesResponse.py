# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class DeleteDevicesResponse(BaseModel):
    """
    DeleteDevicesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    failedDevices: Optional[List[str]] = Field(
        validation_alias="failedDevices",
        default=None,
        description="List of IDs of devices that failed to be deleted",
    )
