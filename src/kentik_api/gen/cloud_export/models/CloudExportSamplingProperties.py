# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CloudExportSamplingType import CloudExportSamplingType


class CloudExportSamplingProperties(BaseModel):
    """
    CloudExportSamplingProperties model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    samplingEnabled: Optional[bool] = Field(
        validation_alias="samplingEnabled",
        default=None,
        description="Boolean indicating if sampling is used for this export.",
    )

    samplingType: Optional[CloudExportSamplingType] = Field(
        validation_alias="samplingType", default=None
    )

    samplingRate: Optional[int] = Field(
        validation_alias="samplingRate",
        default=None,
        description="Sampling rate for the export.",
    )
