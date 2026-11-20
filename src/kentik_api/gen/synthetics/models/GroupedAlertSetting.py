# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .SrcGroupBy import SrcGroupBy


class GroupedAlertSetting(BaseModel):
    """
    GroupedAlertSetting
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    metric: Optional[str] = Field(
        validation_alias="metric", default=None, description="Metric"
    )

    srcGroupBy: Optional[SrcGroupBy] = Field(
        validation_alias="srcGroupBy", default=None
    )

    percentOfSrcGroup: Optional[int] = Field(
        validation_alias="percentOfSrcGroup",
        default=None,
        description="Grouping percentage",
    )

    filterIds: Optional[List[int]] = Field(
        validation_alias="filterIds",
        default=None,
        description="List of IDs to include in the group",
    )
