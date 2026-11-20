# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Secret import Secret


class GetSecretResponse(BaseModel):
    """
    GetSecretResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    secret: Optional[Secret] = Field(validation_alias="secret", default=None)
