# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Every third-party import is declared, and the inventory page lists exactly the declared set."""

from __future__ import annotations

import ast
import re
import sys
import tomllib
from importlib.metadata import packages_distributions
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import NormalizedName, canonicalize_name

ROOT = Path(__file__).resolve().parents[2]
SCANNED = ("src", "scripts", "tests")
INVENTORY = ROOT / "docs" / "sphinx" / "dependencies.md"
PROJECT_NAME = "kentik-api"


def _declared() -> set[NormalizedName]:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    specs = [
        *pyproject["project"]["dependencies"],
        *(
            s
            for extra in pyproject["project"]["optional-dependencies"].values()
            for s in extra
        ),
        *(s for group in pyproject["dependency-groups"].values() for s in group),
        *pyproject["build-system"]["requires"],
    ]
    names = {
        canonicalize_name(Requirement(s).name) for s in specs if isinstance(s, str)
    }
    return names - {PROJECT_NAME}


def _first_party() -> set[str]:
    names = {"kentik_api", *SCANNED}
    names |= {p.name for p in ROOT.iterdir() if (p / "__init__.py").exists()}
    for top in SCANNED:
        for path in (ROOT / top).rglob("*"):
            if path.suffix == ".py" or (
                path.is_dir() and (path / "__init__.py").exists()
            ):
                names.add(path.stem)
    return names


def _third_party_imports() -> dict[str, set[str]]:
    """Top-level module name to the files that import it."""
    skip = set(sys.stdlib_module_names) | _first_party()
    found: dict[str, set[str]] = {}
    for top in SCANNED:
        for path in (ROOT / top).rglob("*.py"):
            for node in ast.walk(ast.parse(path.read_bytes())):
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif (
                    isinstance(node, ast.ImportFrom) and node.level == 0 and node.module
                ):
                    modules = [node.module]
                else:
                    continue
                for module in modules:
                    name = module.split(".")[0]
                    if name not in skip:
                        found.setdefault(name, set()).add(str(path.relative_to(ROOT)))
    return found


def test_every_third_party_import_is_declared():
    declared = _declared()
    owners = packages_distributions()
    undeclared = {
        module: sorted(files)
        for module, files in _third_party_imports().items()
        if not declared & {canonicalize_name(d) for d in owners.get(module, [])}
    }
    assert not undeclared, f"Declare these in pyproject.toml: {undeclared}"


def test_inventory_lists_exactly_the_declared_dependencies():
    rows = re.findall(
        r"^\| `?([A-Za-z][A-Za-z0-9._-]*)`? \|",
        INVENTORY.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    listed = {canonicalize_name(name) for name in rows} - {"dependency"}
    declared = _declared()
    assert listed == declared, (
        f"Missing rows: {sorted(declared - listed)}; extra rows: {sorted(listed - declared)}"
    )
