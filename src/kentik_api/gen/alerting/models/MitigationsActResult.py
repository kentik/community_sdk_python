# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class MitigationsActResult(BaseModel):
    """
    MitigationsActResult model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    mitigationId: Optional[str] = Field(
        validation_alias="mitigationId",
        default=None,
        description="The ID of the mitigation that was acted upon.",
    )

    success: Optional[bool] = Field(
        validation_alias="success",
        default=None,
        description="Whether the action was successful.",
    )

    message: Optional[str] = Field(
        validation_alias="message",
        default=None,
        description="A message describing the result of the action.",
    )
