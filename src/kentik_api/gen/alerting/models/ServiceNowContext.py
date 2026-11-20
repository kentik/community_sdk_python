# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class ServiceNowContext(BaseModel):
    """
    ServiceNowContext model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    incidentId: str = Field(
        validation_alias="incidentId",
        description="Incident ID associated with incoming Kentik alert, e.g., INC0012345.",
    )

    incidentUrl: str = Field(
        validation_alias="incidentUrl",
        description="Incident URL, e.g. https://instance.service-now.com/...",
    )
