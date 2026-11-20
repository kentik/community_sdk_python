# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PathTrace import PathTrace
from .Stats import Stats


class Path(BaseModel):
    """
    Path
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agentId: Optional[str] = Field(
        validation_alias="agentId",
        default=None,
        description="ID of the agent generating the path data",
    )

    targetIp: Optional[str] = Field(
        validation_alias="targetIp",
        default=None,
        description="IP address of the target of the path",
    )

    hopCount: Optional[Stats] = Field(validation_alias="hopCount", default=None)

    maxAsPathLength: Optional[int] = Field(
        validation_alias="maxAsPathLength",
        default=None,
        description="Maximum length of AS path across all traces",
    )

    traces: Optional[List[Optional[PathTrace]]] = Field(
        validation_alias="traces",
        default=None,
        description="Data for individual traces",
    )

    time: Optional[str] = Field(
        validation_alias="time",
        default=None,
        description="Timestamp (UTC) of initiation of the path trace",
    )
