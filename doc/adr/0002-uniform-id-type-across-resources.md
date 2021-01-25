# 2. Common ID type across kentik resources

Date: 2021-01-19

## Status

Accepted

## Context

Kentik HTTP API returns "id" for different resources as integers or as strings.
Some resources reference others by id and then the id types sometimes differ.
Exposing this to the library client can provoke questions and cause confusion.

## Decision

Introduce common public type "ID" that will represent "id" across all resources.

## Consequences

Cleaner interface for the library user, less confusion, no need to convert between "id" types.
