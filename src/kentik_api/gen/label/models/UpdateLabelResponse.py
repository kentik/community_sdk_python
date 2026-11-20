# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Label import Label


class UpdateLabelResponse(BaseModel):
    """
    UpdateLabelResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    label: Optional[Label] = Field(validation_alias="label", default=None)
