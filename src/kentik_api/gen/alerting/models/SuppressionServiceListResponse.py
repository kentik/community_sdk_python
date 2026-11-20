# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PaginationInfo import PaginationInfo
from .Suppression import Suppression


class SuppressionServiceListResponse(BaseModel):
    """
    SuppressionServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationInfo] = Field(
        validation_alias="pagination", default=None
    )

    suppressions: Optional[List[Optional[Suppression]]] = Field(
        validation_alias="suppressions",
        default=None,
        description="The matching suppression configurations, with resolved timestamps and without timestamp commands.",
    )
