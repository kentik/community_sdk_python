# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AlertAutoAck import AlertAutoAck
from .PaginationInfo import PaginationInfo


class AlertAutoAckServiceListResponse(BaseModel):
    """
    AlertAutoAckServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationInfo] = Field(
        validation_alias="pagination", default=None
    )

    autoAcks: Optional[List[Optional[AlertAutoAck]]] = Field(
        validation_alias="autoAcks",
        default=None,
        description="The auto-ack configurations that were found matching the filters.",
    )
