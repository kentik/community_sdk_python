# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class TokenRevoked(BaseModel):
    """
    TokenRevoked
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    revokedBy: Optional[str] = Field(
        validation_alias="revokedBy",
        default=None,
        description="who revoked the token\n\nEmail of the user who revoked the token.",
    )

    revokedAt: Optional[str] = Field(
        validation_alias="revokedAt",
        default=None,
        description="Time at which the token was revoked.",
    )
