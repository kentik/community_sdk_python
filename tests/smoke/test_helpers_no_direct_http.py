# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Hand-written helpers reach the API only through generated operations (FR-007).

Every request must go through request_json(), so a helper module that imports
httpx or request_json is a second connection path (constitution Principle II).
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_PACKAGE = Path(__file__).resolve().parents[2] / "src" / "kentik_api"
_HELPERS = sorted(
    path
    for path in [
        _PACKAGE / "v5_tools.py",
        _PACKAGE / "devices.py",
        *(_PACKAGE / "analytics").glob("*.py"),
    ]
    if path.exists()
)


def _imported_names(path: Path) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add(node.module or "")
            names.update(alias.name for alias in node.names)
    return names


@pytest.mark.parametrize("path", _HELPERS, ids=[p.name for p in _HELPERS])
def test_helper_sends_no_http_itself(path: Path):
    names = _imported_names(path)

    assert "httpx" not in names
    assert "request_json" not in names
    assert "kentik_api.core.rest_runtime" not in names
