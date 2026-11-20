# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .SiteMarket import SiteMarket


class CreateSiteMarketRequest(BaseModel):
    """
    CreateSiteMarketRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    siteMarket: SiteMarket = Field(validation_alias="siteMarket")
