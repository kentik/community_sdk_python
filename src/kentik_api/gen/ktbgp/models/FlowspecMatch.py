# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FragmentFormula import FragmentFormula
from .NumericFormula import NumericFormula
from .TCPFlagsFormula import TCPFlagsFormula


class FlowspecMatch(BaseModel):
    """
    FlowspecMatch represents the traffic filtering criteria encoded
    as Flow Specification NLRI as per RFC 8955:
    https://datatracker.ietf.org/doc/html/rfc8955#name-dissemination-of-ipv4-flow-
    and other related documents.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dstPrefix: Optional[str] = Field(
        validation_alias="dstPrefix",
        default=None,
        description="IPv4 or IPv6 CIDR prefix to match",
    )

    srcPrefix: Optional[str] = Field(
        validation_alias="srcPrefix",
        default=None,
        description="IPv4 or IPv6 CIDR prefix to match",
    )

    ipProtocol: Optional[NumericFormula] = Field(
        validation_alias="ipProtocol", default=None
    )

    dstPort: Optional[NumericFormula] = Field(validation_alias="dstPort", default=None)

    srcPort: Optional[NumericFormula] = Field(validation_alias="srcPort", default=None)

    icmpType: Optional[NumericFormula] = Field(
        validation_alias="icmpType", default=None
    )

    icmpCode: Optional[NumericFormula] = Field(
        validation_alias="icmpCode", default=None
    )

    tcpFlags: Optional[TCPFlagsFormula] = Field(
        validation_alias="tcpFlags", default=None
    )

    packetLength: Optional[NumericFormula] = Field(
        validation_alias="packetLength", default=None
    )

    dscp: Optional[NumericFormula] = Field(validation_alias="dscp", default=None)

    fragments: Optional[FragmentFormula] = Field(
        validation_alias="fragments", default=None
    )
