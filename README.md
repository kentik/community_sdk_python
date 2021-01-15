# community_sdk_python

## Installation with pip

1. Install the library using pip (currently the library is available under pypi test repository):  
```pip3 install --index-url https://pypi.org/simple --extra-index-url https://test.pypi.org/simple/ kentik-api```
1. Check installation successful - no errors should be reported:  
```python3 -c "import kentik_api"```
1. Run an example (optional):
  ```bash
  export KTAPI_AUTH_EMAIL=<your kentik api credentials email>
  export KTAPI_AUTH_TOKEN=<your kentik api credentials token>
  python3 kentik_api_library/examples/sites_example.py
  ```

## Usage examples

For library usage examples please see: kentik_api_library/examples/  
List of available examples:
- [alerting_example.py](./kentik_api_library/examples/alerting_example.py) - create Manual Mitigation
- [applications_example.py](./kentik_api_library/examples/applications_example.py) - create/update/delete Custom Application
- [bulk_user_create.py](./kentik_api_library/examples/bulk_user_create.py) - create users from YAML file
- [devices_example.py](./kentik_api_library/examples/devices_example.py) - create/update/get/delete/list Devices
- [dimensions_example.py](./kentik_api_library/examples/dimensions_example.py) - create/update/get/delete/list Custom Dimensions, create/update/delete Populator
- [labels_example.py](./kentik_api_library/examples/labels_example.py) - create/update/get/delete/list Device Labels
- [my_kentik_portal_example.py](./kentik_api_library/examples/my_kentik_portal_example.py) - get/list Tenants, create/delete Tenant User
- [plans_example.py](./kentik_api_library/examples/plans_example.py) - list plans
- [queries_example.py](./kentik_api_library/examples/queries_example.py) - query for SQL/URL/data/chart
- [saved_filters_example.py](./kentik_api_library/examples/saved_filters_example.py) - create/update/get/delete/list Saved Filters
- [sites_example.py](./kentik_api_library/examples/sites_example.py) - create/update/get/delete/list Sites
- [tags_example.py](./kentik_api_library/examples/tags_example.py) - create/update/get/delete/list Tags
- [users_example.py](./kentik_api_library/examples/users_example.py) - create/update/get/delete/list Users

## Release process for kentik-api

Release process for kentik-api library is based on github repo tags. Every tag with format v[0-9].[0-9].[0-9] will trigger automatic build of package and publish it in PyPi repository (at the moment in testing instance).

To build and release package:
1. Make sure that all code that you want to release is in main branch
1. Create tag with format v[0-9].[0-9].[0-9] in github. [Releases](https://github.com/kentik/community_sdk_python/releases) -> Draft a new release -> Put tag version, name and description
1. Go to [Github Actions](https://github.com/kentik/community_sdk_python/actions)


## Development state

Implemented API resources:
- users
- sites
- tags
- devices
- device labels
- custom dimensions
- custom applications
- saved filters
- my kentik portal
- query methods
- plans
- alerts

Working on:
- interfaces

To be implemented:
- alerts active
