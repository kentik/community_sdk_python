"""This module provides default types and values for uninitialized fields of request's payload classes
and also mypy tool's type error suppression for special cases."""
from typing import Any


class NOTSET:
    """Default type for unset fields."""

    def __repr__(self) -> str:
        return "NOTSET_"


_NOTSET: NOTSET = NOTSET()
"""Default value for unset fields."""

_NOTSET_ = Any
"""mypy tool's type error suppression and indicator of expected real value."""

_None_ = Any
"""mypy tool's type error suppression and indicator of expected real value."""
