"""Finds REST writes whose URL sets a field nested in a message that the body also carries.

Lists every google.api.http rule that has a body, creates included.
For a google.api.http rule with `body: "*"` and a path variable such as
`{as_group.id}`, grpc-gateway merges the URL value and the JSON body into one
request message. The body uses the proto3 JSON name of the field (`asGroup`),
and the path uses the proto name (`as_group`). Every proto3 JSON parser must
accept both names, so the two must land on the same field. The live Kentik
REST API does not do that: it keeps the object it builds from the URL and
drops the body. This script lists every rule where the two names differ.

Reads the descriptors that protoc serialized into the SDK's `_pb2.py` files,
so it checks exactly the schema commit pinned in `schema.lock`.

Usage, from the SDK repo root:

    uv run python reports/scripts/rest-body-merge/audit.py         # table
    uv run python reports/scripts/rest-body-merge/audit.py --json  # machine-readable
"""

from __future__ import annotations

import argparse
import importlib
import json
import pathlib
import re

from google.api import annotations_pb2

import kentik_api.gen.pb_companions  # noqa: F401  registers shared protos

GEN = pathlib.Path("src/kentik_api/gen")
VAR_RE = re.compile(r"\{([^}=]+)")


def http_rules(rule):
    yield rule
    for extra in rule.additional_bindings:
        yield from http_rules(extra)


def renamed_segments(message, var: str) -> list[str]:
    """The segments of a dotted path field whose proto name differs from its JSON name."""
    renamed = []
    for segment in var.split("."):
        field = message.fields_by_name[segment]
        if field.json_name != field.name:
            renamed.append(f"{field.name}/{field.json_name}")
        message = field.message_type
    return renamed


def verdict_for(rule_body: str, request, var: str) -> str:
    if rule_body != "*":
        return f"body is one field ({rule_body})"
    if "." not in var:
        return "flat path field"
    renamed = renamed_segments(request, var)
    if not renamed:
        return "same key"
    top = var.split(".")[0]
    if renamed[0].startswith(f"{top}/"):
        return "AFFECTED"
    return "leaf renamed only"


def audit() -> list[dict]:
    rows = []
    for pb2_path in sorted(GEN.glob("*/pb/*_pb2.py")):
        module = importlib.import_module(".".join(pb2_path.with_suffix("").parts[1:]))
        for service in module.DESCRIPTOR.services_by_name.values():
            for method in service.methods:
                options = method.GetOptions()
                if not options.HasExtension(annotations_pb2.http):
                    continue
                for rule in http_rules(options.Extensions[annotations_pb2.http]):
                    verb = rule.WhichOneof("pattern")
                    if verb is None or not rule.body:
                        continue
                    path = getattr(rule, verb)
                    request = method.input_type
                    base = {
                        "service": pb2_path.parts[-3],
                        "rpc": f"{service.name}.{method.name}",
                        "verb": verb.upper(),
                        "path": path,
                        "body": rule.body,
                    }
                    path_vars = VAR_RE.findall(path)
                    if not path_vars:
                        # Body keys whose proto name differs: the merge cannot hit them, a parser can.
                        renamed = [
                            f"{f.name}/{f.json_name}"
                            for f in request.fields
                            if rule.body == "*" and f.json_name != f.name
                        ]
                        rows.append(
                            base
                            | {
                                "path_field": "",
                                "renamed": ", ".join(renamed),
                                "verdict": "no path field",
                            }
                        )
                    for var in path_vars:
                        rows.append(
                            base
                            | {
                                "path_field": var,
                                "renamed": ", ".join(renamed_segments(request, var)),
                                "verdict": verdict_for(rule.body, request, var),
                            }
                        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows = audit()
    if args.json:
        print(json.dumps(rows, indent=2))
        return
    for r in sorted(
        rows,
        key=lambda r: (
            r["verdict"] != "AFFECTED",
            r["verdict"],
            r["service"],
            r["rpc"],
        ),
    ):
        print(
            f"{r['verdict']:<28} {r['service']:<20} {r['rpc']:<55} "
            f"{r['verb']:<6} {r['path']}  body={r['body']}  {r['renamed']}"
        )
    rank = [
        "AFFECTED",
        "leaf renamed only",
        "same key",
        "flat path field",
        "body is one field",
        "no path field",
    ]
    worst: dict[tuple, str] = {}
    for r in rows:
        key = (r["service"], r["rpc"], r["verb"], r["path"])
        verdict = str(r["verdict"]).split(" (")[0]
        worst[key] = min(worst.get(key) or verdict, verdict, key=rank.index)
    counts = {v: list(worst.values()).count(v) for v in rank}
    print(f"{len(worst)} rules with a body, by worst verdict: {counts}")


if __name__ == "__main__":
    main()
