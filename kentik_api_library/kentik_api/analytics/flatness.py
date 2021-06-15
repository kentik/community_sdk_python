import io
import json
import logging
import numpy as np
import pandas as pd
from kentik_api.utils import DeviceCache
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

log = logging.getLogger('ktapi_analytics')


def set_link_utilization(df: pd.DataFrame, devices: DeviceCache, link_col: Optional[str] = 'link',
                         data_col: Optional[str] = 'bps_out', util_col: Optional[str] = 'utilization',
                         speed_col: Optional[str] = 'speed') -> None:
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
            log.debug('Input DataFrame %s: link_col: %s, data_col: %s, util_col: %s', f.getvalue(), link_col, data_col,
                      util_col)
    if link_col not in df:
        raise RuntimeError(f'No {link_col} column in DataFrame')
    if data_col not in df:
        raise RuntimeError(f'No {data_col} column in DataFrame')
    speeds = devices.get_link_speeds(df[link_col].unique())
    df[speed_col] = [speeds[link] for link in df[link_col]]
    df[util_col] = (df[data_col] / df[speed_col]) * 100


def compute_flatness(df: pd.DataFrame,
                     method: str = 'range',
                     pivot: str = 'link',
                     data: str = 'utilization',
                     window: str = '1H',
                     min_samples: int = 3,
                     closed: str = 'right') -> pd.DataFrame:
    """
    Compute measure of flatness over DataFrame column using time window
    :param df: pandas.DataFrame indexed by time with  2 columns:
        - pivot: str or panda.object
        - any numeric value (anything allowing to compute mean)
    :param method: string identifying method to use for producing measure of flatness
           available methods:
           - range = use difference between min and max over utilization
           - variance = uses variance over utilization
    :param pivot: name of column for grouping results
    :param data: name of column containing data over which to compute flatness score
    :param window: window size specification for flatness computation (see pandas.Rolling)
    :param min_samples: minimum number of samples in a window to have valid result (see pandas.Rolling min_period)
    :param closed: parameter for rolling window interval calculation (see pandas.Rolling closed)
    :return: pandas.DataFrame indexed with MultiIndex(pivot, time) and with 2 columns
            - mean = mean value of data column for each rollup window
            - flatness measure for each rollup window based on specified method
    """
    if log.level == logging.DEBUG:
        with io.StringIO() as f:
            df.info(buf=f)
            log.debug('Evaluating DataFrame %s, window: %s, pivot: %s, data: %s', f.getvalue(), window, pivot, data)
    if pivot not in df:
        raise RuntimeError(f'No {pivot} columns in DataFrame')
    if data not in df:
        raise RuntimeError(f'No {data} column in DataFrame')
    mean = df.groupby(by=pivot)[data].rolling(window=window, closed=closed, min_periods=min_samples).mean()
    if method == 'range':
        y = df.groupby(by=pivot)[data].rolling(window=window, closed=closed, min_periods=min_samples)\
            .apply(lambda x: np.max(x) - np.min(x), raw=True)
    elif method == 'variance':
        y = df.groupby(by=pivot)[data].rolling(window=window, closed=closed, min_periods=min_samples).var()
    else:
        raise RuntimeError(f'Unsupported flatness analysis method "{method}"')
    return pd.DataFrame(index=mean.index, data={'mean': mean, 'flatness': y})


def compute_stats(df: pd.DataFrame,
                  pivot: str = 'link',
                  data: str = 'utilization',
                  window: str = '1H',
                  min_samples: int = 3,
                  closed: str = 'right') -> pd.DataFrame:
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
            log.debug('Evaluating DataFrame %s, window: %s, pivot: %s, data: %s', f.getvalue(), window, pivot, data)
    if pivot not in df:
        raise RuntimeError(f'No {pivot} columns in DataFrame')
    if data not in df:
        raise RuntimeError(f'No {data} column in DataFrame')
    return df.groupby(by=pivot)[data].rolling(window=window, closed=closed, min_periods=min_samples).agg(
                                                                        {'mean': 'mean', 'max': 'max', 'min': 'min'})


def analyze_flatness(df: pd.DataFrame,
                     flatness_limit: float,
                     window: timedelta,
                     min_valid: float = 0,
                     max_valid: float = 100,
                     link_index: str = 'link',
                     mean_column: str = 'mean',
                     max_column: str = 'max',
                     min_column: str = 'min') -> Dict[str, List[Tuple[datetime, datetime]]]:
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
    :return: dictionary keyed by link names with values being List of Tuples of start, end timestamps of intervals
    """
    if log.level == logging.DEBUG:
        with io.StringIO() as f:
            df.info(buf=f)
            log.debug('Input DataFrame %s', f.getvalue())
            log.debug('flatness_limit: %f, window: %s, min_valid: %f, max_valid: %f',
                      flatness_limit, window, min_valid, max_valid)
            log.debug('mean_column: %s, min_column: %s, max_column: %s,  link_index: %s',
                      mean_column, min_column, max_column, link_index,)

    links = df.index.get_level_values(link_index).unique()
    results: Dict[str, List[Tuple[datetime, datetime]]] = {link: [] for link in links}
    suspects = (min_valid < df[mean_column]) & (df[mean_column] < max_valid) & \
               ((df[max_column] - df[min_column]) < flatness_limit)
    if not suspects.any():
        log.debug('No suspects')
        # Nothing to do
        return results
    log.debug('%d suspects', len(suspects))
    merged = 0
    for link in links:
        last = None
        d = df.xs(link)
        for ts in suspects.xs(link)[suspects.xs(link)].index:
            log.debug('link: %s, ts: %s', link, ts)
            s = d.loc[ts - window:].index[0]
            if last is not None and last[1] >= s:
                agg_min = min(d.loc[last[1]][min_column], d.loc[ts][min_column])
                agg_max = max(d.loc[last[1]][max_column], d.loc[ts][max_column])
                log.debug('link: %s, overlap at: %s, combined range: %f', link, ts, agg_max - agg_min)
                if agg_max - agg_min < flatness_limit:
                    merged += 1
                    log.debug('link: %s, merging: [%s, %s]', link, results[link][-1][0], ts)
                    results[link][-1][1] = ts
                    continue
            log.debug('link: %s, adding: [%s, %s]', link, s, ts)
            results[link].append([s, ts])
            last = results[link][-1]
    # remove intervals shorter than window
    # such intervals can occur at the beginning of the observation
    removed = 0
    for link, intervals in results.items():
        for interval in [i for i in intervals if i[1] - i[0] < window]:
            log.debug('link: %s, removing: %s', link, f'[{interval[0]} {interval[1]}]')
            intervals.remove(interval)
            removed += 1
    log.debug('total events: %d', sum(len(x) for x in results.values()))
    log.debug('merged %s intervals', merged)
    log.debug('removed %s intervals', removed)
    return results


def flatness_results_to_json(results: Dict, filename: str) -> None:
    r = dict()
    for link, intervals in results.items():
        if len(intervals) < 1:
            continue
        r[link] = list()
        for i in intervals:
            r[link].append([i[0].isoformat(), i[1].isoformat()])
    with Path(filename).open('w') as f:
        json.dump(r, f, indent=2)
