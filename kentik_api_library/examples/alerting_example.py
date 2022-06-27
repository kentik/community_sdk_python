# pylint: disable=redefined-outer-name
"""
Examples of using the alerting API
"""

import logging
from datetime import datetime

from examples.utils import pretty_print
from kentik_api import AlertFilter, KentikAPI, ManualMitigation
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud():
    """Runs example CRUD API calls and prints responses"""

    email, token = get_credentials()
    client = KentikAPI(email, token)

    start_time = datetime(2020, 10, 15, 22, 15, 0)
    end_time = datetime(2021, 1, 20, 9, 15, 0)

    print("### GET ALERTS")
    alerts = client.alerting.get_active_alerts(start_time, end_time)
    pretty_print(alerts)
    print()

    print("### GET ALERTS HISTORY")
    historical_alerts = client.alerting.get_alerts_history(start_time, end_time, AlertFilter.ALERT_KEY, "443")
    pretty_print(historical_alerts)
    print()

    print("### CREATE")
    # below ManualMitigation values are invalid and will cause error 404
    new_manual_mitigation = ManualMitigation("192.168.0.0/24", "1234", "12345", "20", "This is comment")
    try:
        created = client.alerting.create_manual_mitigation(new_manual_mitigation)
    except Exception:
        return

    pretty_print(created)
    print()


if __name__ == "__main__":
    run_crud()
