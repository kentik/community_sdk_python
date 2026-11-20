# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Threshold import Threshold


class Alert(BaseModel):
    """
    Alert
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    saved: Optional[bool] = Field(validation_alias="saved", default=None)

    policyId: Optional[str] = Field(validation_alias="policyId", default=None)

    thresholds: Optional[List[Optional[Threshold]]] = Field(
        validation_alias="thresholds", default=None
    )

    primaryMetric: Optional[str] = Field(validation_alias="primaryMetric", default=None)

    secondaryMetrics: Optional[List[str]] = Field(
        validation_alias="secondaryMetrics", default=None
    )

    isTemplate: Optional[bool] = Field(validation_alias="isTemplate", default=None)

    subpolicyId: Optional[str] = Field(validation_alias="subpolicyId", default=None)
