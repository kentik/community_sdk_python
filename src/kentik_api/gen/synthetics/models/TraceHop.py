# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class TraceHop(BaseModel):
    """
    TraceHop
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    latency: Optional[int] = Field(
        validation_alias="latency",
        default=None,
        description="Round-trip packet latency to the node (in microseconds) - 0 if no response was received",
    )

    nodeId: Optional[str] = Field(
        validation_alias="nodeId",
        default=None,
        description="ID of the node for this hop in the Nodes map  - empty if no response was received",
    )
