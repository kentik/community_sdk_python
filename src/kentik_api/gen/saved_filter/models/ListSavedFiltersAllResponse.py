# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .SavedFilter import SavedFilter


class ListSavedFiltersAllResponse(BaseModel):
    """
    ListSavedFiltersAllResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filters: Optional[List[Optional[SavedFilter]]] = Field(
        validation_alias="filters", default=None
    )
