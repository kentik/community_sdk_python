# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .BgpMonitor import BgpMonitor


class GetMonitorResponse(BaseModel):
    """
    GetMonitorResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    monitor: Optional[BgpMonitor] = Field(validation_alias="monitor", default=None)
