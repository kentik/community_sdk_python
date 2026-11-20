# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class KmiServiceGetASNDetailsBody(BaseModel):
    """
    GetASNDetailsRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ip: Optional[str] = Field(
        validation_alias="ip",
        default=None,
        description="IP Address Family ('v4' or 'v6'). Defaults to 'v4'.",
    )

    mutualProvider: Optional[str] = Field(
        validation_alias="mutualProvider",
        default=None,
        description="Filter by mutual provider ('all', 'only', 'exclude'). Defaults to 'all'.",
    )

    mutualCustomer: Optional[str] = Field(
        validation_alias="mutualCustomer",
        default=None,
        description="Filter by mutual customer ('all', 'only', 'exclude'). Defaults to 'all'.",
    )

    singlehomedCustomer: Optional[str] = Field(
        validation_alias="singlehomedCustomer",
        default=None,
        description="Filter by singlehomed customer ('all', 'only', 'exclude'). Defaults to 'all'.",
    )
