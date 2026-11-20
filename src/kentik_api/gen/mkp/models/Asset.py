# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AssetReport import AssetReport


class Asset(BaseModel):
    """
    Asset
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    reports: Optional[List[Optional[AssetReport]]] = Field(
        validation_alias="reports", default=None
    )

    defaultReport: Optional[AssetReport] = Field(
        validation_alias="defaultReport", default=None
    )
