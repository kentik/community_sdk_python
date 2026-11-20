# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class SavedFilterFilterId(BaseModel):
    """
    SavedFilterFilterId model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filterId: Optional[str] = Field(
        validation_alias="filterId",
        default=None,
        description="ID of reference saved filter.",
    )

    isNot: Optional[bool] = Field(
        validation_alias="isNot",
        default=None,
        description="Include/Exclude of the reference saved filter.",
    )
