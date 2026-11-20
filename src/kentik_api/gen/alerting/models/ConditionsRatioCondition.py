# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .RatioConditionDirection import RatioConditionDirection


class ConditionsRatioCondition(BaseModel):
    """
    ConditionsRatioCondition model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    lhsMetric: str = Field(
        validation_alias="lhsMetric",
        description="The left hand side metric used for the policy level condition.",
    )

    rhsMetric: str = Field(
        validation_alias="rhsMetric",
        description="The right hand side metric used for the policy level condition.",
    )

    lhsProportion: int = Field(
        validation_alias="lhsProportion",
        description="The left hand side proportion used for the policy level condition.",
    )

    rhsProportion: int = Field(
        validation_alias="rhsProportion",
        description="The right hand side proportion used for the policy level condition.",
    )

    margin: float = Field(
        validation_alias="margin",
        description="The margin used for the policy level condition.",
    )

    direction: RatioConditionDirection = Field(validation_alias="direction")
