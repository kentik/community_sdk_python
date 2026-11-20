# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowContextSiteDetails(BaseModel):
    """
    FlowContextSiteDetails model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="The ID of the site."
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="The name of the site."
    )

    latitude: Optional[str] = Field(
        validation_alias="latitude",
        default=None,
        description="The geographic latitude of the site.",
    )

    longitude: Optional[str] = Field(
        validation_alias="longitude",
        default=None,
        description="The geographic longitude of the site.",
    )

    location: Optional[str] = Field(
        validation_alias="location",
        default=None,
        description="The location of the site (e.g. 'New York, NY').",
    )

    country: Optional[str] = Field(
        validation_alias="country",
        default=None,
        description="The country of the site (e.g. 'United States').",
    )
