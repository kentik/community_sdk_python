# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class DisabledMetrics(BaseModel):
    """
    DisabledMetrics model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    pingLatency: Optional[bool] = Field(validation_alias="pingLatency", default=None)

    pingJitter: Optional[bool] = Field(validation_alias="pingJitter", default=None)

    pingPacketLoss: Optional[bool] = Field(
        validation_alias="pingPacketLoss", default=None
    )

    httpLatency: Optional[bool] = Field(validation_alias="httpLatency", default=None)

    httpHeaders: Optional[bool] = Field(validation_alias="httpHeaders", default=None)

    httpCodes: Optional[bool] = Field(validation_alias="httpCodes", default=None)

    httpCertExpiry: Optional[bool] = Field(
        validation_alias="httpCertExpiry", default=None
    )

    transactionLatency: Optional[bool] = Field(
        validation_alias="transactionLatency", default=None
    )

    dnsLatency: Optional[bool] = Field(validation_alias="dnsLatency", default=None)

    dnsCodes: Optional[bool] = Field(validation_alias="dnsCodes", default=None)

    dnsIps: Optional[bool] = Field(validation_alias="dnsIps", default=None)

    throughputBandwidth: Optional[bool] = Field(
        validation_alias="throughputBandwidth", default=None
    )
