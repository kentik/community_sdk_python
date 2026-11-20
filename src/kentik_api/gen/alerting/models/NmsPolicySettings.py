# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .NmsPolicySettingsDatasetConfig import NmsPolicySettingsDatasetConfig
from .NmsPolicySettingsEvaluationConfig import NmsPolicySettingsEvaluationConfig


class NmsPolicySettings(BaseModel):
    """
    NmsPolicySettings model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dataset: Optional[NmsPolicySettingsDatasetConfig] = Field(
        validation_alias="dataset", default=None
    )

    evaluation: Optional[NmsPolicySettingsEvaluationConfig] = Field(
        validation_alias="evaluation", default=None
    )
