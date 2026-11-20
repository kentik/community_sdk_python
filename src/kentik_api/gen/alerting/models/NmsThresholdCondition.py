# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .NmsConditionOperator import NmsConditionOperator


class NmsThresholdCondition(BaseModel):
    """
    NmsThresholdCondition model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    operator: Optional[NmsConditionOperator] = Field(
        validation_alias="operator", default=None
    )

    conditionValue: Optional[str] = Field(
        validation_alias="conditionValue", default=None
    )
