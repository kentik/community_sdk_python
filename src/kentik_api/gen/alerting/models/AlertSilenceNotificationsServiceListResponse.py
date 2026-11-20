# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AlertSilenceNotificationsDefinition import AlertSilenceNotificationsDefinition
from .PaginationInfo import PaginationInfo


class AlertSilenceNotificationsServiceListResponse(BaseModel):
    """
    AlertSilenceNotificationsServiceListResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pagination: Optional[PaginationInfo] = Field(
        validation_alias="pagination", default=None
    )

    silences: Optional[List[Optional[AlertSilenceNotificationsDefinition]]] = Field(
        validation_alias="silences",
        default=None,
        description="The alert silence notifications configurations that were found matching the filters.",
    )
