# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .KeyValue import KeyValue
from .Source import Source


class AlertAutoAck(BaseModel):
    """
    AlertAutoAck model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The ID of the auto-ack configuration.",
    )

    userId: Optional[str] = Field(
        validation_alias="userId",
        default=None,
        description="The ID of the user who most recently updated the auto-ack configuration.",
    )

    source: Optional[Source] = Field(validation_alias="source", default=None)

    key: Optional[KeyValue] = Field(validation_alias="key", default=None)

    startTimeAt: str = Field(
        validation_alias="startTimeAt",
        description="The start time when the auto-ack configuration is active. Has to be at least 5 minutes in the future.",
    )

    endTimeAt: Optional[str] = Field(
        validation_alias="endTimeAt",
        default=None,
        description="The end time when the auto-ack configuration is no longer active.",
    )

    createdAt: Optional[str] = Field(
        validation_alias="createdAt",
        default=None,
        description="The time when the auto-ack configuration was created.",
    )

    modifiedAt: Optional[str] = Field(
        validation_alias="modifiedAt",
        default=None,
        description="The time when the auto-ack configuration was last modified.",
    )
