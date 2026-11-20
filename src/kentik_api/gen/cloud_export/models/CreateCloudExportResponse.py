# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CloudExport import CloudExport


class CreateCloudExportResponse(BaseModel):
    """
    CreateCloudExportResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    export: Optional[CloudExport] = Field(validation_alias="export", default=None)
