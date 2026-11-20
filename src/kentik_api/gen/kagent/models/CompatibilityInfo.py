# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CompatibilityInfo(BaseModel):
    """
    CompatibilityInfo provides details when a distro fallback was used
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tier: Optional[int] = Field(
        validation_alias="tier",
        default=None,
        description="The compatibility tier (1=exact, 2=same-family-newer, 3=same-family-older, 4=cross-family)\n\nThe compatibility tier: 1=exact match, 2=same-family (agent newer), 3=same-family (agent older), 4=cross-family",
    )

    tierName: Optional[str] = Field(
        validation_alias="tierName",
        default=None,
        description="Human-readable tier name\n\nHuman-readable name for the compatibility tier",
    )

    requestedDistro: Optional[str] = Field(
        validation_alias="requestedDistro",
        default=None,
        description="The distro that the agent reported\n\nThe distro reported by the agent",
    )

    matchedDistro: Optional[str] = Field(
        validation_alias="matchedDistro",
        default=None,
        description="The distro of the binary being served\n\nThe distro of the binary that will be served",
    )

    message: Optional[str] = Field(
        validation_alias="message",
        default=None,
        description="Human-readable message explaining the fallback\n\nHuman-readable explanation of the compatibility decision",
    )
