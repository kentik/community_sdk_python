# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .RouteInfo import RouteInfo


class GetRoutesForTargetResponse(BaseModel):
    """
    GetRoutesForTargetResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    routes: Optional[List[Optional[RouteInfo]]] = Field(
        validation_alias="routes", default=None, description="List of routes"
    )

    asNames: Optional[Dict[str, Any]] = Field(
        validation_alias="asNames",
        default=None,
        description="look-aside map AS names keyed by ASNs",
    )
