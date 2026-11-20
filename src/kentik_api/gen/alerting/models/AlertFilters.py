# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AlertState import AlertState
from .MultiAttributeFilter import MultiAttributeFilter
from .Severity import Severity
from .Source import Source
from .TimeRange import TimeRange
from .v202505AlertAcknowledgement import v202505AlertAcknowledgement


class AlertFilters(BaseModel):
    """
    AlertFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    severities: Optional[List[Optional[Severity]]] = Field(
        validation_alias="severities",
        default=None,
        description="The severities of the alerts to list.",
    )

    alertIds: Optional[List[str]] = Field(
        validation_alias="alertIds",
        default=None,
        description="The IDs of the alerts to list.",
    )

    sources: Optional[List[Optional[Source]]] = Field(
        validation_alias="sources",
        default=None,
        description="The source policies of the alerts to list.",
    )

    keys: Optional[MultiAttributeFilter] = Field(validation_alias="keys", default=None)

    states: Optional[List[Optional[AlertState]]] = Field(
        validation_alias="states",
        default=None,
        description="The states of the alerts to list.",
    )

    startedAt: Optional[TimeRange] = Field(validation_alias="startedAt", default=None)

    endedAt: Optional[TimeRange] = Field(validation_alias="endedAt", default=None)

    highestSeverities: Optional[List[Optional[Severity]]] = Field(
        validation_alias="highestSeverities",
        default=None,
        description="Filter alerts by the highest reached severity.",
    )

    recentSeverities: Optional[List[Optional[Severity]]] = Field(
        validation_alias="recentSeverities",
        default=None,
        description="Filter alerts by the most recent (for active ones) and last (for cleared ones) severity.",
    )

    ackStates: Optional[List[Optional[v202505AlertAcknowledgement]]] = Field(
        validation_alias="ackStates",
        default=None,
        description="The acknowledgement states of the alerts to list.",
    )

    activeAt: Optional[TimeRange] = Field(validation_alias="activeAt", default=None)

    ackedByUserIds: Optional[List[str]] = Field(
        validation_alias="ackedByUserIds",
        default=None,
        description="The IDs of the users who acknowledged the alerts to list.",
    )

    includeRemovedPolicies: Optional[bool] = Field(
        validation_alias="includeRemovedPolicies",
        default=None,
        description="Whether to include removed policies in the response. If true, the response will include alerts from source that has been removed.",
    )

    contextSearch: Optional[List[str]] = Field(
        validation_alias="contextSearch",
        default=None,
        description="The context search terms (e.g. device name, interface name, site name, labels etc.) of the alerts to list.",
    )
