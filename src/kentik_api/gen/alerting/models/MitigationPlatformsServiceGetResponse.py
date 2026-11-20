# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .MitigationPlatform import MitigationPlatform


class MitigationPlatformsServiceGetResponse(BaseModel):
    """
    MitigationPlatformsServiceGetResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    platform: Optional[MitigationPlatform] = Field(
        validation_alias="platform", default=None
    )
