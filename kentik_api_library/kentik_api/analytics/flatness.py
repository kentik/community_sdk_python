import io
import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from kentik_api.utils import DeviceCache


log = logging.getLogger("flatness_analysis")


@dataclass
class Interval:
    start: datetime
    end: datetime


class FlatnessResults:
    """
    Class storing results of traffic flatness analysis on set of links
    The events attribute contains dictionary keyed by link name containing list intervals in which traffic was
    deemed to be 'flat'. Each interval is instance of 'Interval' named tuple.
    """

    def __init__(self, links: List[str]):
        self.events: Dict[str, List[Interval]] = {link: [] for link in links}

    def __getitem__(self, link):
        return self.events.get(link)

    @property
    def stats(self) -> Dict[str, int]:
        return dict(
            total_events=sum(len(i) for i in self.events.values()),
            max_per_link=max(len(i) for i in self.events.values()),
        )

    def last(self, link: str) -> Optional[Interval]:
        if link in self.events and self.events[link]:
            return self.events[link][-1]
        else:
            return None

    def set_last(self, link: str, interval: Interval) -> None:
        self.events[link][-1] = interval

    @property
    def affected_links(self) -> List[str]:
        return [link for link, intervals in self.events.items() if len(intervals) > 0]

    def to_json(self, filename: Optional[str] = None) -> Optional[str]:
        r = {
            link: [(i.start.isoformat(), i.end.isoformat()) for i in intervals]
            for link, intervals in self.events.items()
            if len(intervals) > 0
        }
        if filename:
            with Path(filename).open("w") as f:
                json.dump(r, f, indent=2)
                return None
        else:
            return json.dumps(r, indent=2)

    def to_text(self, out=sys.stdout) -> None:
        for k, v in self.stats.items():
            print(f"{k:20}: {v}", file=out)
        print(file=out)
        for link, intervals in self.events.items():
            if len(intervals) < 1:
                continue
            print(link, file=out)
            for i in intervals:
                print(f"\t[{i.start}, {i.end}]", file=out)


def set_link_utilization(
    df: pd.DataFrame,
    devices: DeviceCache,
    link_col: Optional[str] = "link",
    data_col: Optional[str] = "bps_out",
    util_col: Optional[str] = "utilization",
    speed_col: Optional[str] = "speed",
) -> None:
    """
    Adds column 'utilization' to a DataFrame based on interface speeds in 'devices' and the 'data' column
    :param df: DataFrame to work on. It is expected to contain:
    - link_col column containing names of links  (link = device_name:interface_name)
    - numeric data_col column containing data rate in bps
    :param devices: DeviceCache instance containing data for relevant devices
    :param link_col: Name of column containing link names
    :param data_col: Name of column containing data rate
    :param util_col: Name of column for utilization
    :param speed_col: Name of columns for interface speed (installed bandwidth)
    :return: None (modifies input DataFrame in place)
    """
    if log.level == logging.DEBUG:
        with io.StringIO() as f:
            df.info(buf=f)
            log.debug(
                "Input DataFrame %s: link_col: %s, data_col: %s, util_col: %s",
                f.getvalue(),
                link_col,
                data_col,
                util_col,
            )
    if link_col not in df:
        raise RuntimeError(f"No {link_col} column in DataFrame")
    if data_col not in df:
        raise RuntimeError(f"No {data_col} column in DataFrame")
    speeds = devices.get_link_speeds(df[link_col].unique())
    df[speed_col] = [speeds[link] for link in df[link_col]]
    df[util_col] = (df[data_col] / df[speed_col]) * 100


def compute_stats(
    df: pd.DataFrame,
    pivot: str = "link",
    data: str = "utilization",
    window: timedelta = timedelta(hours=1),
    min_samples: int = 3,
    closed: str = "right",
) -> pd.DataFrame:
    """
    Compute mean, max and min over a DataFrame column using rolling window
    :param df: pandas.DataFrame indexed by time with  2 columns:
        - pivot: str or panda.object
        - any numeric value (anything allowing to compute mean)
    :param pivot: name of column for grouping results
    :param data: name of column containing data over which to compute flatness score
    :param window: window size specification for flatness computation (see pandas.Rolling)
    :param min_samples: minimum number of samples in a window to have valid result (see pandas.Rolling min_period)
    :param closed: parameter for rolling window interval calculation (see pandas.Rolling closed)
    :return: pandas.DataFrame indexed with MultiIndex(pivot, time) and with 3 columns
            - mean = mean value of data column for each rollup window
            - min = minimum value for each rollup window
            - max = maximum values for each rollup window
    """
    if log.level == logging.DEBUG:
        with io.StringIO() as f:
            df.info(buf=f)
            log.debug("Evaluating DataFrame %s, window: %s, pivot: %s, data: %s", f.getvalue(), window, pivot, data)
    if pivot not in df:
        raise RuntimeError(f"No {pivot} columns in DataFrame")
    if data not in df:
        raise RuntimeError(f"No {data} column in DataFrame")
    return (
        df.groupby(by=pivot)[data]
        .rolling(window=window, closed=closed, min_periods=min_samples)
        .agg({"mean": "mean", "max": "max", "min": "min"})
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
    """
    Analyze flatness measure and means in the DataFrame to find intervals where utilization was 'flat' based
    on specified criteria

    :param df: DataFrame containing flatness measure and mean of the observed variable
               The DataFrame must be indexed by link names and time
    :param flatness_limit: threshold for considering traffic flat (values less than the threshold are considered flat)
    :param window: time interval in which the rolling windows were computed
    :param min_valid: lower bound for the mean of the observed variable to consider interval for flatness
    :param max_valid: upper bound for the mean of the observed variable to consider interval for flatness
    :param mean_column: name of the column containing mean of the observed variable
    :param max_column: name of the column containing maximum of the observed variable
    :param min_column: name of the column containing minimum of the observed variable
    :param link_index: name of index level containing link names
    :return: FlatnessResults object
    """
    if log.getEffectiveLevel() == logging.DEBUG:
        with io.StringIO() as f:
            df.info(buf=f)
            log.debug("Input DataFrame %s", f.getvalue())
            log.debug(
                "flatness_limit: %f, window: %s, min_valid: %f, max_valid: %f",
                flatness_limit,
                window,
                min_valid,
                max_valid,
            )
            log.debug(
                "mean_column: %s, min_column: %s, max_column: %s,  link_index: %s",
                mean_column,
                min_column,
                max_column,
                link_index,
            )

    links = df.index.get_level_values(link_index).unique()
    results = FlatnessResults(links)
    suspects = (
        (min_valid < df[mean_column])
        & (df[mean_column] < max_valid)
        & ((df[max_column] - df[min_column]) < flatness_limit)
    )
    if not suspects.any():
        log.debug("No suspects")
        # Nothing to do
        return results
    log.debug("%d suspects", suspects.value_counts().loc[True])
    merged = 0
    for link in links:
        last = results.last(link)
        d = df.xs(link)
        for ts in suspects.xs(link)[suspects.xs(link)].index:
            log.debug("link: %s, ts: %s", link, ts)
            s = d.loc[(ts - window) :].index[0]
            if last is not None and last.end >= s:
                agg_min = min(d.loc[last.end][min_column], d.loc[ts][min_column])
                agg_max = max(d.loc[last.end][max_column], d.loc[ts][max_column])
                log.debug("link: %s, overlap at: %s, combined range: %f", link, ts, agg_max - agg_min)
                if agg_max - agg_min < flatness_limit:
                    merged += 1
                    log.debug("link: %s, merging: [%s, %s]", link, results[link][-1].start, ts)
                    results.last(link).end = ts  # type: ignore
                    continue
            log.debug("link: %s, adding: [%s, %s]", link, s, ts)
            results[link].append(Interval(start=s, end=ts))
            last = results.last(link)
    # remove intervals shorter than window
    # such intervals can occur at the beginning of the observation
    removed = 0
    for link, intervals in results.events.items():
        for interval in [i for i in intervals if i.end - i.start < window]:
            log.debug("link: %s, removing: %s", link, f"[{interval.start} {interval.end}]")
            intervals.remove(interval)
            removed += 1
    log.debug("total events: %d", results.stats["total_events"])
    log.debug("merged %s intervals", merged)
    log.debug("removed %s intervals", removed)
    return results


def flatness_analysis(
    devices: DeviceCache,
    data: pd.DataFrame,
    flatness_limit: float,
    window: timedelta,
    min_valid: float = 0,
    max_valid: float = 100,
) -> FlatnessResults:
    """
    Detect intervals of constant traffic in data passed in DataFrame based on provided criteria.
    :param devices: instance of kentik-api.utils.DeviceCache containing data for all devices references in the `link`
                    column of the "data" DataFrame
    :param data: DataFrame indexed by time ("ts" column) containing columns "link" and "bps_out". The "link" column is
                 expected to contain names of network links as <device_name>:<interface_name> and :"bps_out" contains
                 sum of outbound traffic rate (in bits per second) for the interval ending at the row timestamp
    :param flatness_limit: maximum range of network link utilization in percents to deem traffic constant ("flat")
    :param window: minimum time window over which link utilization must stay with flatness_limit
    :param min_valid: minimum link utilization in percents for the interval to be considered as "flat traffic"
    :param max_valid: maximum link utilization in percents for the interval to be considered as "flat traffic"
    :return: FlatnessResults instance
    """
    log.debug("Got %d entries for %d links", data.shape[0], len(data["link"].unique()))
    log.debug("Computing link utilization")
    set_link_utilization(data, devices)
    log.debug("Computing traffic statistics")
    stats = compute_stats(data, window=window)
    log.debug("Analyzing flatness")
    return analyze_flatness(
        stats, flatness_limit=flatness_limit, window=window, min_valid=min_valid, max_valid=max_valid
    )
