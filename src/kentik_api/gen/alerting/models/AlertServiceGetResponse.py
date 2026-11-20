# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Alert import Alert
from .AlertPhase import AlertPhase
from .Comment import Comment


class AlertServiceGetResponse(BaseModel):
    """
    AlertServiceGetResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    alert: Optional[Alert] = Field(validation_alias="alert", default=None)

    history: Optional[List[Optional[AlertPhase]]] = Field(
        validation_alias="history",
        default=None,
        description="The history of the alert.",
    )

    comments: Optional[List[Optional[Comment]]] = Field(
        validation_alias="comments",
        default=None,
        description="The comments on the alert.",
    )
