# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from typing import TYPE_CHECKING, Any

from .core.rate_limit import RateLimit, rate_limit_of

if TYPE_CHECKING:
    from .client import KentikAPI as KentikAPI

__all__ = ["KentikAPI", "RateLimit", "rate_limit_of"]


def __getattr__(name: str) -> Any:
    if name == "KentikAPI":
        from .client import KentikAPI

        return KentikAPI
    raise AttributeError(name)
