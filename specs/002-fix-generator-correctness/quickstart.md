# Quickstart: Validating Fix Generator Correctness Defects

How to verify this feature end to end. Run every command from the repository
root.

## Prerequisites

- The repo environment installed: `make install`
- For the regeneration check, either a clean local schema checkout or network
  access for a fresh clone.

> [!WARNING]
> Confirm the local schema checkout is clean before regenerating from it.
> A corrupted checkout previously caused two Services to be dropped silently.
>
> ```bash
> git -C ../api-schema-public status --short   # expect no output
> ```
>
> If it is not clean, use plain `make generate`, which clones a fresh copy from
> GitHub instead.

## 1. Confirm the defects exist first

Run these **before** implementing, so the after-state means something.

```bash
# SC-001: pages naming a function that does not exist. Expect 42.
grep -l '_render_sphinx_stubs' docs/sphinx/services/*.md | wc -l

# The named function genuinely does not exist. Expect 0.
grep -c 'def _render_sphinx_stubs' scripts/generation/endpoint_docs.py

# SC-003: an internal directory documented as a Service. Expect a match.
head -3 src/kentik_api/gen/pb_companions/README.md
ls docs/sphinx/services/pb_companions.md

# SC-003: a real Service with no page. Expect "No such file".
ls docs/sphinx/services/core.md

# SC-004: assertions on a path production never runs. Expect test hits only.
grep -rn 'patch_schema_for_clean_names' --include='*.py' scripts/ tests/
```

## 2. Unit-level checks

```bash
make test-generator
```

Expected after implementation:

- Tests covering the shared Service rule pass, including that `pb_companions`
  is excluded and `core` is included.
- Tests covering provenance derivation pass.
- A forced extraction failure surfaces rather than being swallowed.
- The three retargeted schema-patching tests now exercise `patched_swagger`.

## 3. Full mocked suite

```bash
make lint
make typecheck
make test
```

All three must be clean. `make test` must not regress from its current count
other than by tests added or retargeted here.

## 4. Regeneration check: the primary acceptance gate

This is what proves FR-011 and SC-006. Unit tests alone cannot.

```bash
make generate local     # or: make generate   (fresh clone)
git status --short
```

**Expected diff, and nothing else:**

| Path | Expected change |
| --- | --- |
| `docs/sphinx/services/core.md` | added |
| `docs/sphinx/services/pb_companions.md` | deleted |
| `docs/sphinx/services/index.md` | toctree updated to match |
| `docs/sphinx/services/*.md` | provenance header corrected (42 files) |
| `src/kentik_api/gen/pb_companions/README.md` | no longer calls itself a Service |
| `src/kentik_api/gen/**/*.py` | **no change at all** |
| `src/kentik_api/client_mixin.py` | **no change at all** |

Confirm the last two rows explicitly, since together they are the FR-011
guarantee. `client_mixin.py` is generated but lives outside `gen/`, so a check
scoped to `gen/` alone would miss it:

```bash
git diff --stat -- 'src/kentik_api/gen/**/*.py' src/kentik_api/client_mixin.py
# expect empty output
```

Then confirm the corrected **set**, not just the total:

```bash
# SC-002: compare membership, since the totals already match today.
diff \
  <(ls -d src/kentik_api/gen/*/ | xargs -n1 basename \
      | grep -vE '^(__pycache__|pb_companions)$' | sort) \
  <(ls docs/sphinx/services/*.md | xargs -n1 basename \
      | sed 's/\.md$//' | grep -vE '^(README|index)$' | sort)
# expect no output: the sets are identical

# SC-001: zero pages naming a missing function. Expect 0.
grep -l '_render_sphinx_stubs' docs/sphinx/services/*.md | wc -l
```

> [!NOTE]
> The count stays **40** before and after. Only the membership changes:
> `core` joins, `pb_companions` leaves. The count was already correct for the
> wrong reason, which is why this defect went unnoticed.

## 5. Live API suites

```bash
make test-e2e
make test-e2e-grpc
```

Both must pass unchanged (SC-008). These need real credentials in a
project-root `.env` and are opt-in only; they are verification here, not part of
the default pipeline.

## 6. Documentation build

```bash
make docs
```

Sphinx must build without warnings about a missing or orphaned page, confirming
`core.md` is wired into the toctree and `pb_companions.md` is gone from it.

## Rollback

Every change is confined to the generator and its output. To revert, undo the
commits on `feat/fix-generator-correctness` and run `make generate` again; the
previous output is fully reproducible from the schema.
