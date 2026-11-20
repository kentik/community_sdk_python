# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .User import User


class CreateUserRequest(BaseModel):
    """
    CreateUserRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    user: User = Field(validation_alias="user")
