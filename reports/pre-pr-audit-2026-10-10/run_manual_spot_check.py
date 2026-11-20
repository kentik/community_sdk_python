#!/usr/bin/env python3
"""Run one manual spot check and append a structured run record.

This helper runs exactly one check per invocation, records sanitized details,
and appends a markdown summary plus a JSON artifact.
"""

# ruff: noqa: E402
from __future__ import annotations

import argparse
import copy
import json
import os
import shlex
import subprocess
import sys
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kentik_api.client import KentikAPI
from kentik_api.core.api_config import APIConfig
from kentik_api.errors import ConfigurationError, KentikError
from kentik_api.gen.user.models import ListUsersResponse

DEFAULT_OUTPUT_FILE = REPORT_DIR / "manual-spot-check-output.md"
DEFAULT_ARTIFACT_DIR = REPORT_DIR / "manual-spot-check-artifacts"


@dataclass(frozen=True)
class CheckDefinition:
    check_id: str
    finding_id: str
    finding: str
    description: str
    live_candidate: bool
    runner: Callable[[], dict[str, Any]]


REMEDIATION_STATES = ("open", "in_progress", "fixed", "deferred")


def _now_utc() -> datetime:
    return datetime.now(tz=UTC)


def _iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


def _timestamp_slug(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def _relative_to_project(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(resolved)


def _users_count(response: ListUsersResponse) -> int:
    return len([user for user in (response.users or []) if user is not None])


def _exc_dict(exc: BaseException) -> dict[str, str]:
    return {
        "type": f"{type(exc).__module__}.{type(exc).__name__}",
        "message": str(exc).splitlines()[0] if str(exc) else "",
    }


def _tail(text: str, max_lines: int = 30, max_chars: int = 1600) -> str:
    lines = text.splitlines()
    tail_text = "\n".join(lines[-max_lines:])
    if len(tail_text) <= max_chars:
        return tail_text
    trimmed = tail_text[:max_chars]
    remainder = len(tail_text) - max_chars
    return f"{trimmed}\n[truncated {remainder} chars]"


def _run_python_probe(relative_path: str, timeout_seconds: int = 30) -> dict[str, Any]:
    script_path = PROJECT_ROOT / relative_path
    command = [sys.executable, str(script_path)]
    started = _now_utc()
    try:
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        finished = _now_utc()
        return {
            "command": " ".join(shlex.quote(part) for part in command),
            "exit_code": completed.returncode,
            "timed_out": False,
            "duration_seconds": round((finished - started).total_seconds(), 3),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired as exc:
        finished = _now_utc()
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        return {
            "command": " ".join(shlex.quote(part) for part in command),
            "exit_code": None,
            "timed_out": True,
            "duration_seconds": round((finished - started).total_seconds(), 3),
            "stdout": stdout,
            "stderr": stderr,
        }


def _probe_summary(probe_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "command": probe_result["command"],
        "exit_code": probe_result["exit_code"],
        "timed_out": probe_result["timed_out"],
        "duration_seconds": probe_result["duration_seconds"],
        "stdout_tail": _tail(probe_result["stdout"]),
        "stderr_tail": _tail(probe_result["stderr"]),
    }


def run_c1() -> dict[str, Any]:
    """B13: e2e target and verdict logic probes (local, no live API call)."""
    target = _run_python_probe(
        "reports/pre-pr-audit-2026-10-10/evidence/tests/e2e_target_probe.py",
        timeout_seconds=40,
    )
    logic = _run_python_probe(
        "reports/pre-pr-audit-2026-10-10/evidence/tests/e2e_logic_probe.py",
        timeout_seconds=40,
    )

    target_text = f"{target['stdout']}\n{target['stderr']}"
    logic_text = f"{logic['stdout']}\n{logic['stderr']}"

    markers = {
        "wrong_host_marker": "api.example.com" in target_text,
        "false_pass_marker": "401" in logic_text and "PASS" in logic_text,
    }

    reproduced = (
        target["exit_code"] == 0
        and logic["exit_code"] == 0
        and markers["wrong_host_marker"]
        and markers["false_pass_marker"]
    )

    verdict = "reproduced" if reproduced else "inconclusive"
    summary = (
        "C1 markers observed in local probes."
        if reproduced
        else "C1 did not clearly reproduce from local probe output."
    )

    return {
        "verdict": verdict,
        "summary": summary,
        "live_api_used": False,
        "details": {
            "markers": markers,
            "target_probe": _probe_summary(target),
            "logic_probe": _probe_summary(logic),
        },
    }


def run_c2() -> dict[str, Any]:
    """B5: malformed credentials leak into error text path (local probe)."""
    probe = _run_python_probe(
        "reports/pre-pr-audit-2026-10-10/evidence/rest/token_leak.py",
        timeout_seconds=40,
    )

    text = f"{probe['stdout']}\n{probe['stderr']}"
    marker_present = "s3cr3t-token-value" in text
    reproduced = probe["exit_code"] == 0 and marker_present

    return {
        "verdict": "reproduced" if reproduced else "inconclusive",
        "summary": (
            "C2 token leak marker found in probe output."
            if reproduced
            else "C2 did not clearly reproduce from local probe output."
        ),
        "live_api_used": False,
        "details": {
            "token_leak_marker_present": marker_present,
            "probe": _probe_summary(probe),
        },
    }


def run_c3() -> dict[str, Any]:
    """B6: gRPC use-after-close crash probe (isolated subprocess)."""
    probe = _run_python_probe(
        "reports/pre-pr-audit-2026-10-10/evidence/rest/grpc_use_after_close.py",
        timeout_seconds=20,
    )

    exit_code = probe["exit_code"]
    segfault_like = exit_code in (-11, 139)
    reproduced = segfault_like

    if probe["timed_out"]:
        verdict = "inconclusive"
        summary = "C3 timed out before producing a definitive crash signal."
    elif reproduced:
        verdict = "reproduced"
        summary = "C3 returned a segfault-style exit code in subprocess."
    elif exit_code == 0:
        verdict = "not_reproduced"
        summary = "C3 completed without crash in this environment."
    else:
        verdict = "inconclusive"
        summary = "C3 returned a non-zero exit code without segfault marker."

    return {
        "verdict": verdict,
        "summary": summary,
        "live_api_used": False,
        "details": {
            "segfault_like_exit": segfault_like,
            "probe": _probe_summary(probe),
        },
    }


def run_c4() -> dict[str, Any]:
    """B7: compare override behavior on REST vs gRPC using live read-only calls."""
    details: dict[str, Any] = {}
    live_api_used = False

    override_bad = APIConfig(
        base_path="https://127.0.0.1:1",
        auth_email="override-user@example.invalid",
        auth_token="override-token",
        timeout=5,
    )
    override_no_creds = APIConfig(timeout=5)

    try:
        with KentikAPI(protocol="rest", env_file=".env", timeout=20) as rest_client:
            rest_baseline = rest_client.user.list()
            live_api_used = True
            details["rest_baseline_user_count"] = _users_count(rest_baseline)

            try:
                rest_client.user.list(api_config_override=override_bad)
                details["rest_bad_override"] = {"outcome": "succeeded"}
            except Exception as exc:  # pragma: no cover - runtime behavior capture
                details["rest_bad_override"] = {
                    "outcome": "failed",
                    "error": _exc_dict(exc),
                }

            try:
                rest_client.user.list(api_config_override=override_no_creds)
                details["rest_no_creds_override"] = {"outcome": "succeeded"}
            except Exception as exc:  # pragma: no cover - runtime behavior capture
                details["rest_no_creds_override"] = {
                    "outcome": "failed",
                    "error": _exc_dict(exc),
                }

        with KentikAPI(
            protocol="grpc",
            env_file=".env",
            timeout=20,
            grpc_deadline=20,
        ) as grpc_client:
            grpc_baseline = grpc_client.user.list()
            live_api_used = True
            details["grpc_baseline_user_count"] = _users_count(grpc_baseline)

            try:
                grpc_client.user.list(api_config_override=override_bad)
                details["grpc_bad_override"] = {"outcome": "succeeded"}
            except Exception as exc:  # pragma: no cover - runtime behavior capture
                details["grpc_bad_override"] = {
                    "outcome": "failed",
                    "error": _exc_dict(exc),
                }

            try:
                grpc_client.user.list(api_config_override=override_no_creds)
                details["grpc_no_creds_override"] = {"outcome": "succeeded"}
            except Exception as exc:  # pragma: no cover - runtime behavior capture
                details["grpc_no_creds_override"] = {
                    "outcome": "failed",
                    "error": _exc_dict(exc),
                }
    finally:
        override_bad.close()
        override_no_creds.close()

    rest_bad_failed = details.get("rest_bad_override", {}).get("outcome") == "failed"
    rest_no_creds_failed = (
        details.get("rest_no_creds_override", {}).get("outcome") == "failed"
    )
    rest_no_creds_is_cfg_error = (
        details.get("rest_no_creds_override", {})
        .get("error", {})
        .get("type", "")
        .endswith("ConfigurationError")
    )
    grpc_bad_succeeded = (
        details.get("grpc_bad_override", {}).get("outcome") == "succeeded"
    )
    grpc_no_creds_succeeded = (
        details.get("grpc_no_creds_override", {}).get("outcome") == "succeeded"
    )

    if (
        rest_bad_failed
        and rest_no_creds_failed
        and rest_no_creds_is_cfg_error
        and grpc_bad_succeeded
        and grpc_no_creds_succeeded
    ):
        verdict = "reproduced"
        summary = (
            "C4 reproduced: REST override paths fail as expected, while gRPC override "
            "paths still succeed."
        )
    elif rest_bad_failed and rest_no_creds_failed and not grpc_bad_succeeded:
        verdict = "not_reproduced"
        summary = "C4 not reproduced: gRPC override no longer succeeded with invalid override."
    else:
        verdict = "inconclusive"
        summary = (
            "C4 completed but did not produce a clean reproduce/not-reproduced split."
        )

    return {
        "verdict": verdict,
        "summary": summary,
        "live_api_used": live_api_used,
        "details": details,
    }


def run_c5() -> dict[str, Any]:
    """B1: use a live payload, then mutate enum to check exception class behavior."""
    details: dict[str, Any] = {}
    live_api_used = False

    with KentikAPI(protocol="rest", env_file=".env", timeout=20) as client:
        response = client.user.list()
        live_api_used = True
        details["live_user_count"] = _users_count(response)
        payload = response.model_dump(by_alias=True, exclude_none=False)

    users = payload.get("users") or []
    target_index = next(
        (index for index, user in enumerate(users) if isinstance(user, dict)),
        None,
    )

    if target_index is None:
        return {
            "verdict": "inconclusive",
            "summary": "C5 needs at least one user record from the live account payload.",
            "live_api_used": live_api_used,
            "details": details,
        }

    mutated_payload = copy.deepcopy(payload)
    mutated_payload["users"][target_index]["defaultLandingPageType"] = (
        "LANDING_TYPE_SPOT_CHECK_UNKNOWN"
    )

    try:
        ListUsersResponse.model_validate(mutated_payload)
    except Exception as exc:  # pragma: no cover - runtime behavior capture
        escapes_kentik_error = not isinstance(exc, KentikError)
        details["validation_error"] = _exc_dict(exc)
        details["escapes_kentik_error"] = escapes_kentik_error

        return {
            "verdict": "reproduced" if escapes_kentik_error else "not_reproduced",
            "summary": (
                "C5 reproduced: unknown enum path raised outside KentikError hierarchy."
                if escapes_kentik_error
                else "C5 not reproduced: exception remained inside KentikError hierarchy."
            ),
            "live_api_used": live_api_used,
            "details": details,
        }

    details["validation_error"] = None
    details["escapes_kentik_error"] = False
    return {
        "verdict": "not_reproduced",
        "summary": "C5 not reproduced: mutated payload validated without error.",
        "live_api_used": live_api_used,
        "details": details,
    }


def _checks() -> dict[str, CheckDefinition]:
    return {
        "C1": CheckDefinition(
            check_id="C1",
            finding_id="B13",
            finding="B13 e2e targets wrong host and false-pass rule",
            description="Local reproduction probes for host target and e2e pass/fail logic.",
            live_candidate=False,
            runner=run_c1,
        ),
        "C2": CheckDefinition(
            check_id="C2",
            finding_id="B5",
            finding="B5 malformed credential leaks token in error text",
            description="Local malformed-credential probe for token leakage in error messages.",
            live_candidate=False,
            runner=run_c2,
        ),
        "C3": CheckDefinition(
            check_id="C3",
            finding_id="B6",
            finding="B6 gRPC use-after-close crashes process",
            description="Crash probe in isolated subprocess to avoid taking down the parent shell.",
            live_candidate=False,
            runner=run_c3,
        ),
        "C4": CheckDefinition(
            check_id="C4",
            finding_id="B7",
            finding="B7 gRPC override ignores credential and host override",
            description="Live read-only REST and gRPC comparison with invalid per-call override.",
            live_candidate=True,
            runner=run_c4,
        ),
        "C5": CheckDefinition(
            check_id="C5",
            finding_id="B1",
            finding="B1 unknown enum value can escape KentikError path",
            description="Live read-only payload fetch, then local enum mutation and validation replay.",
            live_candidate=True,
            runner=run_c5,
        ),
    }


def _load_sensitive_values() -> dict[str, str]:
    sensitive: dict[str, str] = {}

    env_from_file = dotenv_values(PROJECT_ROOT / ".env")
    for key in ("KENTIK_EMAIL", "KENTIK_API_TOKEN"):
        value = env_from_file.get(key)
        if isinstance(value, str) and value:
            sensitive[value] = key

    for key in ("KENTIK_EMAIL", "KENTIK_API_TOKEN"):
        value = os.getenv(key)
        if value:
            sensitive[value] = key

    return sensitive


def _sanitize_text(text: str, sensitive: dict[str, str]) -> str:
    sanitized = text
    for value, key in sorted(
        sensitive.items(), key=lambda item: len(item[0]), reverse=True
    ):
        sanitized = sanitized.replace(value, f"<REDACTED:{key}>")
    return sanitized


def _sanitize_data(data: Any, sensitive: dict[str, str]) -> Any:
    if isinstance(data, str):
        return _sanitize_text(data, sensitive)
    if isinstance(data, dict):
        return {
            str(key): _sanitize_data(value, sensitive) for key, value in data.items()
        }
    if isinstance(data, list):
        return [_sanitize_data(item, sensitive) for item in data]
    return data


def _ensure_output_file(output_file: Path) -> None:
    if output_file.exists():
        return
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        "# Manual spot-check output log\n\n"
        "Each entry is appended by run_manual_spot_check.py and links to a "
        "structured JSON artifact.\n\n",
        encoding="utf-8",
    )


def _append_markdown_record(
    output_file: Path,
    *,
    result: dict[str, Any],
    artifact_path: Path,
    notes: str,
) -> None:
    rel_artifact = _relative_to_project(artifact_path)
    details_json = json.dumps(result["details"], indent=2, sort_keys=True)

    entry = (
        f"## {result['started_at']} {result['check_id']}\n\n"
        f"- Finding: {result['finding']}\n"
        f"- Verdict: {result['verdict']}\n"
        f"- Live API used: {'yes' if result['live_api_used'] else 'no'}\n"
        f"- Artifact: {rel_artifact}\n"
    )
    if notes:
        entry += f"- Operator notes: {notes}\n"

    remediation_update = result.get("remediation_state_update")
    if isinstance(remediation_update, dict):
        entry += f"- Remediation state: {remediation_update.get('state', '')}\n"
        if remediation_update.get("verification_gate"):
            entry += (
                f"- Verification gate: {remediation_update.get('verification_gate')}\n"
            )
        if remediation_update.get("state_owner"):
            entry += f"- State owner: {remediation_update.get('state_owner')}\n"
        if remediation_update.get("defer_reason"):
            entry += f"- Defer reason: {remediation_update.get('defer_reason')}\n"
        if remediation_update.get("mitigation"):
            entry += f"- Mitigation: {remediation_update.get('mitigation')}\n"
        if remediation_update.get("revisit_trigger"):
            entry += f"- Revisit trigger: {remediation_update.get('revisit_trigger')}\n"

    entry += f"\nSummary: {result['summary']}\n\n```json\n{details_json}\n```\n\n"

    with output_file.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def _run_one_check(
    check: CheckDefinition,
    *,
    notes: str,
    output_file: Path,
    artifact_dir: Path,
    remediation_state_update: dict[str, Any] | None,
) -> dict[str, Any]:
    started = _now_utc()
    try:
        run_result = check.runner()
    except ConfigurationError as exc:
        run_result = {
            "verdict": "error",
            "summary": "Missing or invalid SDK credential/configuration.",
            "live_api_used": False,
            "details": {
                "error": _exc_dict(exc),
            },
        }
    except Exception as exc:  # pragma: no cover - defensive guardrail
        run_result = {
            "verdict": "error",
            "summary": "Runner crashed before the check completed.",
            "live_api_used": False,
            "details": {
                "error": _exc_dict(exc),
                "traceback": traceback.format_exc(),
            },
        }

    finished = _now_utc()

    result: dict[str, Any] = {
        "check_id": check.check_id,
        "finding": check.finding,
        "description": check.description,
        "live_candidate": check.live_candidate,
        "started_at": _iso(started),
        "finished_at": _iso(finished),
        "duration_seconds": round((finished - started).total_seconds(), 3),
        "verdict": run_result.get("verdict", "inconclusive"),
        "summary": run_result.get("summary", "No summary returned."),
        "live_api_used": bool(run_result.get("live_api_used", False)),
        "details": run_result.get("details", {}),
    }

    if notes:
        result["operator_notes"] = notes

    if remediation_state_update is not None:
        result["remediation_state_update"] = remediation_state_update

    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_name = f"{_timestamp_slug(started)}-{check.check_id}.json"
    artifact_path = artifact_dir / artifact_name

    result["artifact_path"] = _relative_to_project(artifact_path)
    result["output_log_path"] = _relative_to_project(output_file)

    if remediation_state_update is not None:
        update_block = result.get("remediation_state_update", {})
        if isinstance(update_block, dict):
            update_block["recorded_at"] = _iso(_now_utc())
            update_block["evidence"] = {
                "check_id": check.check_id,
                "verdict": result["verdict"],
                "artifact_path": result["artifact_path"],
                "output_log_path": result["output_log_path"],
            }

    sensitive = _load_sensitive_values()
    result = _sanitize_data(result, sensitive)

    artifact_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    _ensure_output_file(output_file)
    _append_markdown_record(
        output_file,
        result=result,
        artifact_path=artifact_path,
        notes=notes,
    )
    return result


def _print_checks(checks: dict[str, CheckDefinition]) -> None:
    print("Available spot checks:")
    for check_id in sorted(checks):
        check = checks[check_id]
        live_marker = "yes" if check.live_candidate else "no"
        print(
            f"  {check.check_id} ({check.finding_id}): "
            f"live={live_marker} | {check.finding}"
        )
    print("\nRun one check:")
    print(
        "  uv run python reports/pre-pr-audit-2026-10-10/run_manual_spot_check.py "
        "run --check C4"
    )


def _build_remediation_state_update(
    *,
    check: CheckDefinition,
    remediation_state: str,
    verification_gate: str,
    state_owner: str,
    defer_reason: str,
    mitigation: str,
    revisit_trigger: str,
    state_notes: str,
) -> dict[str, Any] | None:
    if not remediation_state:
        return None

    normalized_state = remediation_state.strip()
    normalized_gate = verification_gate.strip()
    normalized_owner = state_owner.strip()
    normalized_reason = defer_reason.strip()
    normalized_mitigation = mitigation.strip()
    normalized_trigger = revisit_trigger.strip()
    normalized_notes = state_notes.strip()

    missing: list[str] = []
    if normalized_state == "fixed" and not normalized_gate:
        missing.append("--verification-gate")
    if normalized_state == "deferred":
        if not normalized_owner:
            missing.append("--state-owner")
        if not normalized_reason:
            missing.append("--defer-reason")
        if not normalized_mitigation:
            missing.append("--mitigation")
        if not normalized_trigger:
            missing.append("--revisit-trigger")

    if missing:
        options = ", ".join(missing)
        raise ValueError(
            "Missing required options for remediation state "
            f"'{normalized_state}': {options}"
        )

    update: dict[str, Any] = {
        "finding_id": check.finding_id,
        "finding_summary": check.finding,
        "state": normalized_state,
    }

    if normalized_gate:
        update["verification_gate"] = normalized_gate
    if normalized_owner:
        update["state_owner"] = normalized_owner
    if normalized_reason:
        update["defer_reason"] = normalized_reason
    if normalized_mitigation:
        update["mitigation"] = normalized_mitigation
    if normalized_trigger:
        update["revisit_trigger"] = normalized_trigger
    if normalized_notes:
        update["state_notes"] = normalized_notes

    return update


def build_parser(check_ids: list[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run one pre-PR manual spot check and append a structured output record."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available checks.")

    run_parser = subparsers.add_parser("run", help="Run one check and record output.")
    run_parser.add_argument("--check", choices=check_ids, required=True)
    run_parser.add_argument(
        "--notes",
        default="",
        help="Optional operator notes to include in the run record.",
    )
    run_parser.add_argument(
        "--output-file",
        default=str(DEFAULT_OUTPUT_FILE),
        help="Markdown log file to append (default: manual-spot-check-output.md).",
    )
    run_parser.add_argument(
        "--artifact-dir",
        default=str(DEFAULT_ARTIFACT_DIR),
        help="Directory for JSON artifacts (default: manual-spot-check-artifacts).",
    )
    run_parser.add_argument(
        "--remediation-state",
        choices=REMEDIATION_STATES,
        default="",
        help=(
            "Optional finding state update to store with this check "
            "(open, in_progress, fixed, deferred)."
        ),
    )
    run_parser.add_argument(
        "--verification-gate",
        default="",
        help="Verification gate label. Required when --remediation-state fixed.",
    )
    run_parser.add_argument(
        "--state-owner",
        default="",
        help="State owner label. Required when --remediation-state deferred.",
    )
    run_parser.add_argument(
        "--defer-reason",
        default="",
        help="Deferral reason. Required when --remediation-state deferred.",
    )
    run_parser.add_argument(
        "--mitigation",
        default="",
        help="Mitigation plan. Required when --remediation-state deferred.",
    )
    run_parser.add_argument(
        "--revisit-trigger",
        default="",
        help="Revisit trigger. Required when --remediation-state deferred.",
    )
    run_parser.add_argument(
        "--state-notes",
        default="",
        help="Optional short note for the remediation-state update.",
    )

    return parser


def main() -> int:
    checks = _checks()
    parser = build_parser(sorted(checks))
    args = parser.parse_args()

    if args.command == "list":
        _print_checks(checks)
        return 0

    selected_check = checks[args.check]
    output_file = Path(args.output_file)
    artifact_dir = Path(args.artifact_dir)

    try:
        remediation_state_update = _build_remediation_state_update(
            check=selected_check,
            remediation_state=args.remediation_state,
            verification_gate=args.verification_gate,
            state_owner=args.state_owner,
            defer_reason=args.defer_reason,
            mitigation=args.mitigation,
            revisit_trigger=args.revisit_trigger,
            state_notes=args.state_notes,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    result = _run_one_check(
        selected_check,
        notes=args.notes,
        output_file=output_file,
        artifact_dir=artifact_dir,
        remediation_state_update=remediation_state_update,
    )

    print(f"Check {result['check_id']} finished with verdict: {result['verdict']}")
    print(f"Summary: {result['summary']}")
    print(f"Log entry: {result['output_log_path']}")
    print(f"Artifact: {result['artifact_path']}")

    remediation_update = result.get("remediation_state_update")
    if isinstance(remediation_update, dict):
        print(
            "Remediation state recorded: "
            f"{remediation_update.get('state')} for "
            f"{remediation_update.get('finding_id')}"
        )

    return 2 if result["verdict"] == "error" else 0


if __name__ == "__main__":
    raise SystemExit(main())
