# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Facts about the poe task table and the files that agents read (spec 007)."""

from __future__ import annotations

import re
import shlex
import subprocess
import sys
import tomllib
from importlib.metadata import version
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / ".claude" / "skills" / "poethepoet"

_MAKE_SCAN_SKIPS = (
    *(f"specs/00{n}-" for n in range(1, 8)),
    "reports/",
    ".specify/",
    ".github/skills/",
    ".claude/skills/",
    "tests/smoke/test_task_runner.py",
)
_FORMER_TARGETS = {"help", "install", "services", "local", "tests"}


def _poe() -> dict[str, Any]:
    with (ROOT / "pyproject.toml").open("rb") as f:
        return tomllib.load(f)["tool"]["poe"]


def _keys(node: object) -> set[str]:
    if isinstance(node, dict):
        return set(node) | {k for v in node.values() for k in _keys(v)}
    if isinstance(node, list):
        return {k for v in node for k in _keys(v)}
    return set()


def test_every_task_has_help():
    tasks = _poe()["tasks"]
    assert tasks
    for name, task in tasks.items():
        assert isinstance(task, dict), f"{name} has no table, so it has no help"
        help_text = task.get("help", "")
        assert help_text.strip(), f"{name} has no help"
        assert "\n" not in help_text, f"{name} help is longer than one line"


def test_no_task_loads_an_env_file():
    assert "envfile" not in _keys(_poe())


def test_no_task_uses_a_shell():
    for name, task in _poe()["tasks"].items():
        assert "shell" not in task, f"{name} needs a shell, which Windows lacks"


def _dry_run(*argv: str) -> list[str]:
    result = subprocess.run(
        [sys.executable, "-m", "poethepoet", "--no-ansi", "-d", *argv],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    line = next(
        x
        for x in (result.stdout + result.stderr).splitlines()
        if x.startswith("Poe => ")
    )
    return shlex.split(line.removeprefix("Poe => "))[2:]


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["generate"], []),
        (["generate", "--local"], ["--local-repo", "../api-schema-public/"]),
        (["generate", "--local-repo", "a b/c"], ["--local-repo", "a b/c"]),
        (["generate", "--schema-ref", "REF"], ["--schema-ref", "REF"]),
        (
            ["check-changelog", "--since", "REF"],
            ["--check-changelog", "--since", "REF"],
        ),
        (
            ["release-notes", "--since", "REF", "--out", "o.md"],
            ["--since", "REF", "-o", "o.md"],
        ),
        (
            ["impact-report", "--since", "REF", "--no-checks", "--out", "o.html"],
            ["--since", "REF", "--no-checks", "-o", "o.html"],
        ),
    ],
)
def test_task_options_reach_the_program(argv: list[str], expected: list[str]):
    assert _dry_run(*argv) == expected


def test_agent_skill_matches_locked_poe():
    skill = (SKILL_DIR / "version.txt").read_text(encoding="utf-8").strip()
    assert skill == version("poethepoet"), (
        "The poe agent skill is stale. Run: uv run poe _install_skill .claude/skills --upgrade"
    )


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout


def test_agents_md_is_a_regular_file_and_claude_md_imports_it():
    # A committed symlink checks out on Windows as a file holding only its target.
    mode = _git("ls-files", "-s", "AGENTS.md").split()[0]
    assert mode == "100644", "AGENTS.md must be a regular file, not a link"
    assert (ROOT / "CLAUDE.md").read_text(encoding="utf-8").strip() == "@AGENTS.md"


def test_no_make_commands_outside_past_specs():
    targets = sorted(set(_poe()["tasks"]) | _FORMER_TARGETS, key=len, reverse=True)
    pattern = re.compile(
        rf"\bmake (?:{'|'.join(map(re.escape, targets))})\b|\bMakefile\b"
    )
    found = []
    for rel in _git("ls-files").splitlines():
        if rel.startswith(_MAKE_SCAN_SKIPS) or not (ROOT / rel).is_file():
            continue
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        found += [
            f"{rel}:{n}: {line.strip()}"
            for n, line in enumerate(text.splitlines(), 1)
            if pattern.search(line)
        ]
    assert not found, "Name the poe task instead:\n" + "\n".join(found)
