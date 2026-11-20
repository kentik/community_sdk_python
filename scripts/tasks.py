# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Poe script tasks for the steps that would otherwise need a POSIX shell."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_GENERATED = ("src/kentik_api/gen", "docs/build", "docs/sphinx/services")
_CACHES = (".pytest_cache", ".ruff_cache")
# Too slow to walk, and never holds project bytecode.
_SKIP_WALK = {".git", ".venv"}


def clean(root: Path = ROOT) -> None:
    """Removes the generated SDK, the docs build, and every __pycache__."""
    for rel in _GENERATED:
        shutil.rmtree(root / rel, ignore_errors=True)
    for dirpath, dirnames, _ in os.walk(root):
        for name in list(dirnames):
            if name in _SKIP_WALK:
                dirnames.remove(name)
            elif name == "__pycache__":
                shutil.rmtree(Path(dirpath) / name, ignore_errors=True)
                dirnames.remove(name)


def deep_clean(root: Path = ROOT) -> None:
    """clean(), then the tool caches and .venv. uv.lock is tracked and kept."""
    clean(root)
    for rel in _CACHES:
        shutil.rmtree(root / rel, ignore_errors=True)
    venv = root / ".venv"
    # Windows cannot delete the interpreter that runs this task.
    if sys.platform == "win32" and Path(sys.prefix).resolve().is_relative_to(
        venv.resolve()
    ):
        print("Kept .venv: it holds the running poe. Remove it after poe exits:")
        print("  Remove-Item -Recurse -Force .venv")
        return
    shutil.rmtree(venv, ignore_errors=True)


def check_drift(root: Path = ROOT) -> None:
    """Exits 1 when the working tree differs from the commit, naming each path."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    if not result.stdout.strip():
        return
    print("Generated output differs from the commit, or is untracked:")
    print(result.stdout, end="")
    print("A change altered generator output, or schema.lock names a commit the tree")
    print("was not generated from. Run `uv run poe generate` and commit the result.")
    raise SystemExit(1)
