# pylint: disable=redefined-outer-name
"""
Examples of using the typed custom dimensions API
"""

import os
import sys
import logging
import random
import string
from typing import Tuple
from kentik_api import KentikAPI, CustomDimension

logging.basicConfig(level=logging.INFO)


def get_auth_email_token() -> Tuple[str, str]:
    try:
        email = os.environ["KTAPI_AUTH_EMAIL"]
        token = os.environ["KTAPI_AUTH_TOKEN"]
        return email, token
    except KeyError:
        print("You have to specify KTAPI_AUTH_EMAIL and KTAPI_AUTH_TOKEN first")
        sys.exit(1)


def rand_uid() -> str:
    num_characters = 5
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=num_characters))


def run_crud() -> None:
    """
    Expected response is like:
    ### CREATE
    {'name': 'c_testapi_dim_vggr9', 'display_name': 'test_dimension', 'type': 'string', 'populators': [], '_id': 24015, '_company_id': '74333'}

    ### UPDATE
    {'name': 'c_testapi_dim_vggr9', 'display_name': 'test_dimension_updated', 'type': 'string', 'populators': [], '_id': 24015, '_company_id': '74333'}

    ### GET
    {'name': 'c_testapi_dim_vggr9', 'display_name': 'test_dimension_updated', 'type': 'string', 'populators': [], '_id': 24015, '_company_id': '74333'}

    ### DELETE
    True

    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### CREATE")
    dimension = CustomDimension(
        name="c_testapi_dim_" + rand_uid(),  # random uid as even deleted names are held for 1 year and must be unique
        display_name="test_dimension",
        type="string",
    )
    created = client.custom_dimensions.create(dimension)
    print(created.__dict__)
    print()

    print("### UPDATE")
    created.display_name = "test_dimension_updated"
    updated = client.custom_dimensions.update(created)
    print(updated.__dict__)
    print()

    print("### GET")
    got = client.custom_dimensions.get(updated.id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.custom_dimensions.delete(updated.id)
    print(deleted)


def run_list() -> None:
    email, token = get_auth_email_token()
    client = KentikAPI(email, token)
    dimensions = client.custom_dimensions.get_all()
    for d in dimensions:
        print(d.__dict__)


if __name__ == "__main__":
    run_crud()
    # run_list()
