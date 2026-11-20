# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .ASGroupConcise import ASGroupConcise


class CreateASGroupRequest(BaseModel):
    """
    CreateASGroupRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asGroup: ASGroupConcise = Field(validation_alias="asGroup")
