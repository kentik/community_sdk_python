# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .protobufAny import protobufAny


class googlerpcStatus(BaseModel):
    """
    googlerpcStatus model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    code: Optional[int] = Field(validation_alias="code", default=None)

    message: Optional[str] = Field(validation_alias="message", default=None)

    details: Optional[List[Optional[protobufAny]]] = Field(
        validation_alias="details", default=None
    )
