# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class KmiServiceGetRankingsBody(BaseModel):
    """
    GetRankingsRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    limit: Optional[int] = Field(
        validation_alias="limit",
        default=None,
        description="Maximum number of entries returned. (Default: 600).",
    )
