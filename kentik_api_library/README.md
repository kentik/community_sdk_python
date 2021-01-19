# Kentik API python library.

This is a python wrapper for kentik rest api.
For more information on how to interact with kentik resources using this library, see examples in examples/ folder.

## Installation with pip

1. Install the library using pip (currently the library is available under pypi test repository):  
```pip3 install --index-url https://pypi.org/simple --extra-index-url https://test.pypi.org/simple/ kentik-api```
1. Check installation successful - no errors should be reported:  
```python3 -c "import kentik_api"```
1. Run an example (optional):
  ```bash
  export KTAPI_AUTH_EMAIL=<your kentik api credentials email>
  export KTAPI_AUTH_TOKEN=<your kentik api credentials token>
  python3 examples/sites_example.py
  ```

## Usage examples

For library usage examples please see: examples/  
List of available examples:
- [alerting_example.py](./examples/alerting_example.py) - create Manual Mitigation
- [applications_example.py](./examples/applications_example.py) - create/update/delete Custom Application
- [bulk_user_create.py](./examples/bulk_user_create.py) - create users from YAML file
- [devices_example.py](./examples/devices_example.py) - create/update/get/delete/list Devices
- [dimensions_example.py](./examples/dimensions_example.py) - create/update/get/delete/list Custom Dimensions, create/update/delete Populator
- [labels_example.py](./examples/labels_example.py) - create/update/get/delete/list Device Labels
- [my_kentik_portal_example.py](./examples/my_kentik_portal_example.py) - get/list Tenants, create/delete Tenant User
- [plans_example.py](./examples/plans_example.py) - list plans
- [queries_example.py](./examples/queries_example.py) - query for SQL/URL/data/chart
- [saved_filters_example.py](./examples/saved_filters_example.py) - create/update/get/delete/list Saved Filters
- [sites_example.py](./examples/sites_example.py) - create/update/get/delete/list Sites
- [tags_example.py](./examples/tags_example.py) - create/update/get/delete/list Tags
- [users_example.py](./examples/users_example.py) - create/update/get/delete/list Users

## Open-source libraries

This software uses the following open-source libraries:
- [dacite](https://pypi.org/project/dacite/) by Konrad Hałas - MIT License
- [requests](https://pypi.org/project/requests/) by Kenneth Reitz - Apache Software License (Apache 2.0)
- [typing-extensions](https://pypi.org/project/typing-extensions/) by  Guido van Rossum, Jukka Lehtosalo, Lukasz Langa, Michael Lee - PSFL License
