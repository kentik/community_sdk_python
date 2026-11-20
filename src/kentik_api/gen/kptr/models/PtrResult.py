# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class PtrResult(BaseModel):
    """
    PtrResult model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    address: Optional[str] = Field(validation_alias="address", default=None)

    answer: Optional[str] = Field(validation_alias="answer", default=None)

    error: Optional[str] = Field(validation_alias="error", default=None)

    ttl: Optional[int] = Field(validation_alias="ttl", default=None)

    resolverIp: Optional[str] = Field(validation_alias="resolverIp", default=None)
