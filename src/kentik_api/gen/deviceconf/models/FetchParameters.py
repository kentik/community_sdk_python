# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FetchParameters(BaseModel):
    """
    FetchParameters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    fetchInterval: Optional[str] = Field(
        validation_alias="fetchInterval",
        default=None,
        description="How often the device should be fetched.",
    )

    fetchTimeout: Optional[str] = Field(
        validation_alias="fetchTimeout",
        default=None,
        description="Maximum time allowed for a single fetch attempt.\nIf unset or set to 0s, the server default timeout is used.\nThis value should be less than or equal to fetch_interval.",
    )
