# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .FlowTag import FlowTag


class SearchFlowTagResponse(BaseModel):
    """
    SearchFlowTagResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    flowTags: Optional[List[Optional[FlowTag]]] = Field(
        validation_alias="flowTags", default=None
    )

    totalCount: Optional[int] = Field(validation_alias="totalCount", default=None)

    invalidCount: Optional[int] = Field(validation_alias="invalidCount", default=None)
