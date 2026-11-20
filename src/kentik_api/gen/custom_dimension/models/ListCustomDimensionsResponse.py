# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CustomDimension import CustomDimension


class ListCustomDimensionsResponse(BaseModel):
    """
    ListCustomDimensionsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dimensions: Optional[List[Optional[CustomDimension]]] = Field(
        validation_alias="dimensions", default=None
    )
