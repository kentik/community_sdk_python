# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .NmsCondition import NmsCondition
from .NmsConditionConnector import NmsConditionConnector


class NmsConditionGroup(BaseModel):
    """
    NmsConditionGroup model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    connector: Optional[NmsConditionConnector] = Field(
        validation_alias="connector", default=None
    )

    not_: Optional[bool] = Field(
        validation_alias="not", serialization_alias="not", default=None
    )

    conditions: Optional[List[Optional[NmsCondition]]] = Field(
        validation_alias="conditions", default=None
    )

    conditionGroups: Optional[List[Optional["NmsConditionGroup"]]] = Field(
        validation_alias="conditionGroups", default=None, description="recursive"
    )
