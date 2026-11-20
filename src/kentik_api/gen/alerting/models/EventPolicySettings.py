# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .EventPolicySettingsEventType import EventPolicySettingsEventType
from .PolicyFilters import PolicyFilters


class EventPolicySettings(BaseModel):
    """
    EventPolicySettings model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: EventPolicySettingsEventType = Field(validation_alias="type")

    dimensions: List[str] = Field(
        validation_alias="dimensions",
        description="The dimensions of the event to trigger the policy.",
    )

    filters: Optional[PolicyFilters] = Field(validation_alias="filters", default=None)
