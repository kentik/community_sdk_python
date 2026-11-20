# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Status import Status


class CostProviderSummary(BaseModel):
    """
    CostProviderSummary
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    date: Optional[str] = Field(
        validation_alias="date",
        default=None,
        description="Date of the cost provider summary (YYYY-MM)",
    )

    status: Optional[Status] = Field(validation_alias="status", default=None)

    totalCost: Optional[float] = Field(
        validation_alias="totalCost",
        default=None,
        description="Total cost of the cost provider",
    )

    totalCostVariation: Optional[str] = Field(
        validation_alias="totalCostVariation",
        default=None,
        description="Total cost percent variation of the cost provider (percentage changed vs the previous month)",
    )

    totalCostGroupAdditionalCost: Optional[float] = Field(
        validation_alias="totalCostGroupAdditionalCost",
        default=None,
        description="Total cost group additional cost of the cost provider",
    )

    totalCostGroupAdditionalInterfaceCost: Optional[float] = Field(
        validation_alias="totalCostGroupAdditionalInterfaceCost",
        default=None,
        description="Total cost group additional interface cost of the cost provider",
    )

    currency: Optional[str] = Field(
        validation_alias="currency",
        default=None,
        description="Currency (ISO 4217) used for cost values of the cost provider",
    )

    costPerMbps: Optional[float] = Field(
        validation_alias="costPerMbps",
        default=None,
        description="Cost per mbps (million bits per second) of the cost provider",
    )

    costPerMbpsVariation: Optional[str] = Field(
        validation_alias="costPerMbpsVariation",
        default=None,
        description="Cost per mbps percent variation of the cost provider (percentage changed vs the previous month)",
    )

    providerName: Optional[str] = Field(
        validation_alias="providerName",
        default=None,
        description="Provider name of the cost provider",
    )

    costGroupName: Optional[str] = Field(
        validation_alias="costGroupName",
        default=None,
        description="Cost group name of the cost provider",
    )

    costGroupConnType: Optional[str] = Field(
        validation_alias="costGroupConnType",
        default=None,
        description="Cost group connection type of the cost provider",
    )

    siteName: Optional[str] = Field(
        validation_alias="siteName",
        default=None,
        description="Site name of the cost provider",
    )

    siteMarket: Optional[str] = Field(
        validation_alias="siteMarket",
        default=None,
        description="Site market of the cost provider",
    )

    ingressTrafficMbps: Optional[float] = Field(
        validation_alias="ingressTrafficMbps",
        default=None,
        description="Ingress traffic mbps (million bits per second) of the cost provider",
    )

    ingressTrafficVariation: Optional[str] = Field(
        validation_alias="ingressTrafficVariation",
        default=None,
        description="Ingress traffic percent variation of the cost provider (percentage changed vs the previous month)",
    )

    egressTrafficMbps: Optional[float] = Field(
        validation_alias="egressTrafficMbps",
        default=None,
        description="Egress traffic mbps (million bits per second) of the cost provider",
    )

    egressTrafficVariation: Optional[str] = Field(
        validation_alias="egressTrafficVariation",
        default=None,
        description="Egress traffic percent variation of the cost provider (percentage changed vs the previous month)",
    )
