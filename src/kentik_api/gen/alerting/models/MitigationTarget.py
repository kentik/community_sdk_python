# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowspecMatch import FlowspecMatch
from .KeyValue import KeyValue


class MitigationTarget(BaseModel):
    """
    MitigationTarget model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ipCidr: Optional[str] = Field(validation_alias="ipCidr", default=None)

    flowspec: Optional[FlowspecMatch] = Field(validation_alias="flowspec", default=None)

    adaptiveFlowspec: Optional[KeyValue] = Field(
        validation_alias="adaptiveFlowspec", default=None
    )
