# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class GceProperties(BaseModel):
    """
    GceProperties
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    project: str = Field(
        validation_alias="project",
        description="Name of the project from which to export flow logs.",
    )

    subscription: Optional[str] = Field(
        validation_alias="subscription",
        default=None,
        description="GCP Pub/Sub subscription providing flow logs.",
    )

    metadataOnly: Optional[bool] = Field(
        validation_alias="metadataOnly",
        default=None,
        description="Import only metadata without any flows (default false).",
    )

    collectFlowLogs: Optional[bool] = Field(
        validation_alias="collectFlowLogs",
        default=None,
        description="Import metadata and collect flow logs (default true).",
    )

    collectMetrics: Optional[bool] = Field(
        validation_alias="collectMetrics",
        default=None,
        description="Import metadata and collect metrics data.  Note that flow logs will still be collected unless metadata_only is also set to true. (default false).",
    )
