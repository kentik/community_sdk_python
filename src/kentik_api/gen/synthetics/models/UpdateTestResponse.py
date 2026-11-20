# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Test import Test


class UpdateTestResponse(BaseModel):
    """
    UpdateTestResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    test: Optional[Test] = Field(validation_alias="test", default=None)
