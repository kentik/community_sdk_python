# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Filter(BaseModel):
    """
    One filter.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filterField: Optional[str] = Field(
        validation_alias="filterField",
        default=None,
        description="The KDE name of the dimension to filter on.",
    )

    operator: Optional[str] = Field(
        validation_alias="operator",
        default=None,
        description="The operator, for example =, <>, ILIKE, NOT ILIKE, ~, !~, >, <, or &.",
    )

    filterValue: Optional[str] = Field(
        validation_alias="filterValue", default=None, description="The value to match."
    )
