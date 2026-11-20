# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Capability import Capability


class ListCapabilitiesResponse(BaseModel):
    """
    ListCapabilitiesResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capabilities: Optional[List[Optional[Capability]]] = Field(
        validation_alias="capabilities",
        default=None,
        description="The list of capabilities",
    )
