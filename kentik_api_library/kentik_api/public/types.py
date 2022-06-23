from dataclasses import dataclass
from enum import EnumMeta
from ipaddress import ip_address

# common id type across all resources
ID = str


@dataclass
class IP:
    """IP v4 or v6 with format validation; empty address is allowed"""

    addr: str = ""

    def __init__(self, addr: str = "") -> None:
        self.addr = str(ip_address(addr)) if addr else ""

    def __str__(self) -> str:
        return self.addr

    def __repr__(self) -> str:
        return self.addr

    def to_pb(self) -> str:
        """Support for serialization to protobuf"""
        return str(self)


class PermissiveEnumMeta(EnumMeta):
    """
    Allows creating Enum types that permit creating enum members with unknown values.
    See: https://stackoverflow.com/a/56001567/5000820
    """

    def __call__(cls, value, names=None, *, module=None, qualname=None, type=None, start=1):
        if names is not None:
            return super().__call__(
                value,
                names=names,
                module=module,
                qualname=qualname,
                type=type,
                start=start,
            )
        try:
            return super().__call__(
                value,
                names=names,
                module=module,
                qualname=qualname,
                type=type,
                start=start,
            )
        except ValueError:
            return value
