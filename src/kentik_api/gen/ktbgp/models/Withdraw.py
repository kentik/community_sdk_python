# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowspecMatch import FlowspecMatch
from .RTBHMatch import RTBHMatch


class Withdraw(BaseModel):
    """
    Withdraw model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    flowspec: Optional[FlowspecMatch] = Field(validation_alias="flowspec", default=None)

    rtbh: Optional[RTBHMatch] = Field(validation_alias="rtbh", default=None)
