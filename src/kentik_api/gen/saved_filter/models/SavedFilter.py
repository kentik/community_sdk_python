# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FilterLevel import FilterLevel
from .SavedFilterFilters import SavedFilterFilters


class SavedFilter(BaseModel):
    """
    SavedFilter model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier for the saved filter.",
    )

    filterName: str = Field(
        validation_alias="filterName",
        description="An unique name for the saved filter.",
    )

    filterDescription: Optional[str] = Field(
        validation_alias="filterDescription",
        default=None,
        description="The saved filter's description.",
    )

    filters: Optional[SavedFilterFilters] = Field(
        validation_alias="filters", default=None
    )

    filterLevel: Optional[FilterLevel] = Field(
        validation_alias="filterLevel", default=None
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="Date-time of populator creation, in UTC.",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="Date-time of most-recent populator edit, in UTC.",
    )
