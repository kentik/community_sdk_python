# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CapabilityRelease import CapabilityRelease


class GetCapabilityReleaseResponse(BaseModel):
    """
    GetCapabilityReleaseResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    release: Optional[CapabilityRelease] = Field(
        validation_alias="release", default=None
    )
