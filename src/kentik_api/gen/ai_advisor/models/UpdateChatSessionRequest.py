# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class UpdateChatSessionRequest(BaseModel):
    """
    UpdateChatSessionRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    prompt: str = Field(validation_alias="prompt", description="The user question")

    id: str = Field(
        validation_alias="id",
        description="The unique identifier (UUID) for the chat session",
    )
