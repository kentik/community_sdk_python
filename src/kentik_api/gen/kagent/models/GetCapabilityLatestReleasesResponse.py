# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CapabilityRelease import CapabilityRelease


class GetCapabilityLatestReleasesResponse(BaseModel):
    """
    GetCapabilityLatestReleasesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    releases: Optional[List[Optional[CapabilityRelease]]] = Field(
        validation_alias="releases",
        default=None,
        description="A list containing all latest releases",
    )
