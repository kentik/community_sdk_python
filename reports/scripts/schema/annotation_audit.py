"""Audits api-schema-public for HTTP-annotation coverage and service visibility.

Reproduces the evidence in the two upstream ticket reports in this directory.
Counts annotations per RPC block rather than per file, so a single RPC carrying
`additional_bindings` is not double counted.

Usage, from the SDK repo root with ../api-schema-public checked out:

    uv run python reports/scripts/schema/annotation_audit.py
"""

from __future__ import annotations

import json
import pathlib
import re

SCHEMA = pathlib.Path("../api-schema-public")
PROTO = SCHEMA / "proto" / "kentik"
SWAGGER = SCHEMA / "gen" / "openapiv2" / "kentik"

RPC_RE = re.compile(r"^\s*rpc\s+(\w+)\s*\(")
SERVICE_RE = re.compile(r"^\s*service\s+(\w+)")
VISIBILITY_RE = re.compile(r"\(kentik\.core\.v\d+\.visibility\)\s*=\s*(\w+)")


def rpc_blocks(lines: list[str]) -> list[tuple[str, int, str]]:
    """Yields (rpc_name, 1-based line, block text) for each rpc in a proto file.

    Brace counting is enough here: the schema never nests braces inside an rpc
    body beyond the option blocks we care about.
    """
    blocks = []
    for index, line in enumerate(lines):
        match = RPC_RE.match(line)
        if not match:
            continue
        depth, body, cursor = 0, [], index
        while cursor < len(lines):
            body.append(lines[cursor])
            depth += lines[cursor].count("{") - lines[cursor].count("}")
            if depth <= 0 and cursor > index:
                break
            if depth == 0 and lines[cursor].rstrip().endswith(";"):
                break
            cursor += 1
        blocks.append((match.group(1), index + 1, "\n".join(body)))
    return blocks


def latest_version(service_dir: pathlib.Path) -> pathlib.Path | None:
    versions = sorted(
        (p for p in service_dir.iterdir() if p.is_dir()), key=lambda p: p.name
    )
    return versions[-1] if versions else None


def audit() -> list[dict]:
    rows = []
    for service_dir in sorted(p for p in PROTO.iterdir() if p.is_dir()):
        version_dir = latest_version(service_dir)
        if version_dir is None:
            continue

        total, annotated, visibilities, unannotated = 0, 0, set(), []
        for proto in sorted(version_dir.glob("*.proto")):
            lines = proto.read_text(encoding="utf-8", errors="replace").splitlines()
            current_service = None
            for line in lines:
                service_match = SERVICE_RE.match(line)
                if service_match:
                    current_service = service_match.group(1)
                visibility_match = VISIBILITY_RE.search(line)
                if visibility_match and current_service:
                    visibilities.add((current_service, visibility_match.group(1)))
            for name, line_no, body in rpc_blocks(lines):
                total += 1
                if "google.api.http" in body:
                    annotated += 1
                else:
                    unannotated.append(
                        f"{proto.relative_to(SCHEMA)}:{line_no} rpc {name}"
                    )

        paths = 0
        swagger_dir = SWAGGER / service_dir.name / version_dir.name
        if swagger_dir.is_dir():
            for swagger in swagger_dir.glob("*.swagger.json"):
                try:
                    paths += len(
                        json.loads(swagger.read_text(encoding="utf-8")).get("paths", {})
                    )
                except json.JSONDecodeError:
                    pass

        if total:
            rows.append(
                {
                    "service": service_dir.name,
                    "version": version_dir.name,
                    "rpcs": total,
                    "annotated": annotated,
                    "paths": paths,
                    "visibilities": sorted(visibilities),
                    "unannotated": unannotated,
                }
            )
    return rows


def main() -> None:
    rows = audit()

    print(
        f"{'SERVICE':<22}{'VERSION':<18}{'RPCS':>5}{'ANNOTATED':>11}{'PATHS':>7}  VISIBILITY"
    )
    print("-" * 92)
    for row in rows:
        visibility = ",".join(
            sorted(
                {v.replace("SERVICE_VISIBILITY_", "") for _, v in row["visibilities"]}
            )
        )
        flag = "  <== NO REST SURFACE" if row["annotated"] == 0 else ""
        print(
            f"{row['service']:<22}{row['version']:<18}{row['rpcs']:>5}"
            f"{row['annotated']:>11}{row['paths']:>7}  {visibility or '(none)'}{flag}"
        )

    gaps = [r for r in rows if r["annotated"] == 0]
    print(f"\n{len(gaps)} of {len(rows)} services expose zero REST surface:\n")
    for row in gaps:
        visibility = ",".join(sorted({v for _, v in row["visibilities"]}))
        print(f"  {row['service']} ({visibility}), {row['rpcs']} RPCs:")
        for entry in row["unannotated"]:
            print(f"      {entry}")

    print("\nServices annotated non-public:\n")
    for row in rows:
        for service, visibility in row["visibilities"]:
            if "PUBLIC" not in visibility or visibility.endswith("PUBLIC_KENTIK"):
                print(
                    f"  {row['service']}.{service}: {visibility}"
                    f"  (REST paths published: {row['paths']})"
                )


if __name__ == "__main__":
    main()
