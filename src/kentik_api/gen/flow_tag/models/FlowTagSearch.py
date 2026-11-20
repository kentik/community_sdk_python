# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .LookupField import LookupField
from .OrderField import OrderField


class FlowTagSearch(BaseModel):
    """
    FlowTagSearch
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    limit: Optional[int] = Field(
        validation_alias="limit",
        default=None,
        description="Limit the number of rows to fetch",
    )

    offset: Optional[int] = Field(
        validation_alias="offset",
        default=None,
        description="The number rows to skip before returning",
    )

    lookupFields: Optional[List[Optional[LookupField]]] = Field(
        validation_alias="lookupFields",
        default=None,
        description="List of lookup fields",
    )

    lookupValues: Optional[List[str]] = Field(
        validation_alias="lookupValues",
        default=None,
        description="List of lookup values",
    )

    orderBy: Optional[List[Optional[OrderField]]] = Field(
        validation_alias="orderBy", default=None, description="Sort order"
    )

    fieldLimit: Optional[int] = Field(
        validation_alias="fieldLimit",
        default=None,
        description="Limit the number of record to return for nested fields",
    )
