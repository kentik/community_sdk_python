# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class ServiceNowConfig(BaseModel):
    """
    ServiceNowConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier for the ServiceNow configuration.",
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId",
        default=None,
        description="Company ID that owns this configuration.",
    )

    name: str = Field(
        validation_alias="name",
        description="Human-readable name for this ServiceNow configuration.",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Optional description of this configuration.",
    )

    deviceStagingTableName: Optional[str] = Field(
        validation_alias="deviceStagingTableName",
        default=None,
        description="ServiceNow staging table name for device data import.",
    )

    pushFrequencySeconds: Optional[int] = Field(
        validation_alias="pushFrequencySeconds",
        default=None,
        description="Frequency in seconds at which data is pushed to ServiceNow.",
    )

    proxyAgentId: Optional[str] = Field(
        validation_alias="proxyAgentId",
        default=None,
        description="ID of the proxy agent used for ServiceNow connectivity.",
    )

    credentialVaultName: Optional[str] = Field(
        validation_alias="credentialVaultName",
        default=None,
        description="Name of the credential vault entry containing ServiceNow authentication. Always resolves to the latest version of this name.",
    )

    enabled: Optional[bool] = Field(
        validation_alias="enabled",
        default=None,
        description="Whether this configuration is actively polling and pushing.",
    )

    apiUrl: str = Field(
        validation_alias="apiUrl",
        description="Base URL of the ServiceNow instance (e.g. https://instance.service-now.com).",
    )
