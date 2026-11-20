# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class ScheduleSettings(BaseModel):
    """
    ScheduleSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    enabled: Optional[bool] = Field(
        validation_alias="enabled",
        default=None,
        description="Boolean indicating an (dis|en)abled schedule",
    )

    start: Optional[int] = Field(
        validation_alias="start",
        default=None,
        description="UTC unix timestamps indicating the start of the schedule",
    )

    end: Optional[int] = Field(
        validation_alias="end",
        default=None,
        description="UTC unix timestamp indicating the end of the schedule",
    )
