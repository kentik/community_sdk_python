# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class AlertServiceClearResponse(BaseModel):
    """
    AlertServiceClearResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    clearedAlertIds: Optional[List[str]] = Field(
        validation_alias="clearedAlertIds",
        default=None,
        description="The IDs of the alerts that have been cleared.",
    )
