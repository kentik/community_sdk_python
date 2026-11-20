# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

__all__ = [
    "RateLimit",
    "attach_rate_limit",
    "rate_limit_of",
    "rate_limit_of_rpc",
]

_ATTR = "_kentik_rate_limit"

_LIMIT = "x-ratelimit-limit"
_REMAINING = "x-ratelimit-remaining"
_RESET = "x-ratelimit-reset"
# Kentik sends `w=` (draft-polli-ratelimit-headers); other APIs document `window=`.
_WINDOW_PARAMS = ("w", "window")


def _int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value.strip())
    except ValueError:
        return None


def _window_of(policy: str) -> int | None:
    for param in policy.split(";")[1:]:
        name, _, value = param.partition("=")
        if name.strip().lower() in _WINDOW_PARAMS:
            return _int_or_none(value)
    return None


def _parse_limit(raw: str) -> tuple[int | None, int | None]:
    """`60, 60;w=60` -> (60, 60).

    The first value is the binding quota. Its window comes from the policy
    with the same quota, falling back to the first window given at all.
    """
    policies = [part.strip() for part in raw.split(",") if part.strip()]
    if not policies:
        return None, None
    limit = _int_or_none(policies[0].split(";")[0])
    windows = [(_int_or_none(p.split(";")[0]), _window_of(p)) for p in policies]
    matching = [w for quota, w in windows if quota == limit and w is not None]
    any_window = [w for _, w in windows if w is not None]
    return limit, (matching or any_window or [None])[0]


@dataclass(frozen=True)
class RateLimit:
    """Quota the API reported on one response, as of that response.

    Each field is `None` when the server omitted it rather than a guessed
    default, because the API advertises only the per-minute window: the
    concurrency cap, soft-limit delay, and hourly limit never reach a header.
    """

    limit: int | None
    remaining: int | None
    reset_seconds: int | None
    window_seconds: int | None
    raw: str | None

    @classmethod
    def from_headers(cls, headers: Mapping[str, str] | None) -> RateLimit | None:
        """Parses REST response headers. Never raises: quota reporting must not fail a call."""
        try:
            if not headers:
                return None
            lowered = {str(k).lower(): str(v) for k, v in headers.items()}
            raw = lowered.get(_LIMIT)
            limit, window = _parse_limit(raw) if raw else (None, None)
            remaining = _int_or_none(lowered.get(_REMAINING))
            reset = _int_or_none(lowered.get(_RESET))
        except Exception:  # noqa: BLE001 - malformed quota headers must not fail the call
            return None
        if limit is None and remaining is None and reset is None:
            return None
        return cls(
            limit=limit,
            remaining=remaining,
            reset_seconds=reset,
            window_seconds=window,
            raw=raw,
        )

    @classmethod
    def from_metadata(
        cls, metadata: Iterable[tuple[str, str | bytes]] | None
    ) -> RateLimit | None:
        """Parses gRPC initial metadata, where Kentik sends the same keys as REST headers."""
        try:
            if not metadata:
                return None
            headers = {
                key: value.decode("utf-8", errors="replace")
                if isinstance(value, bytes)
                else value
                for key, value in metadata
            }
        except Exception:  # noqa: BLE001 - malformed metadata must not fail the call
            return None
        return cls.from_headers(headers)


def rate_limit_of_rpc(call_or_error: object) -> RateLimit | None:
    """Reads quota off a grpc.Call or a failed call's RpcError.

    Kentik sends it in initial metadata. An error with no body is sent
    "Trailers-Only", which puts every header in the trailing metadata instead.
    """
    for getter in ("initial_metadata", "trailing_metadata"):
        try:
            metadata = getattr(call_or_error, getter)()
        except Exception:  # noqa: BLE001, S112 - a call without metadata has no quota to report
            continue
        if (rate_limit := RateLimit.from_metadata(metadata)) is not None:
            return rate_limit
    return None


def attach_rate_limit[T](result: T, rate_limit: RateLimit | None) -> T:
    """Rides the quota along on a returned model without changing its fields.

    object.__setattr__ bypasses the generated models' validate_assignment, and
    leaves model_dump() and == untouched because Pydantic compares declared
    fields only. Results that cannot carry an attribute (None, lists) are
    returned unchanged.
    """
    if rate_limit is not None and result is not None:
        try:
            object.__setattr__(result, _ATTR, rate_limit)
        except (AttributeError, TypeError):
            pass
    return result


def rate_limit_of(result: object) -> RateLimit | None:
    """The quota reported by the call that produced `result`, if any."""
    return getattr(result, _ATTR, None)
