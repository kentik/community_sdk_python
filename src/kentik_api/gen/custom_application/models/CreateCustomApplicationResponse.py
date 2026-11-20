# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CustomApplication import CustomApplication


class CreateCustomApplicationResponse(BaseModel):
    """
    CreateCustomApplicationResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    application: Optional[CustomApplication] = Field(
        validation_alias="application", default=None
    )
