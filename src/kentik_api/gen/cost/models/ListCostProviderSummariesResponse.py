# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CostProviderSummary import CostProviderSummary


class ListCostProviderSummariesResponse(BaseModel):
    """
    ListCostProviderSummariesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    providers: Optional[List[Optional[CostProviderSummary]]] = Field(
        validation_alias="providers",
        default=None,
        description="List of summaries of requested cost providers",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
