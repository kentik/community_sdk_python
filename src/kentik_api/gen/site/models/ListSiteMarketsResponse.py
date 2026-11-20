# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .SiteMarket import SiteMarket


class ListSiteMarketsResponse(BaseModel):
    """
    ListSiteMarketsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    siteMarkets: Optional[List[Optional[SiteMarket]]] = Field(
        validation_alias="siteMarkets",
        default=None,
        description="List of configurations of requested site markets",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
