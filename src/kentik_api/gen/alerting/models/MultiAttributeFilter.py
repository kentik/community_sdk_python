# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .KeyValueFilter import KeyValueFilter


class MultiAttributeFilter(BaseModel):
    """
    MultiAttributeFilter model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filter: Optional[Dict[str, Any]] = Field(
        validation_alias="filter",
        default=None,
        description="Deprecated: Use MultiAttributeFilter.filters instead.",
    )

    filters: Optional[List[Optional[KeyValueFilter]]] = Field(
        validation_alias="filters", default=None
    )

    strict: Optional[bool] = Field(
        validation_alias="strict",
        default=None,
        description='Every filter must match at least one grouping-key attribute. When true,\nevery grouping-key attribute must also match at least one filter. A filter\nmay match multiple attributes.\n\nExample:\n  filters = [{ key: {equals: "i_device_id"}, value: {equals: "1001"} }]\n  strict = true\n\n  key i_device_id=1001                         - matches\n  key i_device_id=1001, inet_src=ipv4          - does not match',
    )
