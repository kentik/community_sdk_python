# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AzureProperties(BaseModel):
    """
    AzureProperties
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    location: str = Field(
        validation_alias="location",
        description="Azure region/location from which to export flow logs.",
    )

    resourceGroup: str = Field(
        validation_alias="resourceGroup",
        description="Resource group containing the NSG generating flow logs.",
    )

    storageAccount: str = Field(
        validation_alias="storageAccount",
        description="Storage account from which flow logs are to be extracted.",
    )

    subscriptionId: str = Field(
        validation_alias="subscriptionId",
        description="ID of Azure account from which flows logs are to be exported.",
    )

    securityPrincipalEnabled: Optional[bool] = Field(
        validation_alias="securityPrincipalEnabled",
        default=None,
        description="Indication whether security principal for the Kentik flow export application has been authorized.",
    )
