# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    """
    Location
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    latitude: Optional[float] = Field(
        validation_alias="latitude",
        default=None,
        description="Latitude in signed decimal degrees",
    )

    longitude: Optional[float] = Field(
        validation_alias="longitude",
        default=None,
        description="Longitude in signed decimal degrees",
    )

    country: Optional[str] = Field(
        validation_alias="country", default=None, description="Country of the location"
    )

    region: Optional[str] = Field(
        validation_alias="region",
        default=None,
        description="Geographic region within the country",
    )

    city: Optional[str] = Field(
        validation_alias="city", default=None, description="City of the location"
    )
