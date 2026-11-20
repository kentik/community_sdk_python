# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CapabilityDistro import CapabilityDistro


class CapabilitySupportedDistro(BaseModel):
    """
    CapabilitySupportedDistro model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capability: Optional[str] = Field(validation_alias="capability", default=None)

    distros: Optional[List[Optional[CapabilityDistro]]] = Field(
        validation_alias="distros", default=None
    )
