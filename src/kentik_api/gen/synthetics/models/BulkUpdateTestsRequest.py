# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BulkFieldOpRule import BulkFieldOpRule
from .v202309Test import v202309Test


class BulkUpdateTestsRequest(BaseModel):
    """
    BulkUpdateTestsRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ids: List[str] = Field(
        validation_alias="ids",
        description="IDs of the tests to update, as decimal integers. Between 1 and 50 distinct IDs; duplicates are ignored. Deleted tests and IDs that do not exist are reported in `skipped`.",
    )

    test: v202309Test = Field(validation_alias="test")

    mask: Optional[str] = Field(
        validation_alias="mask",
        default=None,
        description="Attributes to be updated, relative to `test`. When empty, the populated attributes of `test` are updated; nothing else is replaced. Required only to set an attribute to its zero or empty value. Wildcard and non-leaf paths are rejected.",
    )

    ops: Optional[List[Optional[BulkFieldOpRule]]] = Field(
        validation_alias="ops",
        default=None,
        description="Add or remove values on set-valued attributes instead of replacing them. Attributes not listed are replaced. A path may appear in at most one rule; duplicates are rejected.",
    )

    allowPartialBatch: Optional[bool] = Field(
        validation_alias="allowPartialBatch",
        default=None,
        description="When true, tests that pass validation are updated even if others fail it. When false (the default), no test is updated if any test fails validation. Does not apply to attributes limited to certain test types: if any selected test is of another type, the whole request is rejected either way.",
    )
