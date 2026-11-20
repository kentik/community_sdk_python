# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .MetricsSchema import MetricsSchema


class GetMetricsSchemaResponse(BaseModel):
    """
    GetMetricsSchemaResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    schema_: Optional[MetricsSchema] = Field(
        validation_alias="schema", serialization_alias="schema", default=None
    )
