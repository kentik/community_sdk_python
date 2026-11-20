# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """
    Comment model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The unique identifier of the comment.",
    )

    text: Optional[str] = Field(
        validation_alias="text",
        default=None,
        description="The text content of the comment.",
    )

    userId: Optional[str] = Field(
        validation_alias="userId",
        default=None,
        description="The ID of the user who created the comment.",
    )

    userName: Optional[str] = Field(
        validation_alias="userName",
        default=None,
        description="The username of the user who created the comment.",
    )

    userFullName: Optional[str] = Field(
        validation_alias="userFullName",
        default=None,
        description="The full name of the user who created the comment.",
    )

    userEmail: Optional[str] = Field(
        validation_alias="userEmail",
        default=None,
        description="The email of the user who created the comment.",
    )

    createdAt: Optional[str] = Field(
        validation_alias="createdAt",
        default=None,
        description="The timestamp when the comment was created.",
    )
