# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Mitigation(BaseModel):
    """
    Mitigation
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(validation_alias="id", default=None)

    status: Optional[str] = Field(validation_alias="status", default=None)

    companyId: Optional[str] = Field(validation_alias="companyId", default=None)

    pairingId: Optional[str] = Field(validation_alias="pairingId", default=None)

    thresholdId: Optional[str] = Field(validation_alias="thresholdId", default=None)

    isMethodOverridable: Optional[bool] = Field(
        validation_alias="isMethodOverridable", default=None
    )

    mitigationApplyType: Optional[str] = Field(
        validation_alias="mitigationApplyType", default=None
    )

    mitigationClearType: Optional[str] = Field(
        validation_alias="mitigationClearType", default=None
    )

    mitigationApplyTimer: Optional[int] = Field(
        validation_alias="mitigationApplyTimer", default=None
    )

    mitigationClearTimer: Optional[int] = Field(
        validation_alias="mitigationClearTimer", default=None
    )

    isPlatformOverridable: Optional[bool] = Field(
        validation_alias="isPlatformOverridable", default=None
    )
