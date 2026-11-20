# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .NmsStateChangeCondition import NmsStateChangeCondition
from .NmsStateSet import NmsStateSet
from .NmsThresholdCondition import NmsThresholdCondition


class NmsCondition(BaseModel):
    """
    NmsCondition model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    measurement: Optional[str] = Field(validation_alias="measurement", default=None)

    metric: Optional[str] = Field(validation_alias="metric", default=None)

    threshold: Optional[NmsThresholdCondition] = Field(
        validation_alias="threshold", default=None
    )

    stateChange: Optional[NmsStateChangeCondition] = Field(
        validation_alias="stateChange", default=None
    )

    stateInCondition: Optional[NmsStateSet] = Field(
        validation_alias="stateInCondition", default=None
    )
