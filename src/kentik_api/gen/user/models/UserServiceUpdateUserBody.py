# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict

from pydantic import BaseModel, Field


class UserServiceUpdateUserBody(BaseModel):
    """
    UpdateUserRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    user: Dict[str, Any] = Field(validation_alias="user", description="User")
