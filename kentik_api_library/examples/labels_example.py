# pylint: disable=redefined-outer-name
"""
Examples of using the typed labels API
"""

import logging

from examples.utils import pretty_print
from kentik_api import DeviceLabel, KentikAPI
from kentik_api.public.types import ID
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### CREATE")
    label = DeviceLabel.new("apitest-label-1", "#0000FF")
    created = client.device_labels.create(label)
    pretty_print(created)
    print()

    print("### UPDATE")
    created.name = "apitest-label-one"
    updated = client.device_labels.update(created)
    pretty_print(updated)
    print()

    print("### GET")
    got = client.device_labels.get(updated.id)
    pretty_print(got)
    print()

    print("### DELETE")
    deleted = client.device_labels.delete(updated.id)
    print(deleted)
    print()


def run_get_with_devices() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET")
    label_with_devices_id = ID("2752")
    got = client.device_labels.get(label_with_devices_id)
    pretty_print(got)
    print("devices:")
    pretty_print(got.devices)
    print()


def run_list() -> None:
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("GET ALL")
    labels = client.device_labels.get_all()
    pretty_print(labels)
    print()


if __name__ == "__main__":
    # run_get_with_devices()
    run_crud()
    run_list()
