# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class BatchDelete(BaseModel):
    """
    A value to delete.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    value: str = Field(
        validation_alias="value", description="The tag name, or the populator value."
    )
