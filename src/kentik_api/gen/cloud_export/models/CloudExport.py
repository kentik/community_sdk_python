# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AwsProperties import AwsProperties
from .AzureProperties import AzureProperties
from .CloudExportSamplingProperties import CloudExportSamplingProperties
from .CloudExportStatus import CloudExportStatus
from .CloudExportType import CloudExportType
from .CloudProvider import CloudProvider
from .GceProperties import GceProperties
from .OciProperties import OciProperties


class CloudExport(BaseModel):
    """
    CloudExport
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier of the instance",
    )

    type: Optional[CloudExportType] = Field(validation_alias="type", default=None)

    enabled: bool = Field(
        validation_alias="enabled",
        description="Attribute controlling whether the instance is active",
    )

    name: str = Field(
        validation_alias="name", description="User selected name of the instance"
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Description of the instance",
    )

    planId: str = Field(
        validation_alias="planId",
        description="Identifier of the billing plan for the instance",
    )

    cloudProvider: CloudProvider = Field(validation_alias="cloudProvider")

    aws: Optional[AwsProperties] = Field(validation_alias="aws", default=None)

    azure: Optional[AzureProperties] = Field(validation_alias="azure", default=None)

    gce: Optional[GceProperties] = Field(validation_alias="gce", default=None)

    oci: Optional[OciProperties] = Field(validation_alias="oci", default=None)

    currentStatus: Optional[CloudExportStatus] = Field(
        validation_alias="currentStatus", default=None
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )

    sampling: Optional[CloudExportSamplingProperties] = Field(
        validation_alias="sampling", default=None
    )
