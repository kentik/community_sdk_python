# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ServiceNowConfig import ServiceNowConfig


class ListServiceNowConfigsResponse(BaseModel):
    """
    ListServiceNowConfigsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    configs: Optional[List[Optional[ServiceNowConfig]]] = Field(
        validation_alias="configs", default=None
    )
