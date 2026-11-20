# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AlertServiceAckBody(BaseModel):
    """
    AlertServiceAckBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    comment: Optional[str] = Field(
        validation_alias="comment",
        default=None,
        description="The comment to add to the acknowledgement.",
    )
