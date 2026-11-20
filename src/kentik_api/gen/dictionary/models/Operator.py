# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Operator(BaseModel):
    """
    An individual filter operator (e.g. "equals", "contains").
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    key: Optional[str] = Field(
        validation_alias="key", default=None, description="Operator key"
    )

    label: Optional[str] = Field(
        validation_alias="label", default=None, description="Operator display label"
    )
