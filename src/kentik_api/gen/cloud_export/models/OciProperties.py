# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class OciProperties(BaseModel):
    """
    OciProperties
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ociUserId: Optional[str] = Field(
        validation_alias="ociUserId",
        default=None,
        description="ID of the user created to represent the Kentik cloud export tool.",
    )

    ociTenancyId: str = Field(
        validation_alias="ociTenancyId", description="OCI Tenancy details."
    )

    ociCompartmentId: Optional[List[str]] = Field(
        validation_alias="ociCompartmentId",
        default=None,
        description="Compartment IDs from which to collect metadata.",
    )

    ociDefaultRegion: str = Field(
        validation_alias="ociDefaultRegion",
        description="Default Enabled Region from which to collect metadata.",
    )

    ociCollectFlowLogs: Optional[bool] = Field(
        validation_alias="ociCollectFlowLogs",
        default=None,
        description="Import metadata and collect flow logs (default true).",
    )

    ociBucketName: Optional[str] = Field(
        validation_alias="ociBucketName",
        default=None,
        description="Name of the bucket from which flow logs are to be extracted.  Required if collecting flow logs (default)",
    )

    ociBucketNamespaceName: Optional[str] = Field(
        validation_alias="ociBucketNamespaceName",
        default=None,
        description="Namespace of the bucket from which flow logs are to be extracted.  Required if collecting flow logs (default)",
    )

    ociServiceConnectorOcid: Optional[str] = Field(
        validation_alias="ociServiceConnectorOcid", default=None
    )

    ociFlowObjectNamePrefix: Optional[str] = Field(
        validation_alias="ociFlowObjectNamePrefix",
        default=None,
        description="We will look for files in the bucket whose names start with {%prefix%}/{%service_connector_ocid%}",
    )

    metadataOnly: Optional[bool] = Field(
        validation_alias="metadataOnly",
        default=None,
        description="Import only metadata without any flows (default false).",
    )
