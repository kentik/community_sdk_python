# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class PaginationInfo(BaseModel):
    """
    PaginationInfo model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    totalCount: Optional[str] = Field(
        validation_alias="totalCount",
        default=None,
        description="total_count is the total number of items in the list.\nIt may be provided optionally if include_total_count is set to false.\nIt will be provided always if include_total_count is set to true.",
    )

    hasMoreResults: Optional[bool] = Field(
        validation_alias="hasMoreResults",
        default=None,
        description="has_more_results is a flag to indicate if there are more results to fetch\nIt may be provided instead of total_count if include_total_count is set to false and it would be very expensive to fetch the total count",
    )
