# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Site(BaseModel):
    """
    Site
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="Site ID"
    )

    siteName: Optional[str] = Field(
        validation_alias="siteName", default=None, description="Site name"
    )

    lat: Optional[float] = Field(
        validation_alias="lat", default=None, description="Site latitude"
    )

    lon: Optional[float] = Field(
        validation_alias="lon", default=None, description="Site longitude"
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId", default=None, description="Company ID"
    )
