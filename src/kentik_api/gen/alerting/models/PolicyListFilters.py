# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Source import Source
from .TimeRange import TimeRange


class PolicyListFilters(BaseModel):
    """
    PolicyListFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    sources: Optional[List[Optional[Source]]] = Field(
        validation_alias="sources",
        default=None,
        description="The source policies to list.",
    )

    userIds: Optional[List[str]] = Field(
        validation_alias="userIds",
        default=None,
        description="The IDs of the users who created the policies to filter by.",
    )

    createdAt: Optional[TimeRange] = Field(validation_alias="createdAt", default=None)

    modifiedAt: Optional[TimeRange] = Field(validation_alias="modifiedAt", default=None)
