# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Verifies every REST path parameter is encoded into its own segment.

An unencoded id like "../../user/7" would send `device.delete` to another
resource, so every placeholder of every operation is checked, not a sample.
"""

from __future__ import annotations

import importlib
import inspect
import re
from pathlib import Path
from typing import Any

import pytest
from _discovery import WrapperCase, build_all_kwargs, discover_cases

from scripts.generation._shared import parse_generated_rest_module

ALL_CASES = discover_cases()

_PLACEHOLDER_ARG = re.compile(r"\{(\w+)\}")
_HOSTILE = "../x?y#z"
_ENCODED = "..%2Fx%3Fy%23z"


class _Stop(Exception):
    """Ends the call once the path is captured."""


@pytest.mark.parametrize(
    "case",
    ALL_CASES,
    ids=[f"{case.wrapper_class}.{case.method_name}" for case in ALL_CASES],
)
def test_every_path_parameter_stays_in_its_segment(
    case: WrapperCase, monkeypatch: pytest.MonkeyPatch
):
    module = importlib.import_module(case.module_path)
    rest_module = getattr(module, case.rest_module_alias)
    (op,) = [
        op
        for op in parse_generated_rest_module(Path(inspect.getfile(rest_module)))
        if op.name == case.rest_function_name
    ]
    path_args = _PLACEHOLDER_ARG.findall(op.path)
    if not path_args:
        pytest.skip("operation has no path parameters")

    captured: dict[str, Any] = {}

    def _request_json(method, path, **_):
        captured["path"] = path
        raise _Stop

    monkeypatch.setattr(rest_module, "request_json", _request_json)
    function = getattr(rest_module, case.rest_function_name)
    kwargs = build_all_kwargs(function) | dict.fromkeys(path_args, _HOSTILE)

    with pytest.raises(_Stop):
        function(**kwargs)

    assert captured["path"] == _PLACEHOLDER_ARG.sub(_ENCODED, op.path)
