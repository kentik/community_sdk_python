# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The public name of every Service, client method, and model.

`public_names.json` maps each public name to what the schema calls that thing
today. A run adds an entry for each new thing and never changes an existing
one, so an upstream rename cannot rename the SDK. When an entry no longer
matches the schema, generation fails and names the entry to point elsewhere.
"""

import json
import keyword
import re
from collections.abc import Iterable
from pathlib import Path

from ._shared import INTERNAL_GEN_DIRS, PROJECT_ROOT, normalize_symbol, write_text_lf

NAMES_FILE = PROJECT_ROOT / "public_names.json"

_PATH_VERSION = re.compile(r"/v\d+(?:alpha\d*|beta\d*)?(?=/|$)")
_PLACEHOLDER = re.compile(r"\{[^{}]*\}")
# Six or more digits, so `Ipv4Address` is not a version.
_NAME_VERSION = re.compile(r"v\d{6,}(?:alpha\d*|beta\d*)?(?=[A-Z])")
_PACKAGE_AND_VERSION = re.compile(rf"^[a-z]*{_NAME_VERSION.pattern}")


class NameDriftError(RuntimeError):
    """The schema and public_names.json disagree."""


def operation_key(http_method: str, path: str) -> str:
    """An operation's identity across version bumps and path parameter renames.

    `GET /label/v202210/labels/{id}` is `GET /label/<version>/labels/{}`.
    """
    path = _PLACEHOLDER.sub("{}", _PATH_VERSION.sub("/<version>", path))
    return f"{http_method.upper()} {path}"


def model_key(name: str) -> str:
    """A model's identity across version bumps: `labelv202210Label` is `label<version>Label`."""
    return _NAME_VERSION.sub("<version>", name)


def default_model_name(name: str) -> str:
    """`labelv202210Label` and `v202303Severity` become `Label` and `Severity`."""
    return _PACKAGE_AND_VERSION.sub("", name)


def _resolve(
    where: str, entries: dict[str, str], candidates: dict[str, list[str]]
) -> dict[str, str]:
    """Maps each current key to its public name.

    `entries` maps public name to key and gains an entry for each new key: the
    first of its candidates not yet taken, in `candidates` order.
    """
    by_key: dict[str, str] = {}
    for public, key in entries.items():
        if key in by_key:
            raise NameDriftError(
                f"{NAMES_FILE.name}, {where}: `{by_key[key]}` and `{public}` "
                f"both point at {key!r}."
            )
        by_key[key] = public

    new = [key for key in candidates if key not in by_key]
    gone = sorted(public for public, key in entries.items() if key not in candidates)
    if gone:
        listed = ", ".join(f"`{public}` ({entries[public]!r})" for public in gone)
        hint = (
            f" The schema has these unnamed: {', '.join(map(repr, new))}."
            if new
            else ""
        )
        raise NameDriftError(
            f"{NAMES_FILE.name}, {where}: the schema no longer has {listed}.{hint} "
            "Point each entry at its new value, or delete it if upstream removed it."
        )

    for key in new:
        name = next((n for n in candidates[key] if n not in entries), None)
        if name is None:
            raise NameDriftError(
                f"{NAMES_FILE.name}, {where}: {key!r} is new, and its default name "
                f"`{candidates[key][0]}` is taken. Add an entry for it by hand."
            )
        entries[name] = key
        by_key[key] = name
    return by_key


def _check_name(where: str, name: str, *, model: bool = False) -> None:
    valid = name.isidentifier() and not keyword.iskeyword(name)
    valid = valid and not name.startswith("_")
    if model:
        valid = valid and normalize_symbol(name) == name
    if not valid:
        raise ValueError(f"{NAMES_FILE.name}, {where}: `{name}` is not a usable name.")


class PublicNames:
    """The contents of public_names.json, resolved against one schema."""

    def __init__(self, services: dict[str, dict] | None = None):
        self._services: dict[str, dict] = services or {}
        for service, entry in self._services.items():
            _check_name("services", service)
            if service in INTERNAL_GEN_DIRS:
                raise ValueError(f"{NAMES_FILE.name}: `{service}` is reserved.")
            for name in entry.get("methods", {}):
                _check_name(f"{service} methods", name)
            for name in entry.get("models", {}):
                _check_name(f"{service} models", name, model=True)

    @classmethod
    def load(cls, path: Path = NAMES_FILE) -> "PublicNames":
        if not path.exists():
            return cls()
        return cls(json.loads(path.read_text(encoding="utf-8"))["services"])

    def save(self, path: Path = NAMES_FILE) -> None:
        text = json.dumps({"services": self._services}, indent=2, sort_keys=True)
        write_text_lf(path, text + "\n")

    def services(self, upstream: Iterable[str]) -> dict[str, str]:
        """Maps each schema Service directory to its public name."""
        entries = {
            public: entry["upstream"] for public, entry in self._services.items()
        }
        by_upstream = _resolve("services", entries, {u: [u] for u in sorted(upstream)})
        for public, upstream_name in entries.items():
            self._services.setdefault(public, {"upstream": upstream_name})
        return by_upstream

    def _service(self, service: str) -> dict:
        return self._services.setdefault(service, {"upstream": service})

    def models(self, service: str, names: Iterable[str]) -> dict[str, str]:
        """Maps each model name a Service's patched schema defines to its public name."""
        by_key: dict[str, str] = {}
        for name in sorted(set(names)):
            other = by_key.setdefault(model_key(name), name)
            if other != name:
                raise NameDriftError(
                    f"{service}: models `{other}` and `{name}` differ only by "
                    "version, so neither has a stable name."
                )
        # An unversioned model claims its own name before a stripped one can.
        order = sorted(by_key, key=lambda key: (key != by_key[key], key))
        candidates = {
            key: list(dict.fromkeys([default_model_name(by_key[key]), by_key[key]]))
            for key in order
        }
        entries = self._service(service).setdefault("models", {})
        public = _resolve(f"{service} models", entries, candidates)
        return {by_key[key]: name for key, name in public.items()}

    def methods(self, service: str, defaults: dict[str, str]) -> dict[str, str]:
        """Maps each operation key of a Service to its client method name."""
        entries = self._service(service).setdefault("methods", {})
        return _resolve(
            f"{service} methods", entries, {key: [n] for key, n in defaults.items()}
        )
