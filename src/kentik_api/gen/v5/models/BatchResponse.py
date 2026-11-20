# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class BatchResponse(BaseModel):
    """
    The answer to one batch part.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    message: Optional[str] = Field(
        validation_alias="message", default=None, description="A status message."
    )

    guid: Optional[str] = Field(
        validation_alias="guid",
        default=None,
        description="The batch ID. Send it in every later part, and use it for batch_status.",
    )
