# Quickstart: validate dependency feature adoption

**Feature**: [spec.md](spec.md) | **Contracts**: [contracts/](contracts/)

Run these steps from the repository root after implementation. Step 6 needs
the network to download packages. No step calls the Kentik API.

## 1. Lock and install

```sh
uv lock --check
uv sync --locked
git diff "$(git merge-base HEAD feat/v6-sdk)" -- uv.lock | grep -E '^[-+]name = '
```

Expected: the lock is current. Compared with the base branch, it adds one
package, rumdl, and changes no locked version.

## 2. Lint gates

```sh
make lint
git status --short
uv run ruff check --output-format github .
uv run ruff format --check --output-format github .
uv run rumdl check --output-format github .
```

Expected: `make lint` changes no file, and the three checks report no
finding. See [contracts/lint.md](contracts/lint.md).

## 3. A finding fails the check

```sh
printf '# Probe\n\n```python\nx=1\n```\n- a\n' > docs/sphinx/probe.md
uv run ruff format --check docs/sphinx/probe.md   # fails: would reformat
uv run rumdl check docs/sphinx/probe.md            # fails: MD032
rm docs/sphinx/probe.md
```

Expected: both commands exit non-zero and name the file and line.

## 4. Regeneration is stable

```sh
make generate
git status --short
```

Expected: no change after the committed regeneration. See
[contracts/generator.md](contracts/generator.md).

## 5. Tests, types, docs, changelog

```sh
make test
make typecheck
make check-specs
make check-changelog SINCE="$(git merge-base HEAD feat/v6-sdk)"
uv run sphinx-build -W --keep-going -b html docs/sphinx docs/build/html
```

Expected: all pass. In `docs/build/html/guides/generation.html`, the
warning shows as an admonition with no `[!WARNING]` text.

Then add `@pytest.mark.typo` to any mocked test and run `make test`.
Expected: pytest stops with an error about the unknown marker. Revert the
change.

## 6. Lowest permitted versions

```sh
uv venv "$TMPDIR/low" -p 3.12
uv pip install --python "$TMPDIR/low" --resolution lowest-direct -e . \
  "autodoc-pydantic>=2.2.0" "myst-parser>=5.1.0" "sphinx>=9.1.0" \
  "sphinx-book-theme>=1.1.0" "sphinxcontrib-mermaid>=1.0.0" "ty>=0.0.84"
uv pip list --python "$TMPDIR/low" | grep -E "^(ty|pydantic|python-dotenv|myst-parser) "
"$TMPDIR/low/bin/sphinx-build" -W --keep-going -b html docs/sphinx "$TMPDIR/low-html"
rm -rf "$TMPDIR/low" "$TMPDIR/low-html"
```

Expected: ty 0.0.84, pydantic 2.14.0, python-dotenv 1.2.4, MyST-Parser
5.1.0, and the docs build exits 0.

## 7. Import check catches an undeclared package

Add `import idna` at the top of any file in `tests/runtime/` and run
`uv run pytest tests/smoke/test_declared_dependencies.py`. Expected: it
fails and names the file and `idna`. Revert the change.

## 8. Python versions

CI runs the mocked suite on Python 3.12, 3.13, and 3.14 (SC-007). Locally:

```sh
for v in 3.12 3.13 3.14; do uv run -p "$v" pytest tests/ -q; done
```
