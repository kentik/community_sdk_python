# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class RTBHAction(BaseModel):
    """
    RTBHAction model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    bgpCommunities: Optional[List[int]] = Field(
        validation_alias="bgpCommunities", default=None
    )

    nextHop: Optional[str] = Field(validation_alias="nextHop", default=None)

    localPreference: Optional[int] = Field(
        validation_alias="localPreference", default=None
    )
