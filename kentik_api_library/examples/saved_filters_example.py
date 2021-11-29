# pylint: disable=redefined-outer-name
"""
Example of using the saved filters API
"""

import logging

from kentik_api import Filter, FilterGroups, Filters, KentikAPI, SavedFilter
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def run_crud() -> None:
    """
    Runs example CRUD API calls and prints responses
    """

    email, token = get_credentials()
    client = KentikAPI(email, token)

    print("### GET_ALL")
    all_saved_filters = client.saved_filters.get_all()
    for i in all_saved_filters:
        print(i.__dict__)
    print()

    print("### CREATE")
    filter_ = Filter(filterField="dst_as", filterValue="81", operator="=")
    filter_groups = [FilterGroups(connector="All", not_=False, filters=[filter_])]
    filters = Filters(connector="All", filterGroups=filter_groups)
    to_create = SavedFilter(
        filter_name="test_filter1", filters=filters, filter_description="This is test filter description"
    )
    created = client.saved_filters.create(to_create)
    print(created.__dict__)
    created_id = created.id
    print()

    print("### UPDATE")
    to_update = created
    to_update.filter_description = "Updated Saved Filter description"
    got = client.saved_filters.update(to_update)
    print(got.__dict__)
    print()

    print("### GET")
    got = client.saved_filters.get(created_id)
    print(got.__dict__)
    print()

    print("### DELETE")
    deleted = client.saved_filters.delete(created_id)
    print(deleted)


if __name__ == "__main__":
    run_crud()
