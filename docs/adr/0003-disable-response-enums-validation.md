# 3. Disable response Enums validation

Date: 2021-03-18

## Status

Accepted

## Context

Several resources of Kentik API v5 have fields with a defined set of values, which are represented as Enums in the code. Possible Enum values are specified in the API documentation ((e.g. [device types][1] or [device BGP settings][2])).

When Kentik API returns Enum values other than defined in the code, a _ValueError_ error is returned by the library. The documentation is not up to date with all possible Enum values, so such case is happening frequently.

[1]: https://kb.kentik.com/v3/Cb01.htm#Cb01-Supported_Device_Types
[2]: https://kb.kentik.com/v3/Cb01.htm#Cb01-Device_BGP_Settings

## Decision

The code will be modified not to return the error when unknown Enum is found in response.

## Consequences

Using of the library will be easier, because a whole category of errors will be eliminated.
