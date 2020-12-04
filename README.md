# community_sdk_python


## Release process for kentik-api

Release process for kentik-api library is based on github repo tags. Every tag with format v[0-9].[0-9].[0-9] will trigger automatic build of package and publish it in PyPi repository (at the moment in testing instance).

To build and release package:
1. Make sure that all code that you want to release is in main branch
1. Create tag with format v[0-9].[0-9].[0-9] in github. [Releases](https://github.com/kentik/community_sdk_python/releases) -> Draft a new release -> Put tag version, name and description
1. Go to [Github Actions](https://github.com/kentik/community_sdk_python/actions)
