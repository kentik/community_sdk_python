# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SecretType import SecretType


class Secret(BaseModel):
    """
    Secret
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: str = Field(validation_alias="name", description="The secret's name")

    value: str = Field(
        validation_alias="value", description="The secret's actual value"
    )

    version: int = Field(validation_alias="version", description="The secret's version")

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Purpose of this secret",
    )

    type: Optional[SecretType] = Field(validation_alias="type", default=None)

    id: str = Field(validation_alias="id", description="The secret's identifier")
