# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class LabelConcise(BaseModel):
    """
    LabelConcise
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[int] = Field(
        validation_alias="id", default=None, description="Label ID"
    )
