from typing import Any, Dict, List
from enum import Enum


def as_dict(obj: Any) -> Dict[str, Any]:
    """ Convert obj to dict, removing all keys with None values """

    assert hasattr(obj, "__dict__") or isinstance(obj, dict), f"Input should be either class or dict , got: {type(obj)}"

    if hasattr(obj, "__dict__"):
        obj = obj.__dict__

    result = dict()
    for k, v in obj.items():
        if v is None:
            continue
        if isinstance(v, Enum):
            result[k] = v.value
        elif isinstance(v, list):
            result[k] = process_list(v)
        elif hasattr(v, "__dict__") or isinstance(v, dict):
            result[k] = as_dict(v)
        else:
            result[k] = v

    return result


def process_list(l: List[Any]) -> List[Any]:
    result = list()
    for item in l:
        if isinstance(item, Enum):
            result.append(item.value)
        elif hasattr(item, "__dict__") or isinstance(item, dict):
            result.append(as_dict(item))
        else:
            result.append(item)

    return result
