# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Peer(BaseModel):
    """
    Peer
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

    pfxCount: Optional[int] = Field(
        validation_alias="pfxCount",
        default=None,
        description="Prefix Count (number of distinct IP address blocks announced by AS)",
    )
