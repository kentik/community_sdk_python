# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""A throwaway project tree that the generator's phase modules can run against.

The phase modules read and write through module-level PROJECT_ROOT and
SDK_OUTPUT_DIR. The `sandbox` fixture copies a small slice of the real,
committed repository into tmp_path and repoints those constants at it, so the
real phase functions run end to end without a schema checkout, network, or
any write to the working tree.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

import pytest

from scripts.generation import (
    _shared,
    docs_rendering,
    endpoint_docs,
    wrapper_generation,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_PACKAGE = REPO_ROOT / "src" / "kentik_api"
REAL_GEN = REAL_PACKAGE / "gen"

SANDBOX_SERVICES = ("device", "alerting", "core")

_HAND_WRITTEN = (
    "__init__.py",
    "client.py",
    "client_mixin.py",
    "auth",
    "core",
    "errors",
    "transports",
)


@dataclass(frozen=True)
class Sandbox:
    root: Path

    @property
    def package(self) -> Path:
        return self.root / "src" / "kentik_api"

    @property
    def gen(self) -> Path:
        return self.package / "gen"

    @property
    def docs(self) -> Path:
        return self.root / "docs" / "sphinx"

    def wrapper_file(self, service: str) -> Path:
        return self.gen / service / "services" / f"{service}.py"


def _copy(src: Path, dest: Path) -> None:
    ignore = shutil.ignore_patterns("__pycache__")
    if src.is_dir():
        shutil.copytree(src, dest, ignore=ignore)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


@pytest.fixture
def sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Sandbox:
    box = Sandbox(tmp_path)

    for name in _HAND_WRITTEN:
        _copy(REAL_PACKAGE / name, box.package / name)
    _copy(REAL_GEN / "__init__.py", box.gen / "__init__.py")
    for service in SANDBOX_SERVICES:
        _copy(REAL_GEN / service, box.gen / service)

    real_docs = REPO_ROOT / "docs" / "sphinx"
    _copy(real_docs / "guides", box.docs / "guides")
    _copy(real_docs / "README.md", box.docs / "README.md")
    _copy(real_docs / "index.md", box.docs / "index.md")
    _copy(REPO_ROOT / "pyproject.toml", box.root / "pyproject.toml")

    gen = box.gen
    for module in (_shared, docs_rendering, endpoint_docs, wrapper_generation):
        if hasattr(module, "PROJECT_ROOT"):
            monkeypatch.setattr(module, "PROJECT_ROOT", box.root)
        if hasattr(module, "SDK_OUTPUT_DIR"):
            monkeypatch.setattr(module, "SDK_OUTPUT_DIR", gen)
    monkeypatch.setattr(docs_rendering, "_GUIDES_DIR", box.docs / "guides")
    return box
