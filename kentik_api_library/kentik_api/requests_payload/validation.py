from typing import Any, Iterable, Mapping

from kentik_api.public.errors import DeserializationError


def validate_fields(class_name: str, required_fields: Iterable[str], dic: Mapping[str, Any]) -> None:
    """Check if all required_fields are present in dic. Raise error otherwise"""
    missing_fields = []
    for f in required_fields:
        if f not in dic:
            missing_fields.append(f)

    if len(missing_fields) > 0:
        raise DeserializationError(class_name, "missing values for fields " + ", ".join(missing_fields))
