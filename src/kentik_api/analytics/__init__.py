# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""pandas helpers for V5 query results (the 1.x `kentik_api.analytics` package).

Needs the `analytics` extra: `pip install "kentik-api[analytics]"`.
"""

try:
    import pandas
    import pyarrow
    import yaml
except ImportError as exc:
    raise ImportError(
        "kentik_api.analytics needs the analytics extra: "
        'pip install "kentik-api[analytics]"'
    ) from exc

from kentik_api.analytics.cache import DFCache, dedup_data_frame
from kentik_api.analytics.definitions import (
    DataQueryDefinition,
    MappingEntry,
    ResultMapping,
    SQLQueryDefinition,
    data_result_to_df,
)
from kentik_api.analytics.flatness import FlatnessResults, Interval, flatness_analysis

__all__ = [
    "DFCache",
    "DataQueryDefinition",
    "FlatnessResults",
    "Interval",
    "MappingEntry",
    "ResultMapping",
    "SQLQueryDefinition",
    "data_result_to_df",
    "dedup_data_frame",
    "flatness_analysis",
]
