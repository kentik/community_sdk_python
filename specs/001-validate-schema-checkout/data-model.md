# Phase 1 Data Model: Validate Schema Checkout Before Generating

This feature's only "entity" is an in-memory validation result. Nothing is
persisted.

## SchemaValidationFailure

One swagger file that failed structural validation.

| Field | Type | Notes |
| --- | --- | --- |
| `path` | `Path` | Absolute path to the offending swagger file. |
| `reason` | `str` | Human-readable reason: `"could not read file: ..."`, `"file is empty"`, `"invalid JSON: ..."`, `"top-level JSON value is not an object"`, or `"missing required key(s): ..."`. |

Represented as a `TypedDict` (`SchemaValidationFailure`), matching the
existing `SwaggerFileMetadata` `TypedDict` convention already used in
`parity.py`.

`validate_schema_files(swagger_paths: list[Path]) -> list[SchemaValidationFailure]`
takes the list of already-selected swagger paths (values of
`selected_swagger_files`, flattened) and returns zero or more failures, with no
state transitions, no persistence.
