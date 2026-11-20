# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CapacityPlanInterfaceDetail import CapacityPlanInterfaceDetail
from .Config import Config
from .SummaryStatus import SummaryStatus


class CapacityPlan(BaseModel):
    """
    CapacityPlan
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="ID of capacity plan"
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Name of capacity plan"
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Description of capacity plan",
    )

    status: Optional[str] = Field(
        validation_alias="status", default=None, description="Status of capacity plan"
    )

    interfaces: Optional[List[Optional[CapacityPlanInterfaceDetail]]] = Field(
        validation_alias="interfaces", default=None, description="List of interfaces"
    )

    config: Optional[Config] = Field(validation_alias="config", default=None)

    summaryStatus: Optional[SummaryStatus] = Field(
        validation_alias="summaryStatus", default=None
    )
