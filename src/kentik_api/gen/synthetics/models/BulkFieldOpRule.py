# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .BulkFieldOp import BulkFieldOp


class BulkFieldOpRule(BaseModel):
    """
    BulkFieldOpRule
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    mask: str = Field(
        validation_alias="mask",
        description="Set-valued attributes, relative to `test`, that this op applies to. Each must also be in the request's effective `mask`.",
    )

    op: BulkFieldOp = Field(validation_alias="op")
