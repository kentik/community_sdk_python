# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict

from pydantic import BaseModel, Field


class ASGroupServiceUpdateASGroupBody(BaseModel):
    """
    UpdateASGroupRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asGroup: Dict[str, Any] = Field(
        validation_alias="asGroup", description="ASGroupConcise"
    )
