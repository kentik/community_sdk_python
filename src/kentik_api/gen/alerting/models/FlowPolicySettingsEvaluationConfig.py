# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class FlowPolicySettingsEvaluationConfig(BaseModel):
    """
    FlowPolicySettingsEvaluationConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    frequency: str = Field(
        validation_alias="frequency",
        description="The frequency of the policy evaluation, also known as the policy window length.",
    )

    keyCount: str = Field(
        validation_alias="keyCount",
        description="The number of alert keys tracked per policy window.",
    )
