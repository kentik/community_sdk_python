# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class V5Error(BaseModel):
    """
    The error body of a V5 call.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    error: Optional[str] = Field(
        validation_alias="error", default=None, description="The error message."
    )

    errorxid: Optional[str] = Field(
        validation_alias="errorxid",
        default=None,
        description="The error ID to give Kentik support.",
    )
