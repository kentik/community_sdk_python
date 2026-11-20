# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .User import User


class GetUserResponse(BaseModel):
    """
    GetUserResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    user: Optional[User] = Field(validation_alias="user", default=None)
