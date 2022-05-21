from enum import Enum
from typing import Any

from kentik_api import KentikAPI
from kentik_api.utils import get_credentials


def is_class(v: Any) -> bool:
    return hasattr(v, "__dict__") and not isinstance(v, Enum)


def is_non_empty_data_structure_list(v: Any) -> bool:
    return isinstance(v, list) and len(v) > 0 and is_class(v[0])


def new_line_if_needed(v: Any) -> str:
    if is_class(v) or isinstance(v, dict) or is_non_empty_data_structure_list(v):
        return "\n"
    else:
        return ""


def pretty_print(v: Any, indent_level: int = 1) -> None:
    """Print object in an indented way"""

    indent = " " * indent_level * 2

    if isinstance(v, Enum):
        print(f"{v.value}")
    elif isinstance(v, str):
        print(f'"{v}"')
    elif isinstance(v, dict):
        for name, value in v.items():
            if callable(value):
                continue
            print(f"{indent}{name}: ", end=new_line_if_needed(value))
            pretty_print(value, indent_level + 1)
    elif is_class(v):
        for name, value in v.__dict__.items():
            if callable(value):
                continue
            print(f"{indent}{name}: ", end=new_line_if_needed(value))
            pretty_print(value, indent_level + 1)
    elif is_non_empty_data_structure_list(v):
        for i, item in enumerate(v):
            print(f"{indent}[{i}]")
            pretty_print(item, indent_level + 1)
    else:
        print(f"{v}")


def client() -> KentikAPI:
    """Get KentikAPI client"""

    email, token = get_credentials()
    return KentikAPI(email, token)
