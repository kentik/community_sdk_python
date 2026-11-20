# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Guards the declared runtime floors against the versions protoc stamps into stubs.

The generated stubs enforce their own minimums at import time: `*_pb2.py` calls
`ValidateProtobufRuntimeVersion` and `*_pb2_grpc.py` raises `RuntimeError`. Neither
is an `ImportError`, so a too-old runtime crashes the consumer rather than degrading
gracefully. That makes `pyproject.toml` the only thing standing between a downstream
`pip install` and an unimportable package.
"""

from __future__ import annotations

import importlib.metadata
import re
import tomllib

import pytest

from scripts.generation._shared import PROJECT_ROOT, SDK_OUTPUT_DIR

Version = tuple[int, ...]

# Spans the newlines protoc emits between the positional major/minor/patch arguments.
_PROTOBUF_GENCODE_RE = re.compile(
    r"ValidateProtobufRuntimeVersion\(\s*"
    r"_runtime_version\.Domain\.\w+,\s*"
    r"(\d+),\s*(\d+),\s*(\d+),",
    re.DOTALL,
)
_GRPC_GENCODE_RE = re.compile(r'^GRPC_GENERATED_VERSION\s*=\s*"([^"]+)"', re.MULTILINE)


def _parse_version(raw: str) -> Version:
    return tuple(int(part) for part in re.findall(r"\d+", raw))


def _requirement(specifiers: list, package: str) -> str:
    for spec in (s for s in specifiers if isinstance(s, str)):
        if re.match(rf"^{re.escape(package)}\s*[<>=!~\[]", spec):
            return spec
    pytest.fail(f"`{package}` is not declared in pyproject.toml: {specifiers}")


def _floor(requirement: str) -> Version:
    match = re.search(r"[><]=\s*([\d.]+)|==\s*([\d.]+)", requirement)
    assert match, f"no lower bound found in requirement {requirement!r}"
    return _parse_version(match.group(1) or match.group(2))


@pytest.fixture(scope="module")
def pyproject() -> dict:
    return tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def _gencode_versions(glob: str, pattern: re.Pattern[str]) -> dict[Version, list[str]]:
    """Maps each gencode version stamped into stubs matching glob to those stubs."""
    found: dict[Version, list[str]] = {}
    for stub in SDK_OUTPUT_DIR.rglob(glob):
        match = pattern.search(stub.read_text(encoding="utf-8"))
        if match:
            version = _parse_version(".".join(match.groups()))
            found.setdefault(version, []).append(
                stub.relative_to(SDK_OUTPUT_DIR).as_posix()
            )
    if not found:
        pytest.skip(
            f"no generated {glob} stubs present; run `uv run poe generate` first"
        )
    return found


def _describe(versions: dict[Version, list[str]]) -> str:
    return "; ".join(
        f"{'.'.join(map(str, version))} in {len(stubs)} stubs (e.g. {stubs[0]})"
        for version, stubs in sorted(versions.items())
    )


@pytest.fixture(scope="module")
def protobuf_gencode() -> dict[Version, list[str]]:
    return _gencode_versions("*_pb2.py", _PROTOBUF_GENCODE_RE)


@pytest.fixture(scope="module")
def grpc_gencode() -> dict[Version, list[str]]:
    return _gencode_versions("*_pb2_grpc.py", _GRPC_GENCODE_RE)


def test_protobuf_gencode_version_is_uniform(protobuf_gencode):
    """A split version means a partial regeneration was committed."""
    assert len(protobuf_gencode) == 1, (
        "generated *_pb2.py stubs disagree on protobuf gencode version: "
        f"{_describe(protobuf_gencode)}. "
        "Re-run `uv run poe generate` so every stub is built by one protoc."
    )


def test_grpc_gencode_version_is_uniform(grpc_gencode):
    assert len(grpc_gencode) == 1, (
        "generated *_pb2_grpc.py stubs disagree on grpcio gencode version: "
        f"{_describe(grpc_gencode)}. "
        "Re-run `uv run poe generate` so every stub is built by one protoc."
    )


def test_declared_protobuf_floor_covers_gencode(pyproject, protobuf_gencode):
    gencode = next(iter(protobuf_gencode))
    requirement = _requirement(pyproject["project"]["dependencies"], "protobuf")
    floor = _floor(requirement)
    assert floor >= gencode, (
        f"pyproject declares `{requirement}` but the generated stubs call "
        f"ValidateProtobufRuntimeVersion({'.'.join(map(str, gencode))}), which raises "
        f"VersionError on any older runtime. Raise the floor to "
        f">={'.'.join(map(str, gencode))}."
    )


def test_declared_protobuf_bound_excludes_next_major(pyproject, protobuf_gencode):
    """protobuf only guarantees gencode compatibility within a major version window."""
    major = next(iter(protobuf_gencode))[0]
    requirement = _requirement(pyproject["project"]["dependencies"], "protobuf")
    assert f"<{major + 1}" in requirement.replace(" ", ""), (
        f"pyproject declares `{requirement}`; gencode major is {major}, so the "
        f"requirement needs an upper bound of <{major + 1}."
    )


def test_declared_grpcio_floor_covers_gencode(pyproject, grpc_gencode):
    gencode = next(iter(grpc_gencode))
    requirement = _requirement(pyproject["project"]["dependencies"], "grpcio")
    floor = _floor(requirement)
    assert floor >= gencode, (
        f"pyproject declares `{requirement}` but the generated stubs set "
        f"GRPC_GENERATED_VERSION = {'.'.join(map(str, gencode))} and raise RuntimeError "
        f"on any older grpcio. Raise the floor to >={'.'.join(map(str, gencode))}."
    )


def test_grpcio_tools_is_pinned_exactly(pyproject, grpc_gencode):
    """An open floor makes `uv run poe generate` output depend on resolution date, not schema."""
    requirement = _requirement(pyproject["dependency-groups"]["dev"], "grpcio-tools")
    assert "==" in requirement, (
        f"pyproject declares `{requirement}`; pin grpcio-tools exactly so protoc "
        "stamps a reproducible version into the committed stubs."
    )
    assert _floor(requirement) == next(iter(grpc_gencode)), (
        f"pinned `{requirement}` does not match the gencode version stamped into the "
        "committed stubs. Re-run `uv run poe generate` after changing the pin."
    )


def test_openapi_generator_is_pinned_exactly(pyproject):
    """The fixups and custom templates match one generator's exact output."""
    requirement = _requirement(
        pyproject["dependency-groups"]["dev"], "openapi-python-generator"
    )
    assert "==" in requirement, (
        f"pyproject declares `{requirement}`; pin openapi-python-generator exactly "
        "so `uv run poe generate` output depends on the schema, not the resolution date."
    )
    installed = _parse_version(importlib.metadata.version("openapi-python-generator"))
    assert _floor(requirement) == installed, (
        f"pinned `{requirement}` but this environment has "
        f"{'.'.join(map(str, installed))}. Run `uv sync --locked`."
    )
