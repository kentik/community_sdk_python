# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CommandResult(BaseModel):
    """
    CommandResult model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    success: Optional[bool] = Field(validation_alias="success", default=None)

    output: Optional[str] = Field(
        validation_alias="output",
        default=None,
        description="if success is false, contains error message",
    )
