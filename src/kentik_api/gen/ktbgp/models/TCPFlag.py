# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class TCPFlag(str, Enum):
    TCP_FLAG_UNSPECIFIED = "TCP_FLAG_UNSPECIFIED"

    TCP_FLAG_FIN = "TCP_FLAG_FIN"

    TCP_FLAG_SYN = "TCP_FLAG_SYN"

    TCP_FLAG_RST = "TCP_FLAG_RST"

    TCP_FLAG_PSH = "TCP_FLAG_PSH"

    TCP_FLAG_ACK = "TCP_FLAG_ACK"

    TCP_FLAG_URG = "TCP_FLAG_URG"

    TCP_FLAG_ECE = "TCP_FLAG_ECE"

    TCP_FLAG_CWR = "TCP_FLAG_CWR"
