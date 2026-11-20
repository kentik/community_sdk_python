# Contract: dependency records

**Feature**: [../spec.md](../spec.md) | **Research**: [../research.md](../research.md)

## `pyproject.toml` after the change

Only the lines below change. Every other requirement stays as it is.

```toml
[project]
dependencies = [
    "python-dotenv>=1.2.4",   # was >=1.2.1
    # ...
    "pydantic>=2.14.0",       # was >=2.12.5
]

[dependency-groups]
dev = [
    # ...
    "ty>=0.0.84",             # was >=0.0.73
    "rumdl==0.3.0",           # new
]
test = [
    # ...
    "jinja2>=3.1.6",          # new, already locked
]
docs = [
    # ...
    "myst-parser>=5.1.0",     # was >=2.0.0
    "sphinxcontrib-mermaid>=1.0.0",  # unchanged, verified with Sphinx 9.1.0
]
```

The lock gains one package, rumdl (SC-004).

## `[tool.pytest]`

Replaces `[tool.pytest.ini_options]`. Same markers, same default
deselection, plus strict mode:

```toml
[tool.pytest]
pythonpath = ["."]
strict = true
markers = [ "...the three existing markers, unchanged..." ]
addopts = ["-m", "not e2e and not e2e_grpc and not e2e_mutating"]
```

## `api_surface.json` and `CHANGELOG.md`

- After `make generate`, `requirements` shows
  `"python-dotenv": "python-dotenv>=1.2.4"` and
  `"pydantic": "pydantic>=2.14.0"`. No other part of the surface changes.
- `CHANGELOG.md` Unreleased names both raised floors as breaking changes,
  with the text that `make check-changelog SINCE=HEAD` asks for.

## `docs/sphinx/dependencies.md`

A hand-written page in the `index.md` toctree:

```markdown
# Dependencies

| Dependency | Group | Purpose | Decision (audit 2026-10-17) |
| --- | --- | --- | --- |
| python-dotenv | runtime | Reads `.env` credentials into a dict | Keep, floor 1.2.4 |
| ... | ... | ... | ... |
```

`tests/smoke/test_declared_dependencies.py` fails when:

- a third-party import in `src/`, `scripts/`, or `tests/` maps to no
  declared dependency, and names the file and the module, or
- the table rows differ from the declared dependency names, and names the
  missing and extra rows.
