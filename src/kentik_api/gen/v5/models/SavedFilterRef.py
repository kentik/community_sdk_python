# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class SavedFilterRef(BaseModel):
    """
    A saved filter to apply.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filter_id: Optional[int] = Field(
        validation_alias="filter_id", default=None, description="The saved filter ID."
    )

    is_not: Optional[bool] = Field(
        validation_alias="is_not",
        default=None,
        description="Excludes the matching traffic instead of including it.",
    )
