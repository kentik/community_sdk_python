# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CloudExportStatus(BaseModel):
    """
    CloudExportStatus
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    status: Optional[str] = Field(
        validation_alias="status",
        default=None,
        description="Status of the export task.",
    )

    errorMessage: Optional[str] = Field(
        validation_alias="errorMessage",
        default=None,
        description="Text of the last error message (empty if status is OK).",
    )

    flowFound: Optional[bool] = Field(
        validation_alias="flowFound",
        default=None,
        description="Indication whether any flow data were exported.",
    )

    apiAccess: Optional[bool] = Field(
        validation_alias="apiAccess",
        default=None,
        description="Indication whether the export process is able to access cloud API.",
    )

    storageAccountAccess: Optional[bool] = Field(
        validation_alias="storageAccountAccess",
        default=None,
        description="Indication whether the export process is able to access storage account containing flow logs.",
    )
