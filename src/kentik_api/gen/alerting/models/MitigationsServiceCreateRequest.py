# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class MitigationsServiceCreateRequest(BaseModel):
    """
    MitigationsServiceCreateRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    platformId: str = Field(
        validation_alias="platformId",
        description="The mitigation platform ID where the mitigation will be deployed.",
    )

    methodId: str = Field(
        validation_alias="methodId",
        description="The mitigation method ID for the mitigation technique.",
    )

    ipCidr: str = Field(
        validation_alias="ipCidr", description="The IP/CIDR range to mitigate."
    )

    srcPort: Optional[str] = Field(
        validation_alias="srcPort",
        default=None,
        description="The source port to mitigate.",
    )

    dstPort: Optional[str] = Field(
        validation_alias="dstPort",
        default=None,
        description="The destination port to mitigate.",
    )

    comment: Optional[str] = Field(
        validation_alias="comment",
        default=None,
        description="A comment describing the mitigation.",
    )

    autoStopTtl: Optional[str] = Field(
        validation_alias="autoStopTtl",
        default=None,
        description="The automatic stop time-to-live for the mitigation.",
    )
