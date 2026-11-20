# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Examples cannot silently rot (FR-044, SC-013).

Importing a module only defines main(), so a renamed wrapper method would still
import cleanly. Each example's `client.<service>.<method>(...)` calls are also
resolved against a real client, keyword arguments included. Nothing is sent:
KentikAPI builds its transport lazily and no example's main() runs.
"""

from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path

import pytest

from kentik_api.client import KentikAPI

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"
MODULES = sorted(
    ".".join(path.relative_to(EXAMPLES.parent).with_suffix("").parts)
    for path in EXAMPLES.rglob("*.py")
    if path.name != "__init__.py"
)


def _client_calls(source: str) -> list[tuple[str, str, list[str], int]]:
    """(service, method, keyword names, line) for each `client.X.Y(...)` call."""
    calls = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        service = node.func.value
        if (
            isinstance(service, ast.Attribute)
            and isinstance(service.value, ast.Name)
            and service.value.id == "client"
        ):
            keywords = [kw.arg for kw in node.keywords if kw.arg is not None]
            calls.append((service.attr, node.func.attr, keywords, node.lineno))
    return calls


@pytest.fixture(scope="module")
def client():
    with KentikAPI(email="dev@example.com", api_token="token") as client:
        yield client


def test_every_example_is_discovered():
    assert len(MODULES) >= 13
    assert "examples.common.error_handling" in MODULES


@pytest.mark.parametrize("module_name", MODULES)
def test_example_imports_without_network_or_credentials(module_name):
    module = importlib.import_module(module_name)

    assert callable(getattr(module, "main", None)), f"{module_name} has no main()"


@pytest.mark.parametrize("module_name", MODULES)
def test_example_calls_resolve_to_real_wrapper_methods(module_name, client):
    path = EXAMPLES.parent / Path(*module_name.split(".")).with_suffix(".py")

    for service, method_name, keywords, line in _client_calls(path.read_text()):
        where = f"{module_name}:{line}"
        wrapper = getattr(client, service, None)
        assert wrapper is not None, f"{where}: client has no service {service!r}"
        method = getattr(wrapper, method_name, None)
        assert method is not None, f"{where}: {service} has no method {method_name!r}"
        try:
            inspect.signature(method).bind_partial(**dict.fromkeys(keywords))
        except TypeError as exc:
            pytest.fail(f"{where}: {service}.{method_name} rejects {keywords}: {exc}")


@pytest.mark.parametrize(
    "module_name", [m for m in MODULES if m.endswith((".rest", ".grpc"))]
)
def test_every_transport_example_calls_the_api(module_name):
    path = EXAMPLES.parent / Path(*module_name.split(".")).with_suffix(".py")

    assert _client_calls(path.read_text()), (
        f"{module_name} makes no client.<service>.<method>() call"
    )
