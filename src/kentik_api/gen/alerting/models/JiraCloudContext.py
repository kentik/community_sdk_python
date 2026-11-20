# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class JiraCloudContext(BaseModel):
    """
    JiraCloudContext model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    issueKey: str = Field(
        validation_alias="issueKey", description="Jira Cloud issue key, e.g., KEY-123."
    )

    issueUrl: str = Field(
        validation_alias="issueUrl",
        description="Jira Cloud issue URL, e.g., https://instance.atlassian.net/browse/KEY-123.",
    )
