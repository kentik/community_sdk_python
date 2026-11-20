# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class EchoRequest(BaseModel):
    """
    EchoRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    message: Optional[str] = Field(validation_alias="message", default=None)
