# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class CreateChatSessionRequest(BaseModel):
    """
    CreateChatSessionRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    prompt: str = Field(validation_alias="prompt", description="The user question")
