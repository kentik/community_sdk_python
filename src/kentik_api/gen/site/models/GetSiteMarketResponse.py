# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SiteMarket import SiteMarket


class GetSiteMarketResponse(BaseModel):
    """
    GetSiteMarketResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    siteMarket: Optional[SiteMarket] = Field(
        validation_alias="siteMarket", default=None
    )
