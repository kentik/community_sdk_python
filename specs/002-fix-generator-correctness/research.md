# Phase 0 Research: Fix Generator Correctness Defects

All findings verified against code or generated output on disk on 2026-08-28.

## Decision 1: The correct Service rule already exists; adopt it rather than invent one

**Decision**: Define a Service as any directory under `src/kentik_api/gen/`
except `__pycache__` and `pb_companions`. Put that rule in
`scripts/generation/_shared.py` and have all nine call sites use it.

**Rationale**: This is already the rule in
`parity.validate_generated_service_parity()`, and parity passes today, so the
rule is proven correct against the schema. Evidence gathered by classifying all
41 generated directories:

| Group | Count | Has wrapper | Has `models/` | Mounted on client |
| --- | --- | --- | --- | --- |
| Ordinary Services | 34 | yes | yes | yes |
| Operationless Services | 6 | no | yes | no |
| Generator-internal | 1 | no | **no** | no |

The 6 operationless Services (`core`, `deviceconf`, `diagnostic`, `kptr`,
`monitoring`, `net`) are real schema-derived Service directories that produced
no REST operations, so no wrapper was emitted. Five of them already have
documentation pages, confirming that operationless Services are meant to be
documented. Only `core` lacks one, and only because `endpoint_docs.py` carries a
hardcoded `"core"` literal in its exclusion set.

`pb_companions` is the sole directory the generator creates itself, in
`_compile_proto_companions()` (`generate_sdk.py:241`). It is not schema-derived,
it has no `models/`, and `parity.py:83` already excludes it by name.

**Correction to an earlier assumption**: the published service count does **not**
change. There are 41 directories minus 1 internal, so 40 Services, and 40 pages
exist today. The count is already right; the **set** is wrong. Adding `core.md`
and removing `pb_companions.md` keeps the total at 40. This matters because it
explains why the defect survived: the two errors cancel exactly, so every count
check passes while the content is wrong.

**Alternatives considered**:

- *Derive Service-ness from "has a wrapper".* Rejected: it would silently drop
  the 6 operationless Services, five of which are documented today. It would
  also make the rule depend on generation order, since wrappers are written
  after the directories exist.
- *Derive it from "has `models/`".* Rejected: it produces the right answer today
  purely by coincidence. A future generator-internal directory that happens to
  contain models would be misclassified, which is the exact failure mode being
  fixed.
- *Re-derive Service-ness from the schema tree at each call site.* Rejected: the
  schema is only available inside the generation window, but several call sites
  (notably `tests/_discovery.py`) run with no schema checkout present.

## Decision 2: Derive provenance from the writing function, not a literal

**Decision**: Build the `AUTO-GENERATED` header from the writing function's own
`__name__` and module, rather than a hand-typed string.

**Rationale**: Two hardcoded strings at `endpoint_docs.py:715` and `:792` name
`_render_sphinx_stubs()`, which does not exist anywhere in the repo. The real
writer is `render_endpoint_docs()` at line 674. Those two literals produce the
same wrong header on 42 generated pages. Deriving the name makes a future rename
self-correcting, and it applies the rule this repo already learned when
`_grpc_stub_method_name` replaced a re-derived name: read the name, do not
retype it.

**Alternatives considered**:

- *Just correct the two literals.* Rejected: it fixes today's 42 files but
  leaves the same trap for the next rename. The derived form costs no more.
- *Drop provenance headers entirely.* Rejected: they are load-bearing for a repo
  whose central rule is "never hand-edit generated files"; the header is how a
  reader knows which generator wrote a file.

## Decision 3: Let documentation extraction failures propagate

**Decision**: Remove the blanket `except Exception` in
`EndpointDocsCollector.extract()` (`endpoint_docs.py:867-873`) so a failure
aborts the run instead of printing a warning and continuing.

**Rationale**: The current handler turns a real failure into an empty
documentation page while the run reports success. That is the same silent-failure
shape as the `_module_group()` incident, where a `None` return into a caller that
skipped `None` erased the entire gRPC runtime from an architecture diagram with
no error anywhere. Generation is an offline, re-runnable developer command, so
failing loudly costs a re-run and never costs production availability.

**Alternatives considered**:

- *Collect failures and raise once at the end.* Deferred, not rejected. It gives
  a better report when several services fail at once, but it adds accumulation
  state to a class whose shape is itself under review in the follow-up feature.
  Raising immediately is the smaller change and satisfies FR-009.
- *Keep the warning but exit non-zero at the end.* Rejected: the run would keep
  writing output derived from a known-bad extraction, so the wrong page could
  still be committed.

## Decision 4: Delete the dead in-place schema mutator and retarget its tests

**Decision**: Delete `patch_schema_for_clean_names` (`generate_sdk.py:198`) and
rewrite its three tests against `patched_swagger` (`generate_sdk.py:173`).

**Rationale**: Verified zero production call sites; the only three callers are
tests at `test_generate_sdk.py:113`, `:149`, `:173`. Its own docstring already
directs callers elsewhere: "Prefer `patched_swagger()` for new call sites to
avoid mutating the schema checkout." The live path, `patched_swagger`, applies
the same two transforms (`clean_schema_names`, `inline_request_body_refs`) but
writes to a `NamedTemporaryFile` and never modifies the original.

Two independent reasons to remove rather than keep:

1. **False confidence.** The requestBody-inlining assertions currently pass
   whether or not `patched_swagger` wires those transforms in correctly.
2. **Standing hazard.** It writes back over files inside the schema checkout,
   the same surface as the 2026-08-26 incident in which a corrupted checkout
   silently dropped two Services.

Coverage is not lost: `clean_schema_names` and `inline_request_body_refs` are
already unit-tested as pure functions, including no-mutation assertions, and
`patched_swagger` already has `test_patched_swagger_does_not_modify_original`.

**Alternatives considered**:

- *Keep it and mark it deprecated.* Rejected: it is importable and tested, so it
  remains a live hazard, and the deprecation note it already carries has not
  prevented the tests from depending on it.

## Decision 5: Verify by regenerating and diffing, not by unit tests alone

**Decision**: Treat a clean regeneration plus `git diff` on
`src/kentik_api/gen/` as the primary acceptance check for FR-011.

**Rationale**: The repo has repeatedly hit bugs where a helper was correct in
isolation but wired in wrong, so unit tests on the changed helpers cannot by
themselves prove the pipeline still emits identical SDK code. A regeneration
diff can. The expected diff is exactly: `docs/sphinx/services/core.md` added,
`docs/sphinx/services/pb_companions.md` removed, `pb_companions`'s README no
longer describing itself as a Service, and 42 provenance headers corrected. Any
change under `src/kentik_api/gen/**/*.py` means something went wrong.

Per the constitution's schema-checkout guardrail, confirm
`git -C ../api-schema-public status --short` is clean before regenerating, or
regenerate from a fresh clone with plain `make generate`.

**Alternatives considered**:

- *Rely on the mocked suites only.* Rejected: they auto-discover from generated
  code, so they would pass against subtly wrong regenerated output.
