# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class FlowTagServiceUpdateFlowTagBody(BaseModel):
    """
    UpdateFlowTagRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    flowTag: Optional[Dict[str, Any]] = Field(
        validation_alias="flowTag", default=None, description="FlowTag"
    )
