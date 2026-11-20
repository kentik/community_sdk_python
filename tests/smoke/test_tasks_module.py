# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""scripts/tasks.py: the poe tasks that replace POSIX shell commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts import tasks

REMOVED = ("src/kentik_api/gen", "docs/build", "docs/sphinx/services")
KEPT = (
    "scripts/openapi_templates/service.jinja2",
    "src/kentik_api/core/rest_runtime.py",
    "docs/sphinx/local_generation_workflow.md",
)


def _tree(root: Path) -> None:
    for rel in REMOVED:
        (root / rel / "x").mkdir(parents=True)
    for rel in KEPT:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("kept\n", encoding="utf-8")
    (root / "scripts" / "__pycache__").mkdir()
    (root / "src" / "kentik_api" / "core" / "__pycache__").mkdir()
    for rel in (".venv/bin", ".pytest_cache", ".ruff_cache"):
        (root / rel).mkdir(parents=True)


def test_clean_removes_generated_output_and_bytecode(tmp_path: Path):
    _tree(tmp_path)
    tasks.clean(tmp_path)
    for rel in REMOVED:
        assert not (tmp_path / rel).exists(), rel
    assert not list(tmp_path.rglob("__pycache__"))
    for rel in KEPT:
        assert (tmp_path / rel).is_file(), rel
    assert (tmp_path / ".venv").is_dir()


def test_deep_clean_removes_caches_and_venv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    _tree(tmp_path)
    monkeypatch.setattr(sys, "platform", "linux")
    tasks.deep_clean(tmp_path)
    for rel in (".venv", ".pytest_cache", ".ruff_cache", "src/kentik_api/gen"):
        assert not (tmp_path / rel).exists(), rel


def test_deep_clean_keeps_the_running_venv_on_windows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    _tree(tmp_path)
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setattr(sys, "prefix", str(tmp_path / ".venv"))
    tasks.deep_clean(tmp_path)
    assert (tmp_path / ".venv").is_dir()
    assert not (tmp_path / ".pytest_cache").exists()
    assert "Remove-Item -Recurse -Force .venv" in capsys.readouterr().out


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    (tmp_path / "a.txt").write_text("a\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(
        tmp_path,
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@example.com",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-q",
        "-m",
        "init",
    )
    return tmp_path


def test_check_drift_passes_on_a_clean_tree(
    repo: Path, capsys: pytest.CaptureFixture[str]
):
    tasks.check_drift(repo)
    assert capsys.readouterr().out == ""


def test_check_drift_fails_and_names_each_path(
    repo: Path, capsys: pytest.CaptureFixture[str]
):
    (repo / "a.txt").write_text("b\n", encoding="utf-8")
    (repo / "new.txt").write_text("n\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        tasks.check_drift(repo)
    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "a.txt" in out and "new.txt" in out
    assert "uv run poe generate" in out
