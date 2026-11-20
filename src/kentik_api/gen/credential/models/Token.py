# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Token
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    key: str = Field(
        validation_alias="key",
        description="Credential key within the group, e.g. `username`",
    )

    value: Optional[str] = Field(
        validation_alias="value",
        default=None,
        description="Secret value. On update, an empty value keeps the existing secret.",
    )
