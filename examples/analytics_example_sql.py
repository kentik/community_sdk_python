import logging
from datetime import datetime, timedelta, timezone

from kentik_api import KentikAPI
from kentik_api.analytics import SQLQueryDefinition, flatness_analysis
from kentik_api.analytics.flatness import freq_to_seconds
from kentik_api.utils import DeviceCache, get_credentials

logging.basicConfig(level=logging.INFO)

query_data = {
    "query": "SELECT i_start_time, i_device_name, i_output_interface_description,"
    " sum(both_bytes) as f_sum_both_bytes FROM all_devices"
    " WHERE app_protocol in (0, 1, 2, 3, 4) AND i_fast_dataset = FALSE"
    " AND i_dst_network_bndry_name = $_kntq$external$_kntq$ AND i_trf_termination = $_kntq$outside$_kntq$"
    " AND i_start_time >= '{start}' AND i_start_time <= '{end}'"
    " GROUP BY i_start_time, i_device_name, i_output_interface_description ORDER BY f_sum_both_bytes DESC",
    "mapping": {
        "bytes_out": {"type": "int64", "source": "{f_sum_both_bytes}"},
        "link": {"source": "{i_device_name}:{i_output_interface_description}"},
        "ts": {"type": "time", "source": "{i_start_time}", "index": True},
    },
}


def main() -> None:
    api = KentikAPI(*get_credentials())
    query = SQLQueryDefinition.from_dict(query_data)
    print("Fetching devices ...", end=" ")
    devices = DeviceCache.from_api(api)
    if devices.count < 1:
        print("No devices available.")
        return
    print(f"Got {devices.count} devices")
    print("Fetching flow data (using SQL query) ...", end=" ")
    end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(hours=23, minutes=59)
    df = query.get_data(api, start=start, end=end)
    if df.shape[0] < 1:
        print("Got no flow data")
        return
    try:
        resolution = freq_to_seconds(df.index.unique().inferred_freq)
    except ValueError:
        resolution = float("NaN")
    print(f"Got {df.shape[0]} entries, time resolution {resolution} seconds")

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
