from typing import Any, Dict

def as_dict(obj: Any) -> Dict[str, Any]:
    """ Convert obj to dict, removing all keys with None values """

    assert hasattr(obj, "__dict__") or isinstance(obj, dict), "Input should be either class or dict instance"

    if hasattr(obj, "__dict__"):
        obj = obj.__dict__

    result = dict()
    for k, v in obj.items():
        if v is None:
            continue
        if hasattr(v, "__dict__") or isinstance(v, dict):
            result[k] = as_dict(v)
        else:
            result[k] = v

    return result
