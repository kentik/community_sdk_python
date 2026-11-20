# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Find flat outbound traffic on external links.

Needs the analytics extra: pip install "kentik-api[analytics]". Read-only.
"""

from datetime import UTC, datetime, timedelta

from kentik_api.analytics import (
    DataQueryDefinition,
    dedup_data_frame,
    flatness_analysis,
)
from kentik_api.client import KentikAPI
from kentik_api.devices import DeviceLookup
from pandas import DataFrame

BOUNDARY_FIELD = "i_dst_network_bndry_name"
QUERY_DEFINITION = {
    "query": {
        "queries": [
            {
                "bucket": "flow",
                "query": {
                    "starting_time": "{start:%Y-%m-%d %H:%M}",
                    "ending_time": "{end:%Y-%m-%d %H:%M}",
                    "lookback_seconds": 0,
                    "aggregates": [
                        {
                            "column": "f_sum_both_bytes",
                            "fn": "average",
                            "name": "avg_bits_per_sec",
                            "raw": True,
                        }
                    ],
                    # The API needs device names even for an account-wide query.
                    "device_name": "{devices}",
                    "dimension": ["i_device_id", "InterfaceID_dst"],
                    "fastData": "Full",
                    "filters_obj": {
                        "connector": "All",
                        "filterGroups": [
                            {
                                "connector": "All",
                                "filters": [
                                    {
                                        "filterField": BOUNDARY_FIELD,
                                        "filterValue": "external",
                                        "operator": "=",
                                    },
                                    {
                                        "filterField": "i_trf_termination",
                                        "filterValue": "outside",
                                        "operator": "=",
                                    },
                                ],
                                "not": False,
                            }
                        ],
                    },
                    "metric": "bytes",
                    "time_format": "UTC",
                    "topx": 125,
                },
            }
        ]
    },
    "mappings": {
        "all": {
            "link": {"source": "{i_device_name}:{output_port}"},
            "bps_out": {
                "source": "@TS.both_bits_per_sec.value",
                "type": "float64",
            },
            "avg_bps_out": {"source": "{avg_bits_per_sec}", "type": "float64"},
            "period": {
                "source": "@TS.both_bits_per_sec.period",
                "type": "int64",
            },
            "ts": {"source": "@TS.both_bits_per_sec.timestamp", "index": True},
        }
    },
}


def main() -> None:
    """Query outbound traffic and report links with flat traffic."""
    client = KentikAPI()  # loads KENTIK_EMAIL / KENTIK_API_TOKEN from .env
    devices = DeviceLookup.from_api(client)
    if devices.count < 1:
        print("No devices available.")
        return
    print(f"Got {devices.count} devices")

    query = DataQueryDefinition.from_dict(QUERY_DEFINITION)
    end = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(hours=23, minutes=59)
    names = ",".join(d.deviceName or "" for d in devices.all)
    df = query.get_data(client, start=start, end=end, devices=names).get(
        "flow", DataFrame()
    )
    if df.empty:
        print("Got no flow data")
        return
    df["link"] = df["link"].str.split(" : ").str[0]
    # topXdata can return duplicate time series entries.
    df = dedup_data_frame(df, ["ts", "link"])
    print(
        f"Got {df.shape[0]} entries, time resolution {df.period.max()} seconds"
    )

    flatness_limit = 0.5
    results = flatness_analysis(
        devices=devices,
        data=df,
        flatness_limit=flatness_limit,
        window=timedelta(minutes=60),
        min_valid=5,
        max_valid=100 - flatness_limit,
    )
    print("-" * 25)
    results.to_text()


if __name__ == "__main__":
    main()
