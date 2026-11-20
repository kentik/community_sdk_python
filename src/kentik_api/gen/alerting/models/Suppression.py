# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ContextFilter import ContextFilter
from .MultiAttributeFilter import MultiAttributeFilter
from .Severity import Severity
from .TimestampSetting import TimestampSetting
from .v202505Source import v202505Source


class Suppression(BaseModel):
    """
    Different matching constraints are ANDed. Values within sources
    and severities are alternatives. At least one non-empty matching constraint is
    required; a display name, comment, or strictness flag alone is insufficient.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The ID of the suppression configuration. Required to identify the existing suppression on Replace; assigned by the server on Create.",
    )

    displayName: Optional[str] = Field(
        validation_alias="displayName",
        default=None,
        description="The name of the suppression configuration. Omission on Replace clears the name.",
    )

    comment: Optional[str] = Field(
        validation_alias="comment",
        default=None,
        description="The comment for the suppression configuration. Omission on Replace clears the comment.",
    )

    contextFilter: Optional[ContextFilter] = Field(
        validation_alias="contextFilter", default=None
    )

    sources: Optional[List[Optional[v202505Source]]] = Field(
        validation_alias="sources",
        default=None,
        description="The source policies whose alerts may be suppressed. IDs are public policy IDs, not internal Alert Manager rule IDs. Any listed source may match. Empty means all source policies, subject to the other matching constraints.",
    )

    severities: Optional[List[Optional[Severity]]] = Field(
        validation_alias="severities",
        default=None,
        description="The alarm severities the suppression applies to. Any listed severity may match. Empty means all severities, subject to the other matching constraints.",
    )

    keyFilter: Optional[MultiAttributeFilter] = Field(
        validation_alias="keyFilter", default=None
    )

    startTimeAt: Optional[str] = Field(
        validation_alias="startTimeAt",
        default=None,
        description="The resolved start time when suppression becomes active. On Create or Replace, omission defaults to the earliest permitted start unless start_time_code overrides it. On Replace, use KEEP_UNCHANGED to retain the existing start time. Worker propagation may delay effectiveness.",
    )

    startTimeCode: Optional[TimestampSetting] = Field(
        validation_alias="startTimeCode", default=None
    )

    endTimeAt: Optional[str] = Field(
        validation_alias="endTimeAt",
        default=None,
        description="The resolved time when suppression ceases to be active. Omission on Create or Replace means no expiration unless end_time_code overrides it. An explicit end must be after the start and after the current time, satisfy the minimum suppression window, and allow time for propagation.",
    )

    endTimeCode: Optional[TimestampSetting] = Field(
        validation_alias="endTimeCode", default=None
    )

    createdAt: Optional[str] = Field(
        validation_alias="createdAt",
        default=None,
        description="The time when the suppression configuration was created.",
    )

    modifiedAt: Optional[str] = Field(
        validation_alias="modifiedAt",
        default=None,
        description="The time when the suppression configuration was last modified.",
    )
