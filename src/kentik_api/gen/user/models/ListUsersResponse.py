# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .User import User


class ListUsersResponse(BaseModel):
    """
    ListUsersResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    users: Optional[List[Optional[User]]] = Field(
        validation_alias="users",
        default=None,
        description="Last of users in the account",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
