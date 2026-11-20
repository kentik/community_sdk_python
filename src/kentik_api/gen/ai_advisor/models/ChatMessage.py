# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SessionStatus import SessionStatus


class ChatMessage(BaseModel):
    """
    ChatMessage
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The unique identifier (UUID) for the message",
    )

    status: Optional[SessionStatus] = Field(validation_alias="status", default=None)

    finalAnswer: Optional[str] = Field(validation_alias="finalAnswer", default=None)

    reasoning: Optional[str] = Field(validation_alias="reasoning", default=None)

    data: Optional[str] = Field(validation_alias="data", default=None)

    errorMessage: Optional[str] = Field(validation_alias="errorMessage", default=None)

    createdAt: Optional[str] = Field(validation_alias="createdAt", default=None)

    updatedAt: Optional[str] = Field(validation_alias="updatedAt", default=None)

    prompt: Optional[str] = Field(validation_alias="prompt", default=None)
