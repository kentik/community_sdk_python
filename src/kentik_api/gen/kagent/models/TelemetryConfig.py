# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class TelemetryConfig(BaseModel):
    """
    TelemetryConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    logsEndpoint: Optional[str] = Field(
        validation_alias="logsEndpoint",
        default=None,
        description="Endpoint the agent sends logs to.",
    )

    metricsEndpoint: Optional[str] = Field(
        validation_alias="metricsEndpoint",
        default=None,
        description="Endpoint the agent sends metrics to.",
    )

    kmetricsEndpoint: Optional[str] = Field(
        validation_alias="kmetricsEndpoint",
        default=None,
        description="Endpoint the agent sends kmetrics to.",
    )

    sentryEndpoint: Optional[str] = Field(
        validation_alias="sentryEndpoint",
        default=None,
        description="Endpoint the agent sends crash reports to.",
    )
