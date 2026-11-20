# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The generated REST modules match the operations the swagger declares (T7).

`schema_operations.json` is written from the patched swagger on every
`uv run poe generate`, and CI's drift check keeps it in step with the schema, so
this runs without a schema checkout.
"""

from __future__ import annotations

import json
import re

import pytest

from scripts.generation._shared import (
    PROJECT_ROOT,
    SDK_OUTPUT_DIR,
    RestOperation,
    iter_service_dirs,
    parse_generated_rest_module,
)

_RECORD = json.loads((PROJECT_ROOT / "schema_operations.json").read_text("utf-8"))


def _generated(service: str) -> dict[str, RestOperation]:
    services_dir = SDK_OUTPUT_DIR / service / "services"
    return {
        f"{op.http_method.upper()} {op.path}": op
        for module in sorted(services_dir.glob("*.py"))
        if module.stem != service
        for op in parse_generated_rest_module(module)
    }


def _code_path(swagger_key: str) -> str:
    return re.sub(
        r"\{([^}]+)\}", lambda m: "{" + m[1].replace(".", "") + "}", swagger_key
    )


def test_the_record_covers_every_generated_service():
    with_operations = {d.name for d in iter_service_dirs() if _generated(d.name)}

    assert with_operations == {s for s, ops in _RECORD.items() if ops}


@pytest.mark.parametrize("service", sorted(_RECORD))
def test_generated_operations_match_the_swagger(service: str):
    generated = _generated(service)
    declared = {_code_path(key): spec for key, spec in _RECORD[service].items()}

    assert set(generated) == set(declared)
    for key, spec in declared.items():
        op = generated[key]
        params = {name for name, _, _ in op.params}
        assert op.operation_name == spec["operation"], key
        assert ("data" in params) == spec["body"], f"{key}: request body"
        missing = {p for p in spec["params"] if p.replace(".", "") not in params}
        assert not missing, f"{key}: no argument for {sorted(missing)}"
        assert str(op.expected_status) in spec["responses"], key
