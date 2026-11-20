# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""wait_for_batch() polls the status until the batch completes (spec 005, FR-012)."""

from __future__ import annotations

import math
from types import SimpleNamespace
from typing import cast

import httpx
import pytest

from kentik_api.client import KentikAPI
from kentik_api.core.api_config import APIConfig
from kentik_api.errors import AuthenticationError, HTTPException, TransportError
from kentik_api.gen.v5.models import BatchStatus
from kentik_api.v5_tools import BatchWaitTimeout, wait_for_batch


@pytest.fixture
def clock(batch_clock):
    return batch_clock


def _client(statuses, *, clock=None, durations=(), calls=None, config=None):
    answers = iter(statuses)
    elapsed = iter(durations)

    def batch_status(*, guid, api_config_override=None):
        if calls is not None:
            calls.append(api_config_override)
        if clock is not None:
            clock.now += next(elapsed, 0.0)
        answer = next(answers)
        if isinstance(answer, Exception):
            raise answer
        return answer

    return cast(
        KentikAPI,
        SimpleNamespace(
            v5=SimpleNamespace(batch_status=batch_status),
            v5_api_config=config
            or APIConfig(auth_email="dev@example.com", auth_token="t"),
        ),
    )


def test_returns_the_status_once_the_batch_is_complete(clock):
    done = BatchStatus(guid="g", is_complete=True)
    client = _client([BatchStatus(guid="g", is_complete=False), done])

    assert wait_for_batch(client, "g", timeout=60, interval=5) is done
    assert clock.sleeps == [5]


def test_raises_with_the_last_status_when_the_time_limit_expires(clock):
    pending = BatchStatus(guid="g", is_complete=False, number_of_parts=2)
    client = _client([pending] * 10)

    with pytest.raises(BatchWaitTimeout) as exc:
        wait_for_batch(client, "g", timeout=12, interval=5)

    assert exc.value.guid == "g"
    assert exc.value.last_status is pending
    assert clock.sleeps == [5, 5, 2]


def test_a_failed_status_call_raises_at_once(clock):
    client = _client([HTTPException(404, "Could not find this batch")])

    with pytest.raises(HTTPException):
        wait_for_batch(client, "g", timeout=60, interval=5)
    assert clock.sleeps == []


@pytest.mark.parametrize("field", ["timeout", "interval"])
@pytest.mark.parametrize("value", [0.0, -1.0, math.nan, math.inf, -math.inf])
def test_invalid_wait_bounds_fail_before_accessing_the_client(clock, field, value):
    client = cast(KentikAPI, SimpleNamespace())
    with pytest.raises(ValueError, match=field):
        wait_for_batch(client, "g", **{field: value})
    assert clock.sleeps == []


@pytest.mark.parametrize("duration", [0.5, 1.0, 30.0])
def test_late_completed_status_never_returns_success(clock, duration):
    done = BatchStatus(guid="g", is_complete=True)
    calls = []
    client = _client([done], clock=clock, durations=(duration,), calls=calls)
    if duration < 1.0:
        assert wait_for_batch(client, "g", timeout=1.0) is done
    else:
        with pytest.raises(BatchWaitTimeout) as exc:
            wait_for_batch(client, "g", timeout=1.0)
        assert exc.value.guid == "g"
        assert exc.value.last_status is done
    assert len(calls) == 1


def test_an_exhausted_sleep_cannot_start_another_poll(clock):
    pending = BatchStatus(guid="g", is_complete=False)
    calls = []
    client = _client([pending] * 3, calls=calls)
    with pytest.raises(BatchWaitTimeout) as exc:
        wait_for_batch(client, "g", timeout=1.0, interval=5.0)
    assert exc.value.last_status is pending
    assert clock.sleeps == [1.0]
    assert len(calls) == 1


@pytest.mark.parametrize(
    "timeout_type",
    [httpx.ConnectTimeout, httpx.ReadTimeout, httpx.WriteTimeout, httpx.PoolTimeout],
)
@pytest.mark.parametrize("duration", [0.5, 1.0, 1.2])
@pytest.mark.parametrize("prior_status", [False, True])
def test_request_timeout_classification_uses_observation_time(
    clock, timeout_type, duration, prior_status
):
    cause = timeout_type("fixture timeout")
    original = TransportError("fixture transport timeout")
    original.__cause__ = cause
    pending = BatchStatus(guid="g", is_complete=False)
    statuses = [pending, original] if prior_status else [original]
    durations = (0.0, duration) if prior_status else (duration,)
    calls = []
    client = _client(
        statuses,
        clock=clock,
        durations=durations,
        calls=calls,
        config=APIConfig(rest_timeout=httpx.Timeout(0.5)),
    )
    expected = TransportError if duration < 1.0 else BatchWaitTimeout

    with pytest.raises(expected) as exc:
        wait_for_batch(client, "g", timeout=1.0, interval=0.1)

    if duration < 1.0:
        assert exc.value is original
    else:
        assert isinstance(exc.value, BatchWaitTimeout)
        assert exc.value.last_status is (pending if prior_status else None)
        assert exc.value.__cause__ is original
    assert original.__cause__ is cause
    assert len(calls) == (2 if prior_status else 1)


@pytest.mark.parametrize(
    "original",
    [
        HTTPException(404, "fixture"),
        HTTPException(502, "fixture"),
        AuthenticationError("fixture"),
        TransportError("fixture connection failure"),
        ValueError("fixture programming error"),
    ],
)
def test_non_timeout_errors_stay_unchanged_after_the_deadline(clock, original):
    calls = []
    client = _client([original], clock=clock, durations=(2.0,), calls=calls)
    with pytest.raises(type(original)) as exc:
        wait_for_batch(client, "g", timeout=1.0)
    assert exc.value is original
    assert len(calls) == 1
    assert clock.sleeps == []
