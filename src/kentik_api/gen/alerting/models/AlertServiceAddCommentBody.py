# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class AlertServiceAddCommentBody(BaseModel):
    """
    AlertServiceAddCommentBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    text: str = Field(
        validation_alias="text",
        description="The text content of the comment. Maximum length is 5000 characters.",
    )
