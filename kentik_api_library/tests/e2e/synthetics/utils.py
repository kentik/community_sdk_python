import os

from kentik_api import KentikAPI
from kentik_api.synthetics.synth_tests.base import ActivationSettings, HealthSettings
from kentik_api.utils import get_credentials

HEALTH = HealthSettings(
    latency_critical=90,
    latency_warning=60,
    latency_critical_stddev=9,
    latency_warning_stddev=6,
    packet_loss_critical=80,
    packet_loss_warning=50,
    jitter_critical=20,
    jitter_warning=10,
    jitter_critical_stddev=2,
    jitter_warning_stddev=1,
    http_latency_critical=250,
    http_latency_warning=150,
    http_latency_critical_stddev=25,
    http_latency_warning_stddev=15,
    http_valid_codes=[200, 201],
    dns_valid_codes=[1, 2, 3],
    unhealthy_subtest_threshold=1,
    activation=ActivationSettings(grace_period="1", time_unit="m", time_window="5", times="3"),
)

credentials_missing_str = "KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN env variables are required to run the test"
credentials_present = "KTAPI_AUTH_EMAIL" in os.environ and "KTAPI_AUTH_TOKEN" in os.environ


def client() -> KentikAPI:
    """Get KentikAPI client"""

    email, token = get_credentials()
    return KentikAPI(email, token)
