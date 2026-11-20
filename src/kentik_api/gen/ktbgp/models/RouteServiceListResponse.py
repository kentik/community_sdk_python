# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .DeviceAdverts import DeviceAdverts


class RouteServiceListResponse(BaseModel):
    """
    RouteServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    result: Optional[List[Optional[DeviceAdverts]]] = Field(
        validation_alias="result", default=None
    )
