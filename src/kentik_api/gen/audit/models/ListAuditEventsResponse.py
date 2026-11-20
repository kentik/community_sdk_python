# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AuditEvent import AuditEvent


class ListAuditEventsResponse(BaseModel):
    """
    ListAuditEventsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    events: Optional[List[Optional[AuditEvent]]] = Field(
        validation_alias="events", default=None
    )
