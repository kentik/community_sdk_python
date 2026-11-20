# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Track every object the mutating e2e tests create in the real account.

Each create appends a line to LEDGER_PATH before the test does anything else
with the object, and each delete appends another. An object with no delete
line is outstanding. Tests may update or delete only outstanding objects, so
they never touch data that existed before them.

Run as a script to list leftovers, and with --delete to remove them:
`uv run poe e2e-cleanup` and `uv run poe e2e-cleanup --delete`.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from kentik_api.client import KentikAPI
from kentik_api.errors import HTTPException, KentikError

NAME_PREFIX = "sdk-e2e-test"
LEDGER_PATH = Path(__file__).with_name(".created_objects.jsonl")


def _is_test_name(name: str | None) -> bool:
    # Some services store names upper-cased or reject hyphens.
    return (name or "").lower().replace("_", "-").startswith(NAME_PREFIX)


@dataclass(frozen=True)
class Kind:
    get: Callable[[KentikAPI, str], object]
    name_field: str
    delete: Callable[[KentikAPI, str], object]

    def current_name(self, client: KentikAPI, id: str) -> str | None:
        return getattr(self.get(client, id), self.name_field, None)


def _get_label(client: KentikAPI, id: str) -> object:
    for label in client.label.list().labels or []:
        if label is not None and label.id == id:
            return label
    raise HTTPException(404, f"label {id} not in the label list")


def _get_custom_application(client: KentikAPI, id: str) -> object:
    app = client.custom_application.get(customApplicationId=id).application
    # A deleted application comes back as 200 with every field empty.
    if app is None or not app.id:
        raise HTTPException(404, f"custom application {id} returned empty")
    return app


KINDS: dict[str, Kind] = {
    "label": Kind(_get_label, "name", lambda c, id: c.label.delete(id=id)),
    "site": Kind(
        lambda c, id: c.site.get(id=id).site,
        "title",
        lambda c, id: c.site.delete(id=id),
    ),
    "site_market": Kind(
        lambda c, id: c.site.get_market(id=id).siteMarket,
        "name",
        lambda c, id: c.site.delete_market(id=id),
    ),
    "as_group": Kind(
        lambda c, id: c.as_group.get(asGroupid=id).asGroup,
        "name",
        lambda c, id: c.as_group.delete(asGroupid=id),
    ),
    "flow_tag": Kind(
        lambda c, id: c.flow_tag.get(flowTagid=id).flowTag,
        "name",
        lambda c, id: c.flow_tag.delete(flowTagid=id),
    ),
    "saved_filter": Kind(
        lambda c, id: c.saved_filter.get(id=id).filter,
        "filterName",
        lambda c, id: c.saved_filter.delete(id=id),
    ),
    "custom_application": Kind(
        _get_custom_application,
        "name",
        lambda c, id: c.custom_application.delete(customApplicationId=id),
    ),
}


@dataclass(frozen=True)
class Entry:
    kind: str
    id: str
    name: str
    run: str
    time: str


class Ledger:
    def __init__(self, path: Path = LEDGER_PATH, run: str | None = None):
        self.path = path
        self.run = run or uuid.uuid4().hex[:8]

    def new_name(self) -> str:
        return f"{NAME_PREFIX}-{uuid.uuid4().hex[:8]}"

    def created(self, kind: str, id: str | None, name: str) -> str:
        assert kind in KINDS, f"no deleter for kind {kind!r}"
        assert id, f"create of {kind} {name!r} returned no id"
        assert _is_test_name(name)
        self._append("created", kind, id, name)
        return id

    def owned(self, kind: str, id: str) -> str:
        if not any(e.kind == kind and e.id == id for e in self.outstanding()):
            raise PermissionError(f"{kind} {id} was not created by an e2e test")
        return id

    def delete(self, client: KentikAPI, kind: str, id: str) -> object:
        result = KINDS[kind].delete(client, self.owned(kind, id))
        self._append("deleted", kind, id, "")
        return result

    def mark_gone(self, kind: str, id: str) -> None:
        self._append("deleted", kind, self.owned(kind, id), "")

    def outstanding(self) -> list[Entry]:
        if not self.path.exists():
            return []
        open_entries: dict[tuple[str, str], Entry] = {}
        for line in self.path.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            key = (record["kind"], record["id"])
            if record["event"] == "created":
                open_entries[key] = Entry(
                    record["kind"],
                    record["id"],
                    record["name"],
                    record["run"],
                    record["time"],
                )
            else:
                open_entries.pop(key, None)
        return list(open_entries.values())

    def _append(self, event: str, kind: str, id: str, name: str) -> None:
        record = {
            "event": event,
            "kind": kind,
            "id": id,
            "name": name,
            "run": self.run,
            "time": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


def sweep(client: KentikAPI, ledger: Ledger, entries: list[Entry]) -> list[str]:
    """Delete each entry whose object still carries the test prefix; return the failures."""
    failures = []
    for entry in entries:
        kind = KINDS[entry.kind]
        try:
            name = kind.current_name(client, entry.id)
        except KentikError as exc:
            if isinstance(exc, HTTPException) and exc.status_code == 404:
                ledger.mark_gone(entry.kind, entry.id)
                continue
            failures.append(f"{entry.kind} {entry.id}: lookup failed: {exc}")
            continue
        if not _is_test_name(name):
            failures.append(
                f"{entry.kind} {entry.id}: name is now {name!r}, not deleted"
            )
            continue
        try:
            ledger.delete(client, entry.kind, entry.id)
        except KentikError as exc:
            failures.append(f"{entry.kind} {entry.id}: delete failed: {exc}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument(
        "--delete", action="store_true", help="Delete the outstanding objects"
    )
    args = parser.parse_args()
    ledger = Ledger()
    entries = ledger.outstanding()
    for e in entries:
        print(f"{e.time}  run={e.run}  {e.kind:<19} {e.id:<12} {e.name}")
    print(f"{len(entries)} outstanding object(s) in {ledger.path}")
    if not args.delete or not entries:
        return 0
    with KentikAPI(protocol="rest") as client:
        failures = sweep(client, ledger, entries)
    for failure in failures:
        print(f"NOT CLEANED: {failure}", file=sys.stderr)
    print(f"{len(entries) - len(failures)} object(s) deleted or already gone")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
