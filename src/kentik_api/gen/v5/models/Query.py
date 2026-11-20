# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, List, Optional

from pydantic import BaseModel, Field

from .Aggregate import Aggregate
from .QueryFilters import QueryFilters
from .SavedFilterRef import SavedFilterRef


class Query(BaseModel):
    """
    A query on the Kentik Data Engine. Types the fields that the Kentik Query API documentation lists, and keeps every other field it gets, so every V5 SDK field and JSON copied from Data Explorer reaches the API unchanged.
    """

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "extra": "allow",
    }

    metric: Any = Field(
        validation_alias="metric",
        description="The unit of measure, as a string or a list of strings (the V5 SDK sent a list): bytes, in_bytes, out_bytes, packets, in_packets, out_packets, tcp_retransmit, perc_retransmit, retransmits_in, perc_retransmits_in, out_of_order_in, perc_out_of_order_in, fragments, perc_fragments, client_latency, server_latency, appl_latency, fps, unique_src_ip, or unique_dst_ip.",
    )

    dimension: List[str] = Field(
        validation_alias="dimension",
        description="The group-by dimensions, for example Proto, AS_src, IP_dst, Traffic, or a custom dimension.",
    )

    device_name: Optional[Any] = Field(
        validation_alias="device_name",
        default=None,
        description="The devices to query, as a comma-separated string or a list of names (the V5 SDK sent a list). Required in practice: the API returns 400 without it, even when all_selected is true.",
    )

    all_selected: Optional[bool] = Field(
        validation_alias="all_selected",
        default=None,
        description="Queries all devices.",
    )

    device_labels: Optional[Any] = Field(
        validation_alias="device_labels",
        default=None,
        description="Device label IDs, as a list or a comma-separated string. Label names are not accepted.",
    )

    lookback_seconds: Optional[int] = Field(
        validation_alias="lookback_seconds",
        default=None,
        description="The time range, in seconds back from now. Overrides starting_time and ending_time unless it is 0.",
    )

    starting_time: Optional[str] = Field(
        validation_alias="starting_time",
        default=None,
        description="The fixed start, as YYYY-MM-DD HH:mm:00. Used when lookback_seconds is 0.",
    )

    ending_time: Optional[str] = Field(
        validation_alias="ending_time",
        default=None,
        description="The fixed end, as YYYY-MM-DD HH:mm:00. Used when lookback_seconds is 0.",
    )

    time_format: Optional[str] = Field(
        validation_alias="time_format",
        default=None,
        description="UTC or Local. URL only.",
    )

    topx: Optional[int] = Field(
        validation_alias="topx",
        default=None,
        description="The number of top rows that get time series, 1 to 40.",
    )

    depth: Optional[int] = Field(
        validation_alias="depth",
        default=None,
        description="The number of result rows from which topx is chosen, 25 to 250.",
    )

    outsort: Optional[str] = Field(
        validation_alias="outsort",
        default=None,
        description="The aggregate name to sort by, for example avg_bits_per_sec.",
    )

    fastData: Optional[str] = Field(
        validation_alias="fastData",
        default=None,
        description="The dataset: Auto, Fast, or Full.",
    )

    hostname_lookup: Optional[bool] = Field(
        validation_alias="hostname_lookup",
        default=None,
        description="Resolves IP addresses to host names. Set to false for faster IP queries.",
    )

    cidr: Optional[int] = Field(
        validation_alias="cidr",
        default=None,
        description="The IPv4 prefix length for IP dimensions, 0 to 32.",
    )

    cidr6: Optional[int] = Field(
        validation_alias="cidr6",
        default=None,
        description="The IPv6 prefix length for IP dimensions, 0 to 128.",
    )

    pps_threshold: Optional[int] = Field(
        validation_alias="pps_threshold",
        default=None,
        description="The minimum packets per second for a flow to count.",
    )

    filters_obj: Optional[QueryFilters] = Field(
        validation_alias="filters_obj", default=None
    )

    saved_filters: Optional[List[Optional[SavedFilterRef]]] = Field(
        validation_alias="saved_filters",
        default=None,
        description="Saved filters to apply.",
    )

    aggregates: Optional[List[Optional[Aggregate]]] = Field(
        validation_alias="aggregates",
        default=None,
        description="The aggregate columns. Kentik makes them from the metric when this is empty.",
    )

    matrixBy: Optional[List[str]] = Field(
        validation_alias="matrixBy",
        default=None,
        description="The matrix dimensions for a matrix chart.",
    )

    minsPolling: Optional[int] = Field(
        validation_alias="minsPolling",
        default=None,
        description="The flow aggregation window in minutes: 1, 5, 10, or 20.",
    )

    forceMinsPolling: Optional[bool] = Field(
        validation_alias="forceMinsPolling",
        default=None,
        description="Uses minsPolling instead of the automatic window.",
    )

    reAggInterval: Optional[int] = Field(
        validation_alias="reAggInterval",
        default=None,
        description="The re-aggregation interval in seconds.",
    )

    reAggFn: Optional[str] = Field(
        validation_alias="reAggFn",
        default=None,
        description="The re-aggregation function: avg, max, min, or none.",
    )

    viz_type: Optional[str] = Field(
        validation_alias="viz_type",
        default=None,
        description="The chart type: stackedArea, line, stackedBar, bar, pie, sankey, table, or matrix. Chart and URL only.",
    )

    show_overlay: Optional[bool] = Field(
        validation_alias="show_overlay",
        default=None,
        description="Shows the historical overlay. Chart and URL only.",
    )

    overlay_day: Optional[int] = Field(
        validation_alias="overlay_day",
        default=None,
        description="The number of days back for the overlay. Chart and URL only.",
    )

    sync_axes: Optional[bool] = Field(
        validation_alias="sync_axes",
        default=None,
        description="Syncs the left and right axis scales. Chart and URL only.",
    )

    query_title: Optional[str] = Field(
        validation_alias="query_title",
        default=None,
        description="The title shown on the chart.",
    )

    descriptor: Optional[str] = Field(
        validation_alias="descriptor",
        default=None,
        description="The series label when queries has more than one item.",
    )
