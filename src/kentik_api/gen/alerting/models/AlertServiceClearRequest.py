# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List

from pydantic import BaseModel, Field


class AlertServiceClearRequest(BaseModel):
    """
    AlertServiceClearRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    alertIds: List[str] = Field(
        validation_alias="alertIds", description="The IDs of the alerts to clear."
    )
