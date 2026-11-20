# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PolicyDataSources import PolicyDataSources
from .PolicyFilters import PolicyFilters


class NmsPolicySettingsDatasetConfig(BaseModel):
    """
    NmsPolicySettingsDatasetConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    sources: Optional[PolicyDataSources] = Field(
        validation_alias="sources", default=None
    )

    filters: Optional[PolicyFilters] = Field(validation_alias="filters", default=None)

    measurements: Optional[List[str]] = Field(
        validation_alias="measurements", default=None
    )

    customDimensions: Optional[List[str]] = Field(
        validation_alias="customDimensions",
        default=None,
        description="this might be irrelevant based on policy type - only applicable if custom type",
    )
