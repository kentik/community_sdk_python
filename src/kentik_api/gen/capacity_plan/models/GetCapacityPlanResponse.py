# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CapacityPlan import CapacityPlan


class GetCapacityPlanResponse(BaseModel):
    """
    GetCapacityPlanResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capacity: Optional[CapacityPlan] = Field(validation_alias="capacity", default=None)
