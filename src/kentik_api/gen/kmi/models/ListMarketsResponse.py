# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Market import Market


class ListMarketsResponse(BaseModel):
    """
    ListMarketsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    markets: Optional[List[Optional[Market]]] = Field(
        validation_alias="markets", default=None, description="Markets"
    )
