# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Documentation and tooling facts the audit found wrong (findings D7 to D10)."""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_docs_contain_no_literal_backslash_n():
    for path in (ROOT / "docs" / "sphinx").glob("*.md"):
        assert "\\n" not in path.read_text(encoding="utf-8"), path.name


def test_changelog_command_does_not_name_a_tag_without_a_surface_record():
    assert "SINCE=v1.0.7" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_poe_lists_every_task():
    with (ROOT / "pyproject.toml").open("rb") as f:
        tasks = tomllib.load(f)["tool"]["poe"]["tasks"]
    result = subprocess.run(
        [sys.executable, "-m", "poethepoet", "--no-ansi"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = result.stdout + result.stderr
    listed = {line.split()[0] for line in output.splitlines() if line.startswith("  ")}
    assert set(tasks) <= listed, output


def test_agent_file_starts_with_front_matter():
    text = (ROOT / ".github" / "agents" / "kentik-sdk-autogen.agent.md").read_text(
        encoding="utf-8"
    )
    assert text.startswith("---\n")


def test_install_docs_upgrade_past_one_x():
    for name in ("README.md", "docs/sphinx/guides/quickstart.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert 'pip install -U "kentik-api>=2"' in text, name
