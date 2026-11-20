# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SummaryStatusRunoutStatus import SummaryStatusRunoutStatus
from .SummaryStatusUtilStatus import SummaryStatusUtilStatus


class SummaryStatus(BaseModel):
    """
    SummaryStatus
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    runout: Optional[SummaryStatusRunoutStatus] = Field(
        validation_alias="runout", default=None
    )

    utilization: Optional[SummaryStatusUtilStatus] = Field(
        validation_alias="utilization", default=None
    )
