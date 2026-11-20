# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowspecActionTerminalSample(BaseModel):
    """
    FlowspecActionTerminalSample specifies that the traffic action extended community.

    terminal, sample or sample-terminal action types.
    https://datatracker.ietf.org/doc/html/rfc8955#name-traffic-action-traffic-acti
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    terminal: Optional[bool] = Field(validation_alias="terminal", default=None)

    sample: Optional[bool] = Field(validation_alias="sample", default=None)
