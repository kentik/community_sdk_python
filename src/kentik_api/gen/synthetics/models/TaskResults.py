# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .DNSResults import DNSResults
from .HTTPResults import HTTPResults
from .PingResults import PingResults


class TaskResults(BaseModel):
    """
    TaskResults
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ping: Optional[PingResults] = Field(validation_alias="ping", default=None)

    http: Optional[HTTPResults] = Field(validation_alias="http", default=None)

    dns: Optional[DNSResults] = Field(validation_alias="dns", default=None)

    health: Optional[str] = Field(
        validation_alias="health", default=None, description="Health status of the task"
    )
