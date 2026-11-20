# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowPolicySettingsBaselineConfig import FlowPolicySettingsBaselineConfig
from .FlowPolicySettingsDatasetConfig import FlowPolicySettingsDatasetConfig
from .FlowPolicySettingsEvaluationConfig import FlowPolicySettingsEvaluationConfig


class FlowPolicySettings(BaseModel):
    """
    FlowPolicySettings model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dataset: Optional[FlowPolicySettingsDatasetConfig] = Field(
        validation_alias="dataset", default=None
    )

    evaluation: Optional[FlowPolicySettingsEvaluationConfig] = Field(
        validation_alias="evaluation", default=None
    )

    baseline: Optional[FlowPolicySettingsBaselineConfig] = Field(
        validation_alias="baseline", default=None
    )
