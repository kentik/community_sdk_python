# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CloudExport import CloudExport


class ListCloudExportsResponse(BaseModel):
    """
    ListCloudExportsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    exports: Optional[List[Optional[CloudExport]]] = Field(
        validation_alias="exports",
        default=None,
        description="List of cloud export objects.",
    )

    invalidExportsCount: Optional[int] = Field(
        validation_alias="invalidExportsCount",
        default=None,
        description="Number of objects with invalid data (which are not returned in the response).",
    )
