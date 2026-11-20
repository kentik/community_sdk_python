# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowTest(BaseModel):
    """
    FlowTest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    target: Optional[str] = Field(
        validation_alias="target",
        default=None,
        description="Target ASN, CDN, Country, Region of City for autonomous test (type of value depends on flow test sub-type)",
    )

    targetRefreshIntervalMillis: Optional[int] = Field(
        validation_alias="targetRefreshIntervalMillis",
        default=None,
        description="Period (in milliseconds) for refreshing list of targets based on available flow data",
    )

    maxProviders: Optional[int] = Field(
        validation_alias="maxProviders",
        default=None,
        description="Maximum number of IP providers to track autonomously",
    )

    maxIpTargets: Optional[int] = Field(
        validation_alias="maxIpTargets",
        default=None,
        description="Maximum number of target IP addresses to select based flow data query",
    )

    type: Optional[str] = Field(
        validation_alias="type",
        default=None,
        description="Autonomous test sub-type (asn | cdn | country | region | city)",
    )

    inetDirection: Optional[str] = Field(
        validation_alias="inetDirection",
        default=None,
        description="Selection of address from flow data (src = source address in inbound flows | dst = destination addresses in outbound flows)",
    )

    direction: Optional[str] = Field(
        validation_alias="direction",
        default=None,
        description="Direction of flows to match target attribute for extraction of target addresses (src | dst)",
    )
