# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Insight import Insight


class GetASNInsightsResponse(BaseModel):
    """
    GetASNInsightsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    insights: Optional[List[Optional[Insight]]] = Field(
        validation_alias="insights",
        default=None,
        description="List of ASN-specific insights",
    )
