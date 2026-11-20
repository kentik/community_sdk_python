# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class InterfaceVrf(BaseModel):
    """
    InterfaceVrf model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="ID of the VRF. Set to reference an existing VRF; omit when creating a new VRF.",
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="VRF name."
    )

    description: Optional[str] = Field(
        validation_alias="description", default=None, description="VRF description."
    )

    routeDistinguisher: Optional[str] = Field(
        validation_alias="routeDistinguisher",
        default=None,
        description="Route distinguisher. Required when creating a new VRF.",
    )

    extRouteDistinguisher: Optional[str] = Field(
        validation_alias="extRouteDistinguisher",
        default=None,
        description="Extended route distinguisher. Required when creating a new VRF.",
    )

    routeTarget: Optional[str] = Field(
        validation_alias="routeTarget",
        default=None,
        description="Route target. Required when creating a new VRF.",
    )

    routeTargets: Optional[List[str]] = Field(
        validation_alias="routeTargets", default=None, description="Route targets."
    )
