# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Verifies every mounted wrapper builds a live gRPC stub.

Generated wrapper `__init__` catches `(ImportError, TypeError)` around its proto
imports and sets the stub to None. That is correct for an environment without the
proto dependencies, but it also swallows a descriptor-pool failure caused by the
generator itself, and every later call then raises NotImplementedError as if the
operation simply had no gRPC translation yet.

That is exactly what happened: protoc's dependency imports look unused, `ruff
--select F --fix` deleted them, and 10 of 28 services lost gRPC entirely while the
suite stayed green. These tests make that failure mode loud.
"""

from __future__ import annotations

import ast
import importlib
import json
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from kentik_api.transports.grpc_client import GrpcTransport
from scripts.generation.api_surface import is_rest_only

_MIXIN = Path(__file__).resolve().parents[2] / "src" / "kentik_api" / "client_mixin.py"
_GEN = _MIXIN.parent / "gen"
_SURFACE = _MIXIN.parents[2] / "api_surface.json"


def _rest_only() -> set[str]:
    """Services from the local schema base: no protos, mounted on a REST transport."""
    if not _SURFACE.exists():
        return set()
    services = json.loads(_SURFACE.read_text(encoding="utf-8"))["services"]
    return {name for name, record in services.items() if is_rest_only(record)}


def _mounted_wrappers() -> list[tuple[str, str]]:
    """Reads the mixin's imports with ast, so a wrapped or aliased import still counts."""
    if not _MIXIN.exists():
        return []
    rest_only = _rest_only()
    found = set()
    for node in ast.walk(ast.parse(_MIXIN.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            parts = node.module.split(".")
            if (
                parts[:2] == ["kentik_api", "gen"]
                and parts[3:4] == ["services"]
                and parts[2] not in rest_only
            ):
                found.update((parts[2], alias.name) for alias in node.names)
    return sorted(found)


MOUNTED = _mounted_wrappers()

if not MOUNTED:
    pytest.skip("client_mixin.py not generated yet", allow_module_level=True)


def _build(service: str, wrapper_class: str):
    module = importlib.import_module(f"kentik_api.gen.{service}.services.{service}")
    transport = MagicMock(spec=GrpcTransport)
    transport.channel = MagicMock()
    return getattr(module, wrapper_class)(transport)


@pytest.mark.parametrize(
    ("service", "wrapper_class"), MOUNTED, ids=[svc for svc, _ in MOUNTED]
)
def test_mounted_wrapper_builds_live_grpc_stubs(service: str, wrapper_class: str):
    wrapper = _build(service, wrapper_class)
    stubs = {
        name: value
        for name, value in vars(wrapper).items()
        if name.startswith("_grpc_stub")
    }

    assert stubs, (
        f"`{wrapper_class}` declared no gRPC stub attribute at all. Either the "
        "generator found no proto for this service, or wrapper generation changed "
        "shape and this guard needs updating."
    )
    dead = sorted(name for name, value in stubs.items() if value is None)
    assert not dead, (
        f"`client.{service}` built {dead} as None, so every gRPC call on it raises "
        "NotImplementedError. The wrapper swallowed an ImportError or TypeError "
        f"while importing kentik_api.gen.{service}.pb. Import that module directly "
        "to see the real error; a descriptor-pool TypeError means a dependency "
        "import was dropped from a generated _pb2 module."
    )


@pytest.mark.parametrize(
    ("service", "wrapper_class"), MOUNTED, ids=[svc for svc, _ in MOUNTED]
)
def test_mounted_wrapper_proto_module_imports_cleanly(service: str, wrapper_class: str):
    """Surfaces the underlying error the wrapper's except clause would hide."""
    wrapper_src = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "kentik_api"
        / "gen"
        / service
        / "services"
        / f"{service}.py"
    ).read_text(encoding="utf-8")
    modules = re.findall(r"import (kentik_api\.gen\.\w+\.pb\.\w+_pb2) as", wrapper_src)
    if not modules:
        pytest.skip(f"{service} wrapper imports no proto module")

    importlib.import_module("kentik_api.gen.pb_companions")
    for module in modules:
        importlib.import_module(module)


def test_a_failed_proto_import_names_its_cause(monkeypatch):
    monkeypatch.setitem(sys.modules, "kentik_api.gen.device.pb.device_pb2", None)
    wrapper = _build("device", "DeviceServiceWrapper")

    with pytest.raises(NotImplementedError, match="failed to import") as exc_info:
        wrapper.list()

    assert isinstance(exc_info.value.__cause__, ImportError)
    assert "device_pb2" in str(exc_info.value)


def test_every_service_with_a_wrapper_is_checked_here():
    with_wrapper = {
        path.parent.parent.name for path in _GEN.glob("*/services/*ServiceWrapper*.py")
    } or {
        p.parent.parent.name
        for p in _GEN.glob("*/services/*.py")
        if "ServiceWrapper" in p.read_text(encoding="utf-8")
    }

    assert {svc for svc, _ in MOUNTED} == with_wrapper - _rest_only()
