# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .KeyValue import KeyValue
from .Source import Source
from .TimeRange import TimeRange


class AlertAutoAckFilters(BaseModel):
    """
    AlertAutoAckFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    autoAckIds: Optional[List[str]] = Field(
        validation_alias="autoAckIds",
        default=None,
        description="The IDs of the auto-ack configurations to list.",
    )

    sources: Optional[List[Optional[Source]]] = Field(
        validation_alias="sources",
        default=None,
        description="The source policies the auto-ack configurations are applied to.",
    )

    keys: Optional[List[Optional[KeyValue]]] = Field(
        validation_alias="keys",
        default=None,
        description="The alert keys the auto-ack configurations are applied to.",
    )

    userIds: Optional[List[str]] = Field(
        validation_alias="userIds",
        default=None,
        description="The IDs of the users who created the auto-ack configurations.",
    )

    createdAt: Optional[TimeRange] = Field(validation_alias="createdAt", default=None)

    modifiedAt: Optional[TimeRange] = Field(validation_alias="modifiedAt", default=None)

    startTimeAt: Optional[TimeRange] = Field(
        validation_alias="startTimeAt", default=None
    )

    endTimeAt: Optional[TimeRange] = Field(validation_alias="endTimeAt", default=None)
