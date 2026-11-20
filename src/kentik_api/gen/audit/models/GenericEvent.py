# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GenericEvent(BaseModel):
    """
    GenericEvent model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    eventSource: Optional[str] = Field(
        validation_alias="eventSource",
        default=None,
        description="Attribute Source of Audit log",
    )

    action: Optional[str] = Field(
        validation_alias="action",
        default=None,
        description="Attribute Action of Audit log",
    )

    eventType: Optional[str] = Field(
        validation_alias="eventType",
        default=None,
        description="Attribute Type of Audit log",
    )

    owner: Optional[str] = Field(
        validation_alias="owner",
        default=None,
        description="Attribute User of Audit log",
    )

    metadata: Optional[Dict[str, Any]] = Field(
        validation_alias="metadata",
        default=None,
        description="generic bag of metadata about the event",
    )
