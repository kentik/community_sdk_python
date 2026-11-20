# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Verifies every model field sends the name it was read under.

A field whose Python name differs from its wire name (the keyword `not`
becomes `not_`, protobuf's `@type` becomes `type`) once dumped the Python
name, so a saved filter's negation reached the API as `not_` and was ignored.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path

import pytest
from pydantic import BaseModel

from kentik_api import gen


def _models() -> list[type[BaseModel]]:
    found = []
    for service in pkgutil.iter_modules(gen.__path__):
        try:
            models = importlib.import_module(f"kentik_api.gen.{service.name}.models")
        except ModuleNotFoundError:
            continue
        found += [
            obj
            for obj in vars(models).values()
            if inspect.isclass(obj)
            and issubclass(obj, BaseModel)
            and obj.__module__.startswith(models.__name__)
        ]
    return sorted(set(found), key=lambda cls: cls.__module__)


RENAMED = [
    (model, name, field.validation_alias)
    for model in _models()
    for name, field in model.model_fields.items()
    if field.validation_alias not in (None, name)
]


def test_renamed_fields_exist():
    assert RENAMED, "the schema has keyword fields such as `not`"


@pytest.mark.parametrize(
    ("model", "name", "wire"),
    RENAMED,
    ids=[f"{m.__module__.split('.')[2]}.{m.__name__}.{n}" for m, n, _ in RENAMED],
)
def test_a_renamed_field_dumps_its_wire_name(model, name, wire):
    assert model.model_fields[name].serialization_alias == wire


def test_every_rest_model_body_is_dumped_by_alias():
    dumps = [
        line.strip()
        for path in sorted(Path(gen.__path__[0]).glob("*/services/*.py"))
        for line in path.read_text(encoding="utf-8").splitlines()
        if "json_body=data.model_dump(" in line
    ]

    assert dumps
    assert all("by_alias=True" in line for line in dumps), set(dumps)
