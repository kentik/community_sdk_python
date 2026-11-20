# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .BaselineConditionDeltaType import BaselineConditionDeltaType


class ConditionsBaselineCondition(BaseModel):
    """
    ConditionsBaselineCondition model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    absolute: Optional[float] = Field(
        validation_alias="absolute",
        default=None,
        description="The absolute value used for the policy level condition.",
    )

    percentage: Optional[str] = Field(
        validation_alias="percentage",
        default=None,
        description="The percentage value used for the policy level condition.",
    )

    delta: BaselineConditionDeltaType = Field(validation_alias="delta")

    useLowest: Optional[bool] = Field(
        validation_alias="useLowest",
        default=None,
        description="Use the lowest value for the policy level condition if valid baseline value is missing.",
    )

    useHighest: Optional[bool] = Field(
        validation_alias="useHighest",
        default=None,
        description="Use the highest value for the policy level condition if valid baseline value is missing.",
    )

    useTrigger: Optional[bool] = Field(
        validation_alias="useTrigger",
        default=None,
        description="Use the trigger value for the policy level condition if valid baseline value is missing.",
    )

    skip: Optional[bool] = Field(
        validation_alias="skip",
        default=None,
        description="Skip the current traffic value if valid baseline value is missing.",
    )

    useValue: Optional[str] = Field(
        validation_alias="useValue",
        default=None,
        description="Use the given value for the policy level condition if valid baseline value is missing.",
    )
