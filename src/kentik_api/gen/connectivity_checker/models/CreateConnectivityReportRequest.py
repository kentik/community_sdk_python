# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CloudProvider import CloudProvider
from .EntityType import EntityType


class CreateConnectivityReportRequest(BaseModel):
    """
    CreateConnectivityReportRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    cloudProvider: CloudProvider = Field(validation_alias="cloudProvider")

    src: str = Field(validation_alias="src", description="Source")

    dst: str = Field(validation_alias="dst", description="Destination")

    dstPort: str = Field(validation_alias="dstPort", description="Destination Port")

    protocol: str = Field(validation_alias="protocol", description="Protocol")

    srcType: Optional[EntityType] = Field(validation_alias="srcType", default=None)

    dstType: Optional[EntityType] = Field(validation_alias="dstType", default=None)

    startTime: str = Field(
        validation_alias="startTime",
        description="Start Timestamp (UTC) which defines the time range for the report.",
    )

    endTime: str = Field(
        validation_alias="endTime",
        description="End timestamp (UTC) which defines the time range for the report.",
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Report Name"
    )
