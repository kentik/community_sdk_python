# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .NmsConditionConnector import NmsConditionConnector
from .NmsConditionGroup import NmsConditionGroup


class NmsActivateOrClearConditions(BaseModel):
    """
    NmsActivateOrClearConditions model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    connector: Optional[NmsConditionConnector] = Field(
        validation_alias="connector", default=None
    )

    conditionGroups: Optional[List[Optional[NmsConditionGroup]]] = Field(
        validation_alias="conditionGroups", default=None
    )
