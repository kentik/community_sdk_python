# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class SummaryStatusUtilStatus(BaseModel):
    """
    UtilStatus
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    status: Optional[str] = Field(
        validation_alias="status", default=None, description="Status of utilization"
    )

    highestPct: Optional[int] = Field(
        validation_alias="highestPct",
        default=None,
        description="Highest utilization percentage",
    )
