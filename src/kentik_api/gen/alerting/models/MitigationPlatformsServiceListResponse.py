# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationPlatform import MitigationPlatform
from .PaginationInfo import PaginationInfo


class MitigationPlatformsServiceListResponse(BaseModel):
    """
    MitigationPlatformsServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationInfo] = Field(
        validation_alias="pagination", default=None
    )

    platforms: Optional[List[Optional[MitigationPlatform]]] = Field(
        validation_alias="platforms",
        default=None,
        description="The mitigation platforms that were found matching the filters.",
    )
