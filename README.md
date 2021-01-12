# community_sdk_python

## Installation with pip

1. Install the library using pip (currently the library is available under pypi test repository):  
```pip install --index-url https://pypi.org/simple --extra-index-url https://test.pypi.org/simple/ kentik-api```
1. Check installation successful - no errors should be reported:  
```python -c "import kentik_api"``` 
1. Run an example (Optional):
  ```bash
  export KTAPI_AUTH_EMAIL=<your kentik api credentials email>
  export KTAPI_AUTH_TOKEN=<your kentik api credentials token>
  python kentik_api_library/examples/sites_example.py
  ```

## Usage examples

For library usage examples please see: kentik_api_library/examples/

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
