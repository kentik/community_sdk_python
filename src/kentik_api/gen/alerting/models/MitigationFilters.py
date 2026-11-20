# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationState import MitigationState
from .MitigationType import MitigationType
from .Source import Source
from .TimeRange import TimeRange


class MitigationFilters(BaseModel):
    """
    MitigationFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    createdAt: Optional[TimeRange] = Field(validation_alias="createdAt", default=None)

    mitigationIds: Optional[List[str]] = Field(
        validation_alias="mitigationIds",
        default=None,
        description="The IDs of the mitigations to list.",
    )

    sources: Optional[List[Optional[Source]]] = Field(
        validation_alias="sources",
        default=None,
        description="The source policies the mitigations are associated with.",
    )

    alarmIds: Optional[List[str]] = Field(
        validation_alias="alarmIds",
        default=None,
        description="The alarm IDs the mitigations are associated with.",
    )

    states: Optional[List[Optional[MitigationState]]] = Field(
        validation_alias="states",
        default=None,
        description="The states of the mitigations to filter by.",
    )

    platformIds: Optional[List[str]] = Field(
        validation_alias="platformIds",
        default=None,
        description="The mitigation platform IDs the mitigations are associated with.",
    )

    methodIds: Optional[List[str]] = Field(
        validation_alias="methodIds",
        default=None,
        description="The mitigation method IDs the mitigations are associated with.",
    )

    ipCidrs: Optional[List[str]] = Field(
        validation_alias="ipCidrs",
        default=None,
        description="The IP/CIDR ranges the mitigations target.",
    )

    ipCidrPattern: Optional[str] = Field(
        validation_alias="ipCidrPattern",
        default=None,
        description="The IP/CIDR pattern to filter mitigations by.",
    )

    types: Optional[List[Optional[MitigationType]]] = Field(
        validation_alias="types",
        default=None,
        description="The types of mitigations to filter by.",
    )
