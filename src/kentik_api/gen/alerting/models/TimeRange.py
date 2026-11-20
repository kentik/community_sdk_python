# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class TimeRange(BaseModel):
    """
    TimeRange model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    start: Optional[str] = Field(validation_alias="start", default=None)

    end: Optional[str] = Field(validation_alias="end", default=None)
