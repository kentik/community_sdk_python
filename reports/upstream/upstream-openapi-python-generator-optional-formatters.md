# Draft issue for openapi-python-generator

Status: draft. A maintainer files it at
<https://github.com/MarcoMuellner/openapi-python-generator/issues> and adds
the issue link to the openapi-python-generator section of
`docs/sphinx/dependencies.md`.

---

**Title**: Make Black, isort, and orjson optional when `--formatter none` is used

**Body**:

openapi-python-generator 2.1.2 declares `black`, `isort`, and `orjson` as
required dependencies. A project that runs the generator with
`--formatter none` and the default JSON library uses none of them, but still
installs all three.

Our use: the Kentik Python SDK runs
`openapi-python-generator --formatter none ...` and formats the output with
Ruff. Our lock file holds Black, isort, and orjson only because the
generator requires them. No code in the project imports them.

Request: move the formatter and the alternative JSON library to optional
extras, for example `openapi-python-generator[black]` and
`openapi-python-generator[orjson]`. Keep the current default behavior for
users who install the extra.

We understand that this changes what a plain install gives users who rely on
the default Black formatter, so it may need a major version or a clear
error message when the formatter is missing.
