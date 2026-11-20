# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .FilterField import FilterField


class Filter(BaseModel):
    """
    Filter
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(validation_alias="name", default=None)

    named: Optional[bool] = Field(validation_alias="named", default=None)

    connector: Optional[str] = Field(validation_alias="connector", default=None)

    not_: Optional[bool] = Field(
        validation_alias="not", serialization_alias="not", default=None
    )

    autoAdded: Optional[str] = Field(validation_alias="autoAdded", default=None)

    savedFilters: Optional[List[str]] = Field(
        validation_alias="savedFilters", default=None
    )

    filters: Optional[List[Optional[FilterField]]] = Field(
        validation_alias="filters", default=None
    )

    filterGroups: Optional[List[Optional["Filter"]]] = Field(
        validation_alias="filterGroups", default=None
    )

    metric: Optional[List[str]] = Field(validation_alias="metric", default=None)
