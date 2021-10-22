# community_sdk_python

## Release process for kentik-api

The release process for the kentik-api library is based on GitHub repo tags. Every tag with format v[0-9].[0-9].[0-9] will trigger an automatic build of the package and publish it in the PyPi repository.

To build and release package:
1. Make sure that all code that you want to release is in the main branch
1. Create a tag with format v[0-9].[0-9].[0-9] in GitHub. [Releases](https://github.com/kentik/community_sdk_python/releases) -> Draft a new release -> Put tag version, name and description
1. Go to [Github Actions](https://github.com/kentik/community_sdk_python/actions)


## Development state

Implemented API resources:
- users
- sites
- tags
- devices (with interfaces)
- device labels
- custom dimensions (with populators)
- custom applications
- saved filters
- my kentik portal
- query methods
- plans
- alerts
- alerts active
