# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AlertSilenceNotificationsDefinition import AlertSilenceNotificationsDefinition


class AlertSilenceNotificationsServiceReplaceResponse(BaseModel):
    """
    AlertSilenceNotificationsServiceReplaceResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    silence: Optional[AlertSilenceNotificationsDefinition] = Field(
        validation_alias="silence", default=None
    )
