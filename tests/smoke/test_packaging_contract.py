# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Packaging metadata the published artifacts depend on (audit findings K4 to K9, K11)."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def _floor(spec: str) -> tuple[int, ...]:
    match = re.search(r">=\s*([\d.]+)", spec)
    assert match, spec
    return tuple(int(part) for part in match.group(1).split("."))


def _dependency_floor(name: str) -> tuple[int, ...]:
    spec = next(
        s for s in PYPROJECT["project"]["dependencies"] if s.startswith(name + ">")
    )
    return _floor(spec)


def test_dotenv_floor_can_read_a_fifo():
    assert _dependency_floor("python-dotenv") >= (1, 2, 1)


def test_googleapis_floor_installs_with_protobuf_7():
    assert _dependency_floor("googleapis-common-protos") >= (1, 73, 1)


def test_build_backend_floor_supports_license_files():
    spec = next(
        s for s in PYPROJECT["build-system"]["requires"] if s.startswith("hatchling")
    )
    assert _floor(spec) >= (1, 27)


def test_sdist_ships_no_agent_or_spec_folders():
    include = PYPROJECT["tool"]["hatch"]["build"]["targets"]["sdist"]["include"]
    assert include
    assert not {".claude", ".github", ".specify", "specs"} & set(include)


def test_license_title_line_is_unmodified():
    assert "<!--" not in (ROOT / "LICENSE").read_text(encoding="utf-8")


def test_ci_syncs_with_the_lock_enforced():
    workflow = (ROOT / ".github" / "workflows" / "tests.yml").read_text("utf-8")
    assert re.search(r"run: uv sync$", workflow, re.MULTILINE) is None


def test_release_notes_wait_for_publish_and_version_is_gated():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text("utf-8")
    assert "needs: publish" in workflow
    assert "does not match tag" in workflow


def test_pypi_readme_links_resolve_on_pypi():
    readme = PYPROJECT["project"]["readme"]
    links = re.findall(r"\]\(([^)]+)\)", (ROOT / readme).read_text("utf-8"))
    assert links
    assert [link for link in links if not link.startswith("https://")] == []
    assert (
        f"/{readme}"
        in PYPROJECT["tool"]["hatch"]["build"]["targets"]["sdist"]["include"]
    )
