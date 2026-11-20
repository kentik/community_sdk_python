# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CommandResult import CommandResult


class ExecuteCommandResponse(BaseModel):
    """
    ExecuteCommandResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    commandResult: Optional[CommandResult] = Field(
        validation_alias="commandResult", default=None
    )
