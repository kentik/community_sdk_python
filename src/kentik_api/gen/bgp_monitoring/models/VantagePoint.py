# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class VantagePoint(BaseModel):
    """
    VantagePoint
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dataset: Optional[str] = Field(
        validation_alias="dataset",
        default=None,
        description="Name of the collector data set",
    )

    collector: Optional[str] = Field(
        validation_alias="collector", default=None, description="Name of the collector"
    )

    peerAsn: Optional[int] = Field(
        validation_alias="peerAsn",
        default=None,
        description="ASN of the peer from which the collector receives BGP data",
    )

    peerIp: Optional[str] = Field(
        validation_alias="peerIp",
        default=None,
        description="IP address of the peer from which the collector receives BGP data",
    )
