# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .NmsActivateOrClearConditions import NmsActivateOrClearConditions
from .Severity import Severity


class NmsContextActivationInfo(BaseModel):
    """
    NmsContextActivationInfo model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    activate: Optional[NmsActivateOrClearConditions] = Field(
        validation_alias="activate", default=None
    )

    severity: Optional[Severity] = Field(validation_alias="severity", default=None)

    clearManual: Optional[bool] = Field(validation_alias="clearManual", default=None)

    clearUnlessActivated: Optional[bool] = Field(
        validation_alias="clearUnlessActivated", default=None
    )
