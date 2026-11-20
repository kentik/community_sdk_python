# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .Test import Test


class CreateTestRequest(BaseModel):
    """
    CreateTestRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    test: Test = Field(validation_alias="test")
