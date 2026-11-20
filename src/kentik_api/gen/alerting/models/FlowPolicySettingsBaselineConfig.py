# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .AggregationType import AggregationType
from .BaselineConfigCompareMode import BaselineConfigCompareMode


class FlowPolicySettingsBaselineConfig(BaseModel):
    """
    FlowPolicySettingsBaselineConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    storedKeyCount: str = Field(
        validation_alias="storedKeyCount",
        description="not exposing completeness duration as this does not work\n\nThe number of alert keys stored in the baseline per policy window.",
    )

    windowLength: str = Field(
        validation_alias="windowLength",
        description="The length of the entire policy baseline window.",
    )

    windowStartOffset: str = Field(
        validation_alias="windowStartOffset",
        description="The start offset from now used when calculating the baseline value.",
    )

    rollupAggregation: AggregationType = Field(validation_alias="rollupAggregation")

    compareMode: BaselineConfigCompareMode = Field(validation_alias="compareMode")

    neighbourhoodRadius: str = Field(
        validation_alias="neighbourhoodRadius",
        description="The neighbourhood radius used to calculate the neighbourhood value. This is the number of hours before and after the current hour to include in the neighbourhood value calculation.",
    )

    neighbourhoodAggregation: AggregationType = Field(
        validation_alias="neighbourhoodAggregation"
    )

    finalAggregation: AggregationType = Field(validation_alias="finalAggregation")
