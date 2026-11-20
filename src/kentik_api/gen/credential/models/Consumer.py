# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Consumer(BaseModel):
    """
    Consumer
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: Optional[str] = Field(
        validation_alias="type",
        default=None,
        description="Consumer type: synth, nms, ai, cloud, deviceconf or mcp",
    )

    consumerId: Optional[str] = Field(
        validation_alias="consumerId",
        default=None,
        description="Id of the consuming entity (synthetic test id, device id, etc.)",
    )
