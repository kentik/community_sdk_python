# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CapabilitySupportedDistro import CapabilitySupportedDistro


class GetCapabilitySupportedDistrosResponse(BaseModel):
    """
    GetCapabilitySupportedDistrosResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capabilities: Optional[List[Optional[CapabilitySupportedDistro]]] = Field(
        validation_alias="capabilities",
        default=None,
        description="The list of distro-based capabilities with their respective supported distributions",
    )
