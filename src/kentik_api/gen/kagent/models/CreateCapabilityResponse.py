# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Capability import Capability


class CreateCapabilityResponse(BaseModel):
    """
    CreateCapabilityResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capability: Optional[Capability] = Field(
        validation_alias="capability", default=None
    )
