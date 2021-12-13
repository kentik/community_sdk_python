from typing import Any, Dict


def reverse_map(src_map: Dict[Any, Any], value: Any) -> Any:
    """Get key by value"""
    for key, val in src_map.items():
        if val == value:
            return key
    raise RuntimeError(f"Value '{value}' not found in map")
