# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Writes a regeneration impact report: what a `uv run poe generate` run changed.

Run it after regenerating, before committing. It compares the working tree
against a git ref and records the facts: schema commit, changed files by kind,
API surface delta, toolchain floors, and check results. Judgment (severity,
what to do) stays with a person, in the report's empty Findings section.

    uv run python scripts/impact_report.py                  # vs HEAD, with checks
    uv run python scripts/impact_report.py --since v1.0.7
    uv run python scripts/impact_report.py --no-checks
    uv run python scripts/impact_report.py -o /tmp/impact.html

The report goes to `reports/`, which is not tracked, because it describes one
working tree at one moment.
"""

from __future__ import annotations

import argparse
import datetime
import html
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generation import api_surface
from generation._shared import PROJECT_ROOT, write_text_lf

SURFACE_RELPATH = "api_surface.json"
REPORTS_DIR = PROJECT_ROOT / "reports"
DEFAULT_SCHEMA_REPO = PROJECT_ROOT.parent / "api-schema-public"

GENERATED_PREFIXES = (
    "src/kentik_api/gen/",
    "src/kentik_api/client_mixin.py",
    "docs/sphinx/",
    SURFACE_RELPATH,
)

# protoc stamps its own version into every stub. A diff made only of these
# lines means the toolchain moved, not the schema.
_VERSION_ONLY_LINE = re.compile(
    r"^[+-](\s*# Protobuf Python Version: [\d.]+"
    r'|GRPC_GENERATED_VERSION = "[\d.]+"'
    r"|\s*\d+,)\s*$"
)

KINDS = {
    "pb-toolchain": "Proto stubs, toolchain version only",
    "pb": "Proto stubs, content",
    "models": "Models",
    "services": "Service wrappers and REST modules",
    "errors": "Error packages",
    "mount": "Client mount (`client_mixin.py`)",
    "surface": "API surface record",
    "docs": "Generated docs and READMEs",
    "other": "Outside the generated paths",
}


def _run(*args: str, cwd: Path = PROJECT_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


def _git(*args: str, cwd: Path = PROJECT_ROOT) -> str:
    result = _run("git", *args, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def is_toolchain_only(diff_text: str) -> bool:
    """True when every changed line in a -U0 diff is a protoc version stamp."""
    changed = [
        line
        for line in diff_text.splitlines()
        if line[:1] in "+-" and not line.startswith(("+++", "---"))
    ]
    return bool(changed) and all(_VERSION_ONLY_LINE.match(line) for line in changed)


def classify(path: str, diff_text: str = "") -> str:
    """Sorts one changed path into a KINDS key."""
    if not path.startswith(GENERATED_PREFIXES):
        return "other"
    if path == SURFACE_RELPATH:
        return "surface"
    if path.endswith("client_mixin.py"):
        return "mount"
    if path.startswith("docs/") or path.endswith("README.md"):
        return "docs"
    parts = path.split("/")
    if "pb" in parts or "pb_companions" in parts:
        return "pb-toolchain" if is_toolchain_only(diff_text) else "pb"
    for part, kind in (
        ("models", "models"),
        ("services", "services"),
        ("error", "errors"),
    ):
        if part in parts:
            return kind
    return "other"


def changed_files(since: str) -> dict[str, list[str]]:
    """Groups every path that differs from `since`, untracked files included."""
    groups: dict[str, list[str]] = {kind: [] for kind in KINDS}
    for line in _git("diff", "--name-only", since).splitlines():
        diff_text = _git("diff", "-U0", since, "--", line) if "/pb" in line else ""
        groups[classify(line, diff_text)].append(line)
    for line in _git("ls-files", "--others", "--exclude-standard").splitlines():
        groups[classify(line)].append(f"{line} (new)")
    return groups


def schema_commit(schema_repo: Path) -> str:
    if not (schema_repo / ".git").exists():
        return f"unknown (no git checkout at `{schema_repo}`)"
    try:
        return _git("log", "-1", "--format=%h %cs", cwd=schema_repo)
    except RuntimeError as exc:
        return f"unknown ({exc})"


def floor_check(surface: dict) -> list[str]:
    """One line per gencode version, saying whether its declared floor covers it."""

    def version(raw: str) -> tuple[int, ...]:
        return tuple(int(part) for part in re.findall(r"\d+", raw))

    lines = []
    for package, gencode in sorted(surface.get("gencode", {}).items()):
        requirement = surface.get("requirements", {}).get(package)
        floor = re.search(r"[><=]=\s*([\d.]+)", requirement or "")
        ok = floor is not None and version(floor.group(1)) >= version(gencode)
        verdict = "covered" if ok else "**NOT covered: raise the floor**"
        lines.append(
            f"| `{package}` | `{gencode}` | `{requirement or 'not declared'}` | {verdict} |"
        )
    return lines


def run_checks() -> list[tuple[str, str]]:
    """Last summary line of each check. Failures are reported, never raised."""
    commands = {
        "pytest": ("uv", "run", "pytest", "-q", "-p", "no:cacheprovider"),
        "ruff": ("uv", "run", "ruff", "check"),
        "ty": ("uv", "run", "ty", "check"),
    }
    results = []
    for name, command in commands.items():
        print(f"Running {name}...", file=sys.stderr)
        result = _run(*command)
        output = (result.stdout + result.stderr).strip().splitlines()
        results.append((name, output[-1] if output else f"exit {result.returncode}"))
    return results


def render_markdown(
    *,
    since: str,
    schema: str,
    groups: dict[str, list[str]],
    surface_delta: str,
    floors: list[str],
    checks: list[tuple[str, str]] | None,
) -> str:
    today = datetime.date.today().isoformat()
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    total = sum(len(paths) for paths in groups.values())

    lines = [
        "# Regeneration Impact Report",
        "",
        "| | |",
        "| --- | --- |",
        f"| Date | {today} |",
        f"| Branch | `{branch}` |",
        f"| Compared against | `{since}` |",
        f"| Schema commit | {schema} |",
        f"| Changed files | {total} |",
        "",
        "## Findings",
        "",
        "_Not generated. Record severity, impact, and what to do here._",
        "",
        "## Change inventory",
        "",
        "| Kind | Files |",
        "| --- | --- |",
    ]
    lines += [
        f"| {KINDS[kind]} | {len(paths)} |" for kind, paths in groups.items() if paths
    ]
    if groups["pb-toolchain"]:
        lines += [
            "",
            (
                f"{len(groups['pb-toolchain'])} proto stubs changed only the protoc version "
                "stamp. That is toolchain churn, not a schema change."
            ),
        ]
    if groups["other"]:
        lines += [
            "",
            (
                "**Files outside the generated paths changed.** A regeneration should not "
                "touch these, unless you edited them yourself:"
            ),
            "",
            *(f"- `{path}`" for path in groups["other"]),
        ]
    for kind, paths in groups.items():
        if paths and kind not in ("pb-toolchain", "other"):
            lines += ["", f"### {KINDS[kind]}", "", *(f"- `{path}`" for path in paths)]

    lines += ["", "## API surface", "", surface_delta.strip()]
    lines += [
        "",
        "## Toolchain floors",
        "",
        "| Package | Gencode | Declared | Verdict |",
        "| --- | --- | --- | --- |",
        *floors,
    ]
    lines += ["", "## Checks", ""]
    if checks is None:
        lines.append("_Skipped with `--no-checks`._")
    else:
        lines += ["| Check | Result |", "| --- | --- |"]
        lines += [f"| {name} | `{result}` |" for name, result in checks]
    return "\n".join(lines) + "\n"


_STYLE = """
:root { --fg: #1d1d1f; --bg: #fff; --muted: #6e6e73; --line: #d2d2d7; --code: #f5f5f7; }
@media (prefers-color-scheme: dark) {
  :root { --fg: #f5f5f7; --bg: #1d1d1f; --muted: #a1a1a6; --line: #424245; --code: #2c2c2e; }
}
body { font: 15px/1.5 system-ui, sans-serif; color: var(--fg); background: var(--bg);
  max-width: 960px; margin: 0 auto; padding: 24px 16px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid var(--line); padding: 6px 10px; text-align: left; }
code { background: var(--code); padding: 1px 4px; border-radius: 4px; }
em { color: var(--muted); }
"""


def to_html(markdown: str) -> str:
    from markdown_it import MarkdownIt

    body = MarkdownIt("commonmark").enable("table").render(markdown)
    title = html.escape(f"Regeneration Impact {datetime.date.today().isoformat()}")
    return (
        f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{title}</title>\n<style>{_STYLE}</style>\n</head>\n"
        f"<body>\n{body}</body>\n</html>\n"
    )


def default_output() -> Path:
    """Never overwrites an earlier report, including a hand-written one."""
    stem = f"regeneration-impact-{datetime.date.today().isoformat()}"
    candidate, n = REPORTS_DIR / f"{stem}.html", 2
    while candidate.exists():
        candidate, n = REPORTS_DIR / f"{stem}-{n}.html", n + 1
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", default="HEAD", metavar="REF", help="default: HEAD")
    parser.add_argument(
        "--schema-repo",
        type=Path,
        default=DEFAULT_SCHEMA_REPO,
        help="schema checkout the run used (default: ../api-schema-public)",
    )
    parser.add_argument(
        "--no-checks", action="store_true", help="skip pytest, ruff, ty"
    )
    parser.add_argument(
        "-o", "--output", type=Path, help="default: reports/<dated>.html"
    )
    args = parser.parse_args()

    surface_path = PROJECT_ROOT / SURFACE_RELPATH
    if not surface_path.exists():
        raise SystemExit(
            f"{SURFACE_RELPATH} is missing. Run `uv run poe generate` first."
        )
    after = api_surface.read(surface_path)
    before = api_surface.recorded_at(args.since)
    surface_delta = (
        f"_`{SURFACE_RELPATH}` does not exist at `{args.since}`, so there is no "
        "surface to compare against._"
        if before is None
        else api_surface.render_markdown(
            api_surface.diff(before, after), since=args.since
        )
    )

    markdown = render_markdown(
        since=args.since,
        schema=schema_commit(args.schema_repo),
        groups=changed_files(args.since),
        surface_delta=surface_delta,
        floors=floor_check(after),
        checks=None if args.no_checks else run_checks(),
    )

    output = args.output or default_output()
    if output.parent == REPORTS_DIR and not REPORTS_DIR.exists():
        REPORTS_DIR.mkdir()
        write_text_lf(REPORTS_DIR / ".gitignore", "*\n")
    write_text_lf(output, to_html(markdown))
    print(
        f"Wrote {output.relative_to(PROJECT_ROOT) if output.is_relative_to(PROJECT_ROOT) else output}"
    )


if __name__ == "__main__":
    main()
