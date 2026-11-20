# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AlertServiceSetExternalContextResponse(BaseModel):
    """
    AlertServiceSetExternalContextResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    updatedAt: Optional[str] = Field(
        validation_alias="updatedAt",
        default=None,
        description="Timestamp of external context update.",
    )
