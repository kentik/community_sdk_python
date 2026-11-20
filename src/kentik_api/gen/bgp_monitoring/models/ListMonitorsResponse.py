# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BgpMonitor import BgpMonitor


class ListMonitorsResponse(BaseModel):
    """
    ListMonitorsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    monitors: Optional[List[Optional[BgpMonitor]]] = Field(
        validation_alias="monitors",
        default=None,
        description="List of BGP monitors configured in the account",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid objects (should be always zero)",
    )
