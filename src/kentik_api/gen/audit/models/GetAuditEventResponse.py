# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AuditEvent import AuditEvent


class GetAuditEventResponse(BaseModel):
    """
    GetAuditEventResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    event: Optional[AuditEvent] = Field(validation_alias="event", default=None)
