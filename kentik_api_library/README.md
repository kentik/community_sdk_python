# Kentik API python library.

This is a python wrapper for kentik rest api.
For more information on how to interact with kentik resources using this library, see examples in examples/ folder.

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
