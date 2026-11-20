# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .Label import Label


class CreateLabelRequest(BaseModel):
    """
    CreateLabelRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    label: Label = Field(validation_alias="label")
