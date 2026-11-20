# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .EchoRequest import EchoRequest
from .EchoResponse import EchoResponse


class ChatResponse(BaseModel):
    """
    ChatResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    messageId: Optional[str] = Field(validation_alias="messageId", default=None)

    echoRequest: Optional[EchoRequest] = Field(
        validation_alias="echoRequest", default=None
    )

    echoResponse: Optional[EchoResponse] = Field(
        validation_alias="echoResponse", default=None
    )
