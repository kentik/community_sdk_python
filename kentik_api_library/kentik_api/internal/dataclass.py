from dataclasses import MISSING
from typing import Any, List


def mandatory_dataclass_attributes(data_cls: Any) -> List[str]:
    try:
        return [
            n for n, f in data_cls.__dataclass_fields__.items() if f.default is MISSING and f.default_factory is MISSING
        ]
    except AttributeError:
        return []
