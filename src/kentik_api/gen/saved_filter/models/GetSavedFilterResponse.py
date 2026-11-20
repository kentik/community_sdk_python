# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SavedFilter import SavedFilter


class GetSavedFilterResponse(BaseModel):
    """
    GetSavedFilterResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filter: Optional[SavedFilter] = Field(validation_alias="filter", default=None)
