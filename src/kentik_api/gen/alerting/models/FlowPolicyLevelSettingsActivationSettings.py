# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class FlowPolicyLevelSettingsActivationSettings(BaseModel):
    """
    FlowPolicyLevelSettingsActivationSettings model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    matchTimes: str = Field(
        validation_alias="matchTimes",
        description="The number of times the policy level conditions must be met within the match window to activate the alert.",
    )

    matchWindow: str = Field(
        validation_alias="matchWindow",
        description="The window of time within which the policy level conditions must be met to activate the alert.",
    )

    resetCountWindow: str = Field(
        validation_alias="resetCountWindow",
        description="The window of time within which the level conditions must not be met again to reset the match count.",
    )
