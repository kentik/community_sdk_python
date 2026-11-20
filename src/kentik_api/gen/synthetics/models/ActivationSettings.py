# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class ActivationSettings(BaseModel):
    """
    ActivationSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    gracePeriod: Optional[str] = Field(
        validation_alias="gracePeriod",
        default=None,
        description="Period of healthy status in minutes within the time window not cancelling alarm activation",
    )

    timeUnit: Optional[str] = Field(
        validation_alias="timeUnit",
        default=None,
        description="Time unit for specifying time window (m | h)",
    )

    timeWindow: Optional[str] = Field(
        validation_alias="timeWindow",
        default=None,
        description="Time window for evaluating of test for alarm activation",
    )

    times: Optional[str] = Field(
        validation_alias="times",
        default=None,
        description="Number of occurrences of unhealthy test status within the time window triggering alarm activation",
    )
