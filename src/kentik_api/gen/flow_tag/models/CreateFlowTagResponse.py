# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowTag import FlowTag


class CreateFlowTagResponse(BaseModel):
    """
    CreateFlowTagResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    flowTag: Optional[FlowTag] = Field(validation_alias="flowTag", default=None)
