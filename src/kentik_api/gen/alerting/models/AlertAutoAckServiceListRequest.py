# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AlertAutoAckFilters import AlertAutoAckFilters
from .PaginationConfig import PaginationConfig
from .SortingConfig import SortingConfig


class AlertAutoAckServiceListRequest(BaseModel):
    """
    AlertAutoAckServiceListRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationConfig] = Field(
        validation_alias="pagination", default=None
    )

    sorting: Optional[SortingConfig] = Field(validation_alias="sorting", default=None)

    filters: Optional[AlertAutoAckFilters] = Field(
        validation_alias="filters", default=None
    )
