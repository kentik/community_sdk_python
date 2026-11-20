# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ScopeConfig import ScopeConfig


class Scope(BaseModel):
    """
    Scope
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier for the Focus Scope.",
    )

    name: str = Field(
        validation_alias="name",
        description="A unique name for the Focus Scope within the company.",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="The Focus Scope's description.",
    )

    scope: Optional[ScopeConfig] = Field(validation_alias="scope", default=None)

    createdBy: Optional[str] = Field(
        validation_alias="createdBy",
        default=None,
        description="Identifier of the user who created the Focus Scope.",
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="Date-time of scope creation, in UTC.",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="Date-time of most-recent scope edit, in UTC.",
    )
