# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .BgpMonitorStatus import BgpMonitorStatus


class BgpMonitoringAdminServiceSetMonitorStatusBody(BaseModel):
    """
    SetMonitorStatusRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    status: BgpMonitorStatus = Field(validation_alias="status")
