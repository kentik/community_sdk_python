# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    """
    UserInfo
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="Unique system generated ID"
    )

    email: Optional[str] = Field(
        validation_alias="email", default=None, description="E-mail address of the user"
    )

    fullName: Optional[str] = Field(
        validation_alias="fullName", default=None, description="Full name of the user"
    )
