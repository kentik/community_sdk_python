# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Alert import Alert
from .PaginationInfo import PaginationInfo


class AlertServiceListResponse(BaseModel):
    """
    AlertServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationInfo] = Field(
        validation_alias="pagination", default=None
    )

    alerts: Optional[List[Optional[Alert]]] = Field(
        validation_alias="alerts", default=None, description="The alerts result set."
    )
