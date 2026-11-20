# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class PeeringDBSiteMapping(BaseModel):
    """
    PeeringDBSiteMapping model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: str = Field(validation_alias="id", description="Peering DB id")

    siteId: str = Field(validation_alias="siteId", description="Peering DB site id")

    peeringdbFacId: str = Field(
        validation_alias="peeringdbFacId", description="Peering DB facility id"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId", default=None, description="Company ID"
    )
