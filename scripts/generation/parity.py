# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Swagger file selection, superseded-file dropping, schema file validation, and
generated/schema service-directory parity validation.
"""

import json
import re
from pathlib import Path
from typing import TypedDict


class SwaggerFileMetadata(TypedDict):
    path: Path
    service: str
    namespace: tuple[str, ...]
    version: str
    filename: str


class SchemaValidationFailure(TypedDict):
    path: Path
    reason: str


def _swagger_file_metadata(
    swagger_path: Path, openapi_base: Path
) -> SwaggerFileMetadata:
    """Extracts normalized metadata for a swagger file path."""
    rel = swagger_path.relative_to(openapi_base)
    if len(rel.parts) < 3:
        raise ValueError(f"Unexpected swagger path shape: {rel}")

    return {
        "path": swagger_path,
        "service": rel.parts[0],
        "namespace": tuple(rel.parts[1:-2]),
        "version": rel.parts[-2],
        "filename": rel.parts[-1],
    }


_VERSION_RE = re.compile(r"^v(\d{6})\d*(?:(alpha|beta)(\d+)?)?$")
_STAGE_RANK = {"alpha": 0, "beta": 1, None: 2}


def _version_key(version: str) -> tuple[int, str, int, int, str]:
    """Orders versions by release: year-month, then alpha < beta < final, then number.

    Plain string order puts `beta10` before `beta9` and `beta2` after the final.
    An unrecognised name sorts below every recognised one, so it never wins silently.
    """
    match = _VERSION_RE.match(version)
    if match is None:
        return (0, "", 0, 0, version)
    month, stage, number = match.groups()
    return (1, month, _STAGE_RANK[stage], int(number or 0), version)


def select_latest_swagger_files_by_service(
    openapi_base: Path,
) -> tuple[dict[str, list[SwaggerFileMetadata]], int, int]:
    """Selects latest swagger per (service, namespace, filename) and groups by service."""
    all_swaggers = sorted(openapi_base.rglob("*.swagger.json"))
    latest_by_family: dict[tuple[str, tuple[str, ...], str], SwaggerFileMetadata] = {}

    for swagger_path in all_swaggers:
        metadata = _swagger_file_metadata(swagger_path, openapi_base)
        family_key = (
            metadata["service"],
            metadata["namespace"],
            metadata["filename"],
        )
        existing = latest_by_family.get(family_key)
        if existing is None or _version_key(metadata["version"]) > _version_key(
            existing["version"]
        ):
            latest_by_family[family_key] = metadata

    by_service: dict[str, list[SwaggerFileMetadata]] = {}
    for metadata in latest_by_family.values():
        service = metadata["service"]
        by_service.setdefault(service, []).append(metadata)

    for files in by_service.values():
        files.sort(
            key=lambda item: (
                item["namespace"],
                item["filename"],
                item["version"],
            )
        )

    selected_count = len(latest_by_family)
    ignored_count = len(all_swaggers) - selected_count
    return by_service, selected_count, ignored_count


def merge_local_schema_base(
    upstream: dict[str, list[SwaggerFileMetadata]],
    local: dict[str, list[SwaggerFileMetadata]],
) -> dict[str, list[SwaggerFileMetadata]]:
    """Adds the local schema base's services to upstream's.

    The local base only describes endpoints upstream does not publish, so a
    service in both means upstream now publishes it and the local copy must go.
    """
    shared = sorted(set(upstream) & set(local))
    if shared:
        raise RuntimeError(
            f"Services in both the upstream schema and the local schema base: "
            f"{', '.join(shared)}. Remove them from schema/openapi/."
        )
    return {**upstream, **local}


_HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


def _rest_modules(swagger_path: Path) -> set[str]:
    """REST modules a swagger file writes: one per operation's first tag, else `default`."""
    paths = json.loads(swagger_path.read_text(encoding="utf-8")).get("paths", {})
    return {
        (op.get("tags") or ["default"])[0].replace("-", "_").replace(" ", "_")
        for item in paths.values()
        for method, op in item.items()
        if method in _HTTP_METHODS
    }


def drop_superseded_swagger_files(
    by_service: dict[str, list[SwaggerFileMetadata]],
) -> tuple[dict[str, list[SwaggerFileMetadata]], list[SwaggerFileMetadata]]:
    """Drops each file whose REST modules newer files in its service all write.

    Two files that write one module overwrite each other, and the last one
    generated wins. An upstream file rename does this: the old version stays
    selected under its old name. Any other shared module raises, because
    neither file can be dropped safely.
    """
    kept_by_service: dict[str, list[SwaggerFileMetadata]] = {}
    dropped: list[SwaggerFileMetadata] = []
    for service, files in by_service.items():
        modules = [_rest_modules(f["path"]) for f in files]
        kept = []
        for i, metadata in enumerate(files):
            newer: set[str] = set().union(
                *(
                    modules[j]
                    for j, other in enumerate(files)
                    if _version_key(other["version"])
                    > _version_key(metadata["version"])
                )
            )
            if modules[i] and modules[i] <= newer:
                dropped.append(metadata)
            else:
                kept.append(i)

        writer: dict[str, Path] = {}
        for i in kept:
            for module in sorted(modules[i]):
                if module in writer:
                    raise RuntimeError(
                        f"{service}: {writer[module]} and {files[i]['path']} both "
                        f"write REST module `{module}`, so one would overwrite the "
                        "other. Neither is fully replaced by a newer file."
                    )
                writer[module] = files[i]["path"]
        kept_by_service[service] = [files[i] for i in kept]
    return kept_by_service, dropped


def validate_generated_service_parity(
    source_services: set[str], generated_root: Path
) -> None:
    """Fails generation if top-level generated service dirs drift from schema dirs."""
    generated_services = {
        p.name
        for p in generated_root.iterdir()
        if p.is_dir() and p.name not in ("__pycache__", "pb_companions")
    }

    missing = sorted(source_services - generated_services)
    extra = sorted(generated_services - source_services)
    if not missing and not extra:
        return

    print("\n❌ Service directory parity check failed.")
    if missing:
        print("  Missing in generated output:", ", ".join(missing))
    if extra:
        print("  Extra generated directories:", ", ".join(extra))
    raise RuntimeError(
        "Generated service directories do not match source schema top-level directories."
    )


_REQUIRED_TOP_LEVEL_KEYS = ("paths", "info")


def validate_selected_services_or_raise(
    source_services: set[str], selected_services: set[str]
) -> None:
    """Fails before the wipe on a service that the post-run parity check would reject."""
    empty = sorted(source_services - selected_services)
    if empty:
        raise RuntimeError(
            "Schema service directories without a swagger file: "
            f"{', '.join(empty)}. Generation would drop these services."
        )


def validate_schema_files(swagger_paths: list[Path]) -> list[SchemaValidationFailure]:
    """Checks each swagger file parses as JSON and has the expected top-level keys.

    Catches a corrupted/truncated local schema checkout (e.g. the 2026-08-26
    incident where a locally truncated swagger file silently produced an
    incomplete SDK) before any code is generated from it. Does not validate
    full OpenAPI schema conformance, only the structural minimum the rest
    of the generation pipeline already assumes.
    """
    failures: list[SchemaValidationFailure] = []
    for path in swagger_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            failures.append({"path": path, "reason": f"could not read file: {e}"})
            continue

        if not text.strip():
            failures.append({"path": path, "reason": "file is empty"})
            continue

        try:
            schema = json.loads(text)
        except json.JSONDecodeError as e:
            failures.append({"path": path, "reason": f"invalid JSON: {e}"})
            continue

        if not isinstance(schema, dict):
            failures.append(
                {"path": path, "reason": "top-level JSON value is not an object"}
            )
            continue

        missing_keys = [key for key in _REQUIRED_TOP_LEVEL_KEYS if key not in schema]
        if "swagger" not in schema and "openapi" not in schema:
            missing_keys.append("swagger/openapi")
        if missing_keys:
            failures.append(
                {
                    "path": path,
                    "reason": f"missing required key(s): {', '.join(missing_keys)}",
                }
            )

    return failures


def validate_schema_files_or_raise(swagger_paths: list[Path]) -> None:
    """Fails generation if any schema file is structurally invalid."""
    if not swagger_paths:
        raise RuntimeError(
            "No swagger files selected; the schema checkout is empty or the "
            "path is wrong, so nothing would be generated."
        )
    failures = validate_schema_files(swagger_paths)
    if not failures:
        return

    print("\n❌ Schema file validation failed.")
    for failure in failures:
        print(f"  {failure['path']}: {failure['reason']}")
    raise RuntimeError(
        "One or more schema files failed structural validation; the source "
        "checkout may be corrupted or truncated."
    )
