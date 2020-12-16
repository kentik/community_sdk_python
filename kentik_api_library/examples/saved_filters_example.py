# pylint: disable=redefined-outer-name
"""
Example of using the saved filters API
"""

import os
import sys
import logging
from typing import Tuple
from kentik_api import KentikAPI, SavedFilter, Filters, FilterGroups, Filter

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
    Runs example CRUD API calls and prints responses
    """

    email, token = get_auth_email_token()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_saved_filters = client.saved_filters.get_all()
    for i in all_saved_filters:
        print(i.__dict__)
    print()

    print("### CREATE")
    filter = Filter(filterField="dst_as", filterValue="81", operator="=")
    filter_groups = [FilterGroups(connector="All", not_=False, filters=[filter])]
    filters = Filters(connector="All", filterGroups=filter_groups)
    sfilter = SavedFilter(filter_name="test_filter1", filters=filters,
                          filter_description="This is test filter description")
    created = client.saved_filters.create(sfilter)
    print(created.__dict__)
    created_id = created.id
    print()

    print("### GET_ALL")
    all_saved_filters = client.saved_filters.get_all()
    for i in all_saved_filters:
        print(i.__dict__)
    print()

    print("### GET")
    got = client.saved_filters.get(created_id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.saved_filters.delete(created_id)
    print(deleted)

    # print("### UPDATE")
    # user = User(
    #     id=created.id,
    #     full_name="User Testing",
    # )
    # got = client.users.update(user)
    # print(got.__dict__)
    # print()


if __name__ == "__main__":
    run_crud()