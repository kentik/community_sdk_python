# pylint: disable=redefined-outer-name
"""
Examples of using the typed labels API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, DeviceLabel


logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def run_crud() -> None:
    """
    Expected response is like:

    ### CREATE
    CreateResponse(id=2794, name='apitest-label-1', color='#0000FF', user_id='144319', company_id='74333', devices=[], created_date='2020-12-02T14:39:46.686Z', updated_date='2020-12-02T14:39:46.686Z')

    ### UPDATE
    UpdateResponse(id=2794, name='apitest-label-one', color='#FF0000', user_id='144319', company_id='74333', devices=[], created_date='2020-12-02T14:39:46.686Z', updated_date='2020-12-02T14:39:46.686Z')

    ### GET
    GetResponse(id=2794, name='apitest-label-one', color='#FF0000', user_id='144319', company_id='74333', devices=[], created_date='2020-12-02T14:39:46.686Z', updated_date='2020-12-02T14:39:46.686Z')

    ### DELETE
    DeleteResponse(success=True)
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### CREATE")
    label = DeviceLabel.new("apitest-label-1", "#0000FF")
    created = client.device_labels.create(label)
    print(created.__dict__)
    print()

    print("### UPDATE")
    created.name = "apitest-label-one"
    updated = client.device_labels.update(created)
    print(updated.__dict__)
    print()

    print("### GET")
    got = client.device_labels.get(updated.id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.device_labels.delete(updated.id)
    print(deleted)


def run_get_with_devices() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### GET")
    label_with_devices_id = 2752
    got = client.device_labels.get(label_with_devices_id)
    print(got.__dict__)
    print("devices:")
    for device in got.devices:
        print(device.__dict__)
    print()


def run_list() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)
    labels = client.device_labels.get_all()
    for l in labels:
        print(l.__dict__)


if __name__ == "__main__":
    # run_get_with_devices()
    run_crud()
    # run_list()
