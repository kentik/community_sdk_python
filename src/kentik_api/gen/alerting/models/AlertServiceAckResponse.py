# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Alert import Alert


class AlertServiceAckResponse(BaseModel):
    """
    AlertServiceAckResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    alert: Optional[Alert] = Field(validation_alias="alert", default=None)
