# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class SiteMarket(BaseModel):
    """
    SiteMarket
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="System generated unique identifier",
    )

    name: str = Field(validation_alias="name", description="User selected unique name")

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Free-form description",
    )

    numberOfSites: Optional[int] = Field(
        validation_alias="numberOfSites",
        default=None,
        description="Number of sites in this market",
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )
