# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class NmsPolicySettingsEvaluationConfig(BaseModel):
    """
    NmsPolicySettingsEvaluationConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    activationDelay: Optional[str] = Field(
        validation_alias="activationDelay", default=None
    )

    clearanceDelay: Optional[str] = Field(
        validation_alias="clearanceDelay", default=None
    )
