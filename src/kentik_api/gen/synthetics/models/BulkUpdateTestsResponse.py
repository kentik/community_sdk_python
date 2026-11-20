# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .BulkActionStatus import BulkActionStatus


class BulkUpdateTestsResponse(BaseModel):
    """
    BulkUpdateTestsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    status: Optional[BulkActionStatus] = Field(validation_alias="status", default=None)
