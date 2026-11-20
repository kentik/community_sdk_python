# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Nlri import Nlri


class BgpMetric(BaseModel):
    """
    BgpMetric
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    timestamp: Optional[str] = Field(
        validation_alias="timestamp",
        default=None,
        description="UTC time of the observation",
    )

    nlri: Optional[Nlri] = Field(validation_alias="nlri", default=None)

    reachability: Optional[float] = Field(
        validation_alias="reachability",
        default=None,
        description="Percentage of vantage points reporting the prefix reachable",
    )

    pathChanges: Optional[int] = Field(
        validation_alias="pathChanges",
        default=None,
        description="Number of AS path changes for the prefix across all vantage points in the queried time interval",
    )
