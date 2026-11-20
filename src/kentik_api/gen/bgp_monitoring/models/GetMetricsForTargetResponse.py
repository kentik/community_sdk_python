# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BgpMetric import BgpMetric


class GetMetricsForTargetResponse(BaseModel):
    """
    GetMetricsForTargetResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    metrics: Optional[List[Optional[BgpMetric]]] = Field(
        validation_alias="metrics",
        default=None,
        description="List of observations (metric values)",
    )
