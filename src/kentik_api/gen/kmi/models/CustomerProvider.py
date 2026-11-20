# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CustomerProvider(BaseModel):
    """
    CustomerProvider
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asn: Optional[int] = Field(
        validation_alias="asn",
        default=None,
        description="Autonomous System Number (ASN)",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="Name of the Autonomous System",
    )

    score: Optional[int] = Field(
        validation_alias="score",
        default=None,
        description="Score of the Autonomous System",
    )

    singlehomedCustomer: Optional[bool] = Field(
        validation_alias="singlehomedCustomer",
        default=None,
        description="Singlehomed customer (only one upstream provider to the internet)",
    )

    mutualCustomer: Optional[bool] = Field(
        validation_alias="mutualCustomer", default=None, description="Mutual customer"
    )

    mutualProvider: Optional[bool] = Field(
        validation_alias="mutualProvider", default=None, description="Mutual provider"
    )
