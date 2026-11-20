# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict

from pydantic import BaseModel, Field


class AlertSilenceNotificationsServiceReplaceBody(BaseModel):
    """
    AlertSilenceNotificationsServiceReplaceBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    silence: Dict[str, Any] = Field(validation_alias="silence")
