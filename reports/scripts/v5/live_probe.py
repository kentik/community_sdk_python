"""Read-only probe of the V5 API: which endpoints still answer.

Run: uv run python reports/scripts/v5/live_probe.py [us|eu]

Sends only GET calls and the read-only query POSTs. Prints status codes,
top-level response keys, item counts, and quota headers. It never prints
credentials or record contents.
"""

import json
import sys
from pathlib import Path
from typing import Any

import httpx
from dotenv import dotenv_values

HOSTS = {"us": "https://api.kentik.com", "eu": "https://api.kentik.eu"}

QUERY: dict[str, Any] = {
    "query": {
        "metric": "bytes",
        "dimension": ["Traffic"],
        "topx": 8,
        "depth": 25,
        "fastData": "Auto",
        "outsort": "avg_bits_per_sec",
        "lookback_seconds": 3600,
        "hostname_lookup": False,
        "all_selected": False,
        "viz_type": "stackedArea",
    },
    "bucket": "Left +Y Axis",
    "bucketIndex": 0,
    "isOverlay": False,
}

GETS = [
    "/api/v5/users",
    "/api/v5/devices",
    "/api/v5/deviceLabels",
    "/api/v5/plans",
    "/api/v5/sites",
    "/api/v5/tags",
    "/api/v5/customdimensions",
    "/api/v5/saved-filters/custom",
    "/api/v5/customApplications",
    "/api/v5/mykentik/tenants",
    "/api/v5/alerts-active/alarms",
    "/api/v5/alerts-active/alerts-history",
    "/api/v5/batch/00000000-0000-0000-0000-000000000000/status",
]

POSTS = [
    ("/api/v5/query/topXdata", {"queries": [QUERY]}),
    ("/api/next/v5/query/topXdata", {"queries": [QUERY]}),
    ("/api/v5/query/topXchart", {"queries": [QUERY], "imageType": "svg"}),
    ("/api/v5/query/url", {"queries": [QUERY]}),
    ("/api/v5/query/sql", {"query": "SELECT 1"}),
]


def shape(body: object) -> str:
    if isinstance(body, dict):
        parts = []
        for key, value in body.items():
            size = f"[{len(value)}]" if isinstance(value, (list, dict, str)) else ""
            parts.append(f"{key}:{type(value).__name__}{size}")
        return "{" + ", ".join(parts) + "}"
    if isinstance(body, list):
        return f"list[{len(body)}]"
    return f"{type(body).__name__}[{len(str(body))}]"


def report(method: str, path: str, response: httpx.Response) -> None:
    quota = {
        k: v
        for k, v in response.headers.items()
        if "ratelimit" in k.lower() or k.lower() == "retry-after"
    }
    try:
        body = shape(response.json())
    except json.JSONDecodeError:
        body = f"non-JSON {response.headers.get('content-type')} {len(response.content)} bytes"
    print(
        f"{response.status_code} {method} {path}\n    body: {body}\n    quota: {quota}"
    )
    if response.status_code >= 400 and response.content:
        print(f"    error: {response.text[:200]}")


def main() -> None:
    region = sys.argv[1] if len(sys.argv) > 1 else "us"
    env = dotenv_values(Path(__file__).resolve().parents[3] / ".env")
    headers = {
        "X-CH-Auth-Email": env["KENTIK_EMAIL"] or "",
        "X-CH-Auth-API-Token": env["KENTIK_API_TOKEN"] or "",
    }
    with httpx.Client(base_url=HOSTS[region], headers=headers, timeout=120) as client:
        for path in GETS:
            report("GET", path, client.get(path))
        devices = client.get("/api/v5/devices").json()["devices"]
        QUERY["query"]["device_name"] = devices[0]["device_name"]
        for path, payload in POSTS:
            try:
                report("POST", path, client.post(path, json=payload))
            except httpx.TransportError as exc:
                print(f"--- POST {path}\n    transport error: {type(exc).__name__}")


if __name__ == "__main__":
    main()
