# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CapacityPlan import CapacityPlan


class ListCapacityPlansResponse(BaseModel):
    """
    ListCapacityPlansResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capacity: Optional[List[Optional[CapacityPlan]]] = Field(
        validation_alias="capacity", default=None, description="List of capacity plans"
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
