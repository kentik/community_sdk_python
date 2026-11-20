# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .PaginationConfig import PaginationConfig
from .PolicyListFilters import PolicyListFilters
from .SortingConfig import SortingConfig


class PolicyServiceListRequest(BaseModel):
    """
    PolicyServiceListRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationConfig] = Field(
        validation_alias="pagination", default=None
    )

    sorting: Optional[SortingConfig] = Field(validation_alias="sorting", default=None)

    filters: Optional[PolicyListFilters] = Field(
        validation_alias="filters", default=None
    )
