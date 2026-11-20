# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Renders release notes by diffing `api_surface.json` against an earlier git revision.

`uv run poe generate` refreshes `api_surface.json` on every run, and it is committed, so
comparing two points in history costs one `git show`. That keeps this command
idempotent: rerunning it never consumes or advances a baseline, unlike a snapshot
file that gets overwritten as a side effect of generation.

    uv run python scripts/release_notes.py                 # since the previous release
    uv run python scripts/release_notes.py --since v1.0.6
    uv run python scripts/release_notes.py --since HEAD    # just this working tree
    uv run python scripts/release_notes.py -o notes.md
    uv run python scripts/release_notes.py --check-changelog --since origin/main

`--check-changelog` prints nothing on success. It exits 1 when a breaking change
since the baseline has no mention in CHANGELOG.md's Unreleased section.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from packaging.version import InvalidVersion, Version

sys.path.insert(0, str(Path(__file__).parent))

from generation import api_surface
from generation._shared import PROJECT_ROOT, write_text_lf

SURFACE_RELPATH = "api_surface.json"
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"
NO_RECORD_REASON = (
    "Surface records start with the V6 rewrite. That rewrite replaces the "
    "unmaintained kentik-api 1.x completely, so it starts from scratch: no "
    "earlier revision has a record to compare with. CHANGELOG.md's Unreleased "
    "section and docs/sphinx/guides/migrating-from-1x.md describe the change."
)


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=PROJECT_ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _version(tag: str) -> Version | None:
    try:
        return Version(tag)
    except InvalidVersion:
        return None


def _earlier_releases_newest_first() -> list[str]:
    """Release tags reachable from HEAD, highest version first, excluding HEAD's.

    Reachability keeps a hotfix branch from comparing against a newer minor made
    elsewhere, and version order beats tag date for the same reason. The release
    workflow runs on the tag it describes, so HEAD's own tags are skipped. A
    final release skips pre-releases, so `v1.1.0` compares against `v1.0.x`, not
    `v1.1.0rc1`.
    """
    head_tags = set(_git("tag", "--points-at", "HEAD").split())
    head_versions = [v for v in map(_version, head_tags) if v is not None]
    allow_pre = bool(head_versions) and all(v.is_prerelease for v in head_versions)
    releases = []
    for tag in _git("tag", "--merged", "HEAD").split():
        version = _version(tag)
        if tag in head_tags or version is None:
            continue
        if version.is_prerelease and not allow_pre:
            continue
        releases.append((version, tag))
    return [tag for _, tag in sorted(releases, reverse=True)]


def _default_baseline() -> tuple[str, dict] | None:
    """Finds the previous release that actually carries a surface record.

    Tags predating surface tracking have no record, so skipping to the newest one
    that has a record beats failing outright.
    """
    for tag in _earlier_releases_newest_first():
        surface = api_surface.recorded_at(tag)
        if surface is not None:
            return tag, surface
    return None


def _require_commit(ref: str) -> None:
    try:
        _git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    except RuntimeError:
        raise SystemExit(
            f"--since `{ref}` does not name a commit in this repository. Check "
            "the spelling, or fetch it first: a shallow clone lacks older history."
        ) from None


def _unreleased_notes() -> str:
    text = CHANGELOG.read_text(encoding="utf-8")
    match = re.search(
        r"^## Unreleased\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    return match.group(1) if match else ""


def _mentioned(name: str, notes: str) -> bool:
    """True when a code span in the notes holds `name` as a whole token.

    A bare substring would let prose such as "user credentials" satisfy a
    removed `user` service.
    """
    token = re.compile(rf"(?<![\w]){re.escape(name)}(?![\w])")
    return any(token.search(span) for span in re.findall(r"`([^`]+)`", notes))


def _check_changelog(delta: dict, since: str) -> None:
    notes = _unreleased_notes()
    missing = [
        (message, name)
        for message, name in api_surface.breaking_changes(delta)
        if not _mentioned(name, notes)
    ]
    if not missing:
        return
    print(
        f"CHANGELOG.md's Unreleased section does not mention these breaking "
        f"changes since `{since}`. Add an entry that names each one:",
        file=sys.stderr,
    )
    for message, name in missing:
        print(f"{message}  (mention `{name}`)", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since",
        metavar="REF",
        help="git ref to compare against (default: previous release tag carrying a surface record)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="write markdown here instead of stdout",
    )
    parser.add_argument(
        "--check-changelog",
        action="store_true",
        help="fail if CHANGELOG.md does not mention every breaking change",
    )
    args = parser.parse_args()

    surface_path = PROJECT_ROOT / SURFACE_RELPATH
    if not surface_path.exists():
        raise SystemExit(
            f"{SURFACE_RELPATH} is missing. Run `uv run poe generate` first."
        )
    after = api_surface.read(surface_path)

    if args.since:
        _require_commit(args.since)
        before = api_surface.recorded_at(args.since)
        baseline = None if before is None else (args.since, before)
    else:
        baseline = _default_baseline()

    if args.check_changelog:
        if baseline is None:
            print(
                f"No surface record at `{args.since or 'any release tag'}`, so "
                f"there is nothing to check.\n{NO_RECORD_REASON}",
                file=sys.stderr,
            )
            return
        since, before = baseline
        _check_changelog(api_surface.diff(before, after), since)
        return

    if baseline is not None:
        since, before = baseline
        print(f"Comparing against {since}", file=sys.stderr)
        markdown = api_surface.render_markdown(
            api_surface.diff(before, after), since=since
        )
    elif args.since:
        raise SystemExit(
            f"`{SURFACE_RELPATH}` does not exist at `{args.since}`, so there is "
            "nothing to compare against. That revision predates surface "
            "tracking. Pick a later ref, or omit --since to use the newest "
            "tag that has a record."
        )
    else:
        print(
            "No tagged release carries a surface record yet, so there is no "
            "baseline to diff against. Showing the current surface instead.\n"
            f"{NO_RECORD_REASON}\n"
            "Future releases will produce a change list automatically.",
            file=sys.stderr,
        )
        markdown = api_surface.render_summary(after)

    if args.output:
        write_text_lf(args.output, markdown)
        print(f"Wrote release notes to {args.output}", file=sys.stderr)
    else:
        print(markdown, end="")


if __name__ == "__main__":
    main()
