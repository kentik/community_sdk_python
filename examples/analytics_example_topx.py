import logging
from datetime import datetime, timedelta, timezone

from pandas import DataFrame

from kentik_api import KentikAPI
from kentik_api.analytics import DataQueryDefinition, dedup_data_frame, flatness_analysis
from kentik_api.utils import DeviceCache, get_credentials

logging.basicConfig(level=logging.INFO)

query_data = {
    "query": {
        "queries": [
            {
                "bucket": "flow",
                "query": {
                    "starting_time": "{start}",
                    "ending_time": "{end}",
                    "aggregates": [
                        {
                            "column": "f_sum_both_bytes",
                            "fn": "average",
                            "name": "avg_bits_per_sec",
                            "raw": True,
                        }
                    ],
                    "all_devices": True,
                    "dimension": ["i_device_id", "InterfaceID_dst"],
                    "fastData": "Full",
                    "filters": {
                        "connector": "All",
                        "filterGroups": [
                            {
                                "connector": "All",
                                "filters": [
                                    {
                                        "filterField": "i_dst_network_bndry_name",
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
                    "metric": ["bytes"],
                    "time_format": "UTC",
                    "topx": 125,
                },
            }
        ]
    },
    "mappings": {
        "all": {
            "link": {
                "source": "{i_device_name}:{output_port}",
                "type": '@fixup: lambda x: x.split(" : ")[0]',
            },
            "bps_out": {"source": "@TS.both_bits_per_sec.value", "type": "float64"},
            "avg_bps_out": {"source": "{avg_bits_per_sec}", "type": "float64"},
            "period": {"source": "@TS.both_bits_per_sec.period", "type": "int64"},
            "ts": {"source": "@TS.both_bits_per_sec.timestamp", "index": True},
        }
    },
}


def main() -> None:
    api = KentikAPI(*get_credentials())
    query = DataQueryDefinition.from_dict(query_data)
    print("Fetching devices ...", end=" ")
    devices = DeviceCache.from_api(api)
    if devices.count < 1:
        print("No devices available.")
        return
    print(f"Got {devices.count} devices")
    print("Fetching flow data (using topXdata query) ...", end=" ")
    end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(hours=23, minutes=59)
    r = query.get_data(api, start=start, end=end)
    df = r.get("flow", DataFrame())
    if df.shape[0] < 1:
        print("Got no flow data")
        return
    print(f"Got {df.shape[0]} entries, time resolution {df.period.max()} seconds")
    # topXdata query may return duplicate time series entries, need to de-duplicate
    df = dedup_data_frame(df, ["ts", "link"])

    time_window = timedelta(minutes=60)
    flatness_limit = 0.5
    min_utilization = 5
    max_utilization = 100 - flatness_limit

    print("Analysis parameters:")
    print("\ttime_window:     ", time_window)
    print("\tflatness_limit:  ", flatness_limit)
    print("\tmin_utilization: ", min_utilization)
    print("\tmax_utilization: ", max_utilization)

    results = flatness_analysis(
        devices=devices,
        data=df,
        flatness_limit=flatness_limit,
        window=time_window,
        min_valid=min_utilization,
        max_valid=max_utilization,
    )

    print("-" * 25)
    results.to_text()


if __name__ == "__main__":
    main()
