# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SignatureAlgorithm import SignatureAlgorithm


class MessageSignature(BaseModel):
    """
    MessageSignature model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    signerId: Optional[str] = Field(validation_alias="signerId", default=None)

    algorithm: Optional[SignatureAlgorithm] = Field(
        validation_alias="algorithm", default=None
    )

    signature: Optional[str] = Field(validation_alias="signature", default=None)
