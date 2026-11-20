# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PaginationInfo import PaginationInfo
from .Policy import Policy


class PolicyServiceListResponse(BaseModel):
    """
    PolicyServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationInfo] = Field(
        validation_alias="pagination", default=None
    )

    policies: Optional[List[Optional[Policy]]] = Field(
        validation_alias="policies",
        default=None,
        description="The alerting policies that were found matching the filters.",
    )
