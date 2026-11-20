# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CreatedBy(BaseModel):
    """
    CreatedBy
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="User id"
    )

    email: Optional[str] = Field(
        validation_alias="email", default=None, description="User email"
    )

    fullName: Optional[str] = Field(
        validation_alias="fullName", default=None, description="User full name"
    )
