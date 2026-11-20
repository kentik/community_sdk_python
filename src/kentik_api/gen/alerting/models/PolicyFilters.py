# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PolicyFiltersFieldFilter import PolicyFiltersFieldFilter
from .PolicyFiltersFilterConnector import PolicyFiltersFilterConnector
from .PolicyFiltersSavedFilter import PolicyFiltersSavedFilter


class PolicyFilters(BaseModel):
    """
    PolicyFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not",
        serialization_alias="not",
        default=None,
        description="If true, the filter will be negated.",
    )

    connector: Optional[PolicyFiltersFilterConnector] = Field(
        validation_alias="connector", default=None
    )

    filters: Optional[List[Optional[PolicyFiltersFieldFilter]]] = Field(
        validation_alias="filters",
        default=None,
        description="The actual filters of the policy.",
    )

    groups: Optional[List[Optional["PolicyFilters"]]] = Field(
        validation_alias="groups",
        default=None,
        description="The nested groups of the policy filters.",
    )

    saved: Optional[List[Optional[PolicyFiltersSavedFilter]]] = Field(
        validation_alias="saved",
        default=None,
        description="The saved filters of the policy. Saved filters are pre-defined filters that can be used in the policy.",
    )
