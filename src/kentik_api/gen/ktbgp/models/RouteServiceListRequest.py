# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .RoutesFilter import RoutesFilter


class RouteServiceListRequest(BaseModel):
    """
    RouteServiceListRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filters: Optional[RoutesFilter] = Field(validation_alias="filters", default=None)
