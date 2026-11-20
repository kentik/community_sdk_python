# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Device import Device


class GetDeviceAssignmentsResponse(BaseModel):
    """
    GetDeviceAssignmentsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    devices: Optional[List[Optional[Device]]] = Field(
        validation_alias="devices", default=None
    )
