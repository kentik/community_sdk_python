# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .Path import Path


class GetTraceForTestResponse(BaseModel):
    """
    GetTraceForTestResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    nodes: Optional[Dict[str, Any]] = Field(
        validation_alias="nodes",
        default=None,
        description="Map of network node information keyed by node IDs",
    )

    paths: Optional[List[Optional[Path]]] = Field(
        validation_alias="paths",
        default=None,
        description="List of retrieved network path data",
    )
