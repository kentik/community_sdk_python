# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Mitigation import Mitigation
from .PaginationInfo import PaginationInfo


class MitigationsServiceListResponse(BaseModel):
    """
    MitigationsServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationInfo] = Field(
        validation_alias="pagination", default=None
    )

    mitigations: Optional[List[Optional[Mitigation]]] = Field(
        validation_alias="mitigations",
        default=None,
        description="The mitigations that were found matching the filters.",
    )
