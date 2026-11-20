# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .NmsActivateOrClearConditions import NmsActivateOrClearConditions
from .NmsPolicyLevelSettingsClearType import NmsPolicyLevelSettingsClearType


class NmsPolicyLevelSettings(BaseModel):
    """
    NmsPolicyLevelSettings model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    activate: Optional[NmsActivateOrClearConditions] = Field(
        validation_alias="activate", default=None
    )

    clearType: Optional[NmsPolicyLevelSettingsClearType] = Field(
        validation_alias="clearType", default=None
    )

    conditional: Optional[NmsActivateOrClearConditions] = Field(
        validation_alias="conditional", default=None
    )
