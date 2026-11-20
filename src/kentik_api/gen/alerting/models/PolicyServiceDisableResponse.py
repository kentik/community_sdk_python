# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Policy import Policy


class PolicyServiceDisableResponse(BaseModel):
    """
    PolicyServiceDisableResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    policy: Optional[Policy] = Field(validation_alias="policy", default=None)
