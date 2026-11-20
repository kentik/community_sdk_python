# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .TagValue import TagValue


class GetTagValuesResponse(BaseModel):
    """
    GetTagValuesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tagValues: Optional[List[Optional[TagValue]]] = Field(
        validation_alias="tagValues", default=None, description="Tag values response"
    )
