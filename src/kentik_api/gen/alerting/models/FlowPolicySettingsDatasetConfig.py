# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PolicyDataSources import PolicyDataSources
from .PolicyFilters import PolicyFilters


class FlowPolicySettingsDatasetConfig(BaseModel):
    """
    FlowPolicySettingsDatasetConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    sources: Optional[PolicyDataSources] = Field(
        validation_alias="sources", default=None
    )

    filters: Optional[PolicyFilters] = Field(validation_alias="filters", default=None)

    dimensions: List[str] = Field(
        validation_alias="dimensions",
        description="The dimensions of the policy used to create alert keys for activated alerts.",
    )

    metrics: List[str] = Field(
        validation_alias="metrics",
        description="The metrics of the dataset that can be used for policy threshold conditions. Metrics are also provided with the activated alert context information",
    )
