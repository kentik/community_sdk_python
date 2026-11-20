# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .TimeRange import TimeRange
from .v202505Source import v202505Source


class SuppressionFilters(BaseModel):
    """
    SuppressionFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    suppressionIds: Optional[List[str]] = Field(
        validation_alias="suppressionIds",
        default=None,
        description="The IDs of the suppression configurations to list.",
    )

    sources: Optional[List[Optional[v202505Source]]] = Field(
        validation_alias="sources",
        default=None,
        description="Select suppressions explicitly associated with any of these source policies.",
    )

    userIds: Optional[List[str]] = Field(
        validation_alias="userIds",
        default=None,
        description="The IDs of the users who most recently updated the suppression configurations.",
    )

    createdAt: Optional[TimeRange] = Field(validation_alias="createdAt", default=None)

    modifiedAt: Optional[TimeRange] = Field(validation_alias="modifiedAt", default=None)

    startTimeAt: Optional[TimeRange] = Field(
        validation_alias="startTimeAt", default=None
    )

    endTimeAt: Optional[TimeRange] = Field(validation_alias="endTimeAt", default=None)
