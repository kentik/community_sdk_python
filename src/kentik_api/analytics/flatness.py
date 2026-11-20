# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Find time windows where outbound traffic on a link stayed flat (1.x flatness).

On a perimeter link, flat traffic suggests a bandwidth limit in a peer network.
Ported from 1.x `kentik_api.analytics.flatness`, with the same inputs and
outputs. `devices` is a `kentik_api.devices.DeviceLookup`, or any object with
`get_link_speeds(links)` that returns bits/s for each link name.
"""

from __future__ import annotations

import json
import logging
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Literal, Protocol, TextIO, cast

import pandas as pd

log = logging.getLogger(__name__)


class LinkSpeeds(Protocol):
    def get_link_speeds(self, links: Any = None) -> dict[str, float]: ...


@dataclass
class Interval:
    start: datetime
    end: datetime


class FlatnessResults:
    """The flat intervals found on each link, keyed by link name."""

    def __init__(self, links: Any):
        self.events: dict[str, list[Interval]] = {link: [] for link in links}

    def __getitem__(self, link: str) -> list[Interval] | None:
        return self.events.get(link)

    @property
    def stats(self) -> dict[str, int]:
        return {
            "total_events": sum(len(i) for i in self.events.values()),
            "max_per_link": max((len(i) for i in self.events.values()), default=0),
        }

    def last(self, link: str) -> Interval | None:
        intervals = self.events.get(link)
        return intervals[-1] if intervals else None

    def set_last(self, link: str, interval: Interval) -> None:
        self.events[link][-1] = interval

    @property
    def affected_links(self) -> list[str]:
        return [link for link, intervals in self.events.items() if intervals]

    def to_json(self, **kwargs: Any) -> str:
        return json.dumps(
            {
                link: [(i.start.isoformat(), i.end.isoformat()) for i in intervals]
                for link, intervals in self.events.items()
                if intervals
            },
            **kwargs,
        )

    def to_json_file(self, filename: str, **kwargs: Any) -> None:
        Path(filename).write_text(self.to_json(**kwargs), encoding="utf-8")

    def to_text(self, out: TextIO | None = None) -> None:
        for key, value in self.stats.items():
            print(f"{key:20}: {value}", file=out)
        print(file=out)
        for link, intervals in self.events.items():
            if not intervals:
                continue
            print(link, file=out)
            for i in intervals:
                print(f"\t[{i.start}, {i.end}]", file=out)


def min_index_resolution(df: pd.DataFrame) -> timedelta:
    """The longest gap between consecutive unique index times."""
    if df.index.inferred_type != "datetime64":
        raise ValueError("Input DataFrame is not indexed by time")
    idx = df.sort_index().index.unique()
    return max(idx[i] - idx[i - 1] for i in range(1, len(idx)))


def freq_to_seconds(freq: str) -> float:
    if not freq[0].isdigit():
        freq = "1" + freq
    return pd.Timedelta(freq).total_seconds()


def resample_volume_data(
    df: pd.DataFrame, resolution: str, link_col: str = "link"
) -> pd.DataFrame:
    """Resamples to a lower resolution and keeps the link column."""
    if df.shape[1] < 2 or link_col not in df:
        raise ValueError(
            f"Input DataFrame must have 2 columns, one of them '{link_col}'"
        )
    if df.index.inferred_type != "datetime64":
        raise ValueError("Input DataFrame must have a DatetimeIndex")
    index_name = df.index.name
    return (
        df.groupby(link_col)
        .resample(resolution)
        .sum(numeric_only=True)
        .reset_index()
        .set_index(index_name)
        .sort_index()
    )


def has_uniform_datetime_index(df: pd.DataFrame) -> bool:
    return _inferred_freq(df) is not None


def _inferred_freq(df: pd.DataFrame) -> str | None:
    index = df.index.unique()
    if index.inferred_type != "datetime64":
        return None
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="A future version of pandas")
        freq = pd.infer_freq(pd.DatetimeIndex(index))
    # A future pandas returns an offset instead of a string.
    return freq if freq is None or isinstance(freq, str) else freq.freqstr


def compute_link_bandwidth(
    df: pd.DataFrame,
    data_col: str = "bytes_out",
    bps_col: str = "bps_out",
    link_col: str = "link",
) -> pd.DataFrame:
    """Bits/s on each link from bytes per index period. Needs a uniform index."""
    freq = _inferred_freq(df)
    if freq is None:
        raise ValueError(
            "Input DataFrame is not indexed by time, or the index is not uniform"
        )
    factor = 8 / freq_to_seconds(freq)
    out = df.drop(columns=[c for c in df.columns if c != link_col])
    out[bps_col] = df[data_col] * factor
    return out


def compute_link_utilization(
    df: pd.DataFrame,
    devices: LinkSpeeds,
    link_col: str = "link",
    data_col: str = "bps_out",
    util_col: str = "utilization",
    speed_col: str = "speed",
) -> pd.DataFrame:
    """Utilization in percent of each link's speed."""
    if link_col not in df:
        raise ValueError(f"No {link_col} column in DataFrame")
    if data_col not in df:
        raise ValueError(f"No {data_col} column in DataFrame")
    speeds = devices.get_link_speeds(df[link_col].unique())
    out = df.drop(columns=[c for c in df.columns if c != link_col])
    out[speed_col] = [speeds[link] for link in df[link_col]]
    out[util_col] = (df[data_col] / out[speed_col]) * 100
    return out


def compute_stats(
    df: pd.DataFrame,
    pivot: str = "link",
    data: str = "utilization",
    window: timedelta = timedelta(hours=1),
    min_samples: int = 3,
    closed: Literal["right", "left", "both", "neither"] = "right",
) -> pd.DataFrame:
    """Rolling mean, max, and min of `data` for each `pivot` value."""
    if pivot not in df:
        raise ValueError(f"No {pivot} column in DataFrame")
    if data not in df:
        raise ValueError(f"No {data} column in DataFrame")
    return cast(
        pd.DataFrame,
        df.groupby(by=pivot)[data]
        .rolling(window=window, closed=closed, min_periods=min_samples)
        .agg(["mean", "max", "min"]),
    )


def analyze_flatness(
    df: pd.DataFrame,
    flatness_limit: float,
    window: timedelta,
    min_valid: float = 0,
    max_valid: float = 100,
    link_index: str = "link",
    mean_column: str = "mean",
    max_column: str = "max",
    min_column: str = "min",
) -> FlatnessResults:
    """Intervals where the rolling range stayed under `flatness_limit`."""
    links = df.index.get_level_values(link_index).unique()
    results = FlatnessResults(links)
    suspects = (
        (min_valid < df[mean_column])
        & (df[mean_column] < max_valid)
        & ((df[max_column] - df[min_column]) < flatness_limit)
    )
    if not cast(bool, suspects.any()):
        return results
    for link in links:
        last = results.last(link)
        d = df.xs(link)
        link_suspects = cast(pd.Series, suspects.xs(link))
        for ts in cast(pd.DatetimeIndex, link_suspects.index[link_suspects.to_numpy()]):
            start_pos = int(d.index.searchsorted(ts - window))
            s = cast(pd.Timestamp, d.index[start_pos])
            if last is not None and last.end >= s:
                agg_min = min(
                    cast(float, d.at[last.end, min_column]),
                    cast(float, d.at[ts, min_column]),
                )
                agg_max = max(
                    cast(float, d.at[last.end, max_column]),
                    cast(float, d.at[ts, max_column]),
                )
                if agg_max - agg_min < flatness_limit:
                    last.end = ts
                    continue
            results.events[link].append(Interval(start=s, end=ts))
            last = results.last(link)
    for intervals in results.events.values():
        intervals[:] = [i for i in intervals if i.end - i.start >= window]
    return results


def flatness_analysis(
    devices: LinkSpeeds,
    data: pd.DataFrame,
    flatness_limit: float,
    window: timedelta,
    min_valid: float = 0,
    max_valid: float = 100,
) -> FlatnessResults:
    """Finds intervals of flat link utilization.

    `data` is indexed by time and has a `link` column (`<device>:<interface>`)
    and `bytes_out` or `bps_out` for the period that ends at each timestamp.
    `bps_out` wins when both are present. `flatness_limit`, `min_valid`, and
    `max_valid` are utilization percentages.
    """
    if "bps_out" not in data:
        if not has_uniform_datetime_index(data):
            resolution = min_index_resolution(data).total_seconds()
            log.info(
                "Non-uniform sampling (min resolution %f s): resampling", resolution
            )
            data = resample_volume_data(data, f"{resolution}s")
        link_bw = compute_link_bandwidth(data)
    else:
        link_bw = data
    link_util = compute_link_utilization(link_bw, devices)
    unknown = len(link_util.loc[link_util.speed == 0].link.unique())
    if unknown:
        log.info("%d links with unknown or zero speed ignored", unknown)
    over = link_util[
        (link_util.utilization > 100) & (link_util.utilization != float("inf"))
    ]
    if not over.empty:
        log.critical("%d data samples with link utilization > 100%%", over.shape[0])
    stats = compute_stats(link_util, window=window)
    return analyze_flatness(
        stats,
        flatness_limit=flatness_limit,
        window=window,
        min_valid=min_valid,
        max_valid=max_valid,
    )
