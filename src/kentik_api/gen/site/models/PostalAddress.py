# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class PostalAddress(BaseModel):
    """
    PostalAddress
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    address: str = Field(validation_alias="address", description="Street address")

    city: str = Field(validation_alias="city", description="City (full name)")

    region: Optional[str] = Field(
        validation_alias="region", default=None, description="Geographical region"
    )

    postalCode: Optional[str] = Field(
        validation_alias="postalCode",
        default=None,
        description="Country specific postal code",
    )

    country: str = Field(
        validation_alias="country", description="Country (full name or country code)"
    )
