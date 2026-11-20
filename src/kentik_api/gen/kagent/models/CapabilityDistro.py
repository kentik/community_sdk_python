# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CapabilityDistro(BaseModel):
    """
    CapabilityDistro model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    distro: Optional[str] = Field(
        validation_alias="distro", default=None, description="The OS distribution"
    )

    arch: Optional[str] = Field(
        validation_alias="arch", default=None, description="The OS architecture"
    )

    os: Optional[str] = Field(
        validation_alias="os", default=None, description="The OS name"
    )
