# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .JiraCloudContext import JiraCloudContext
from .ServiceNowContext import ServiceNowContext


class ExternalContext(BaseModel):
    """
    ExternalContext model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    servicenow: Optional[ServiceNowContext] = Field(
        validation_alias="servicenow", default=None
    )

    jiraCloud: Optional[JiraCloudContext] = Field(
        validation_alias="jiraCloud", default=None
    )
