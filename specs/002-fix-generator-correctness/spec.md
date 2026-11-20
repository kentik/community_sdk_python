# Feature Specification: Fix Generator Correctness Defects

**Feature Branch**: `feat/fix-generator-correctness`

**Created**: 2026-08-28

**Status**: Draft

**Input**: User description: "Fix four verified correctness defects in the SDK
generator, surfaced by an architecture review on 2026-08-28. Scope is limited to
defects that produce factually wrong output or false test confidence today. The
structural refactors that would prevent their recurrence are deliberately
deferred to a separate feature, so this one stays a small, reviewable,
obviously-correct diff."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A maintainer trusts the test suite to fail when production breaks (Priority: P1)

As an SDK maintainer, when I change how the generator patches a schema, I want
the test suite to fail if I break the code path that `make generate` actually
runs. Today three tests assert the behaviour of a helper that no production code
calls, so they stay green whether or not the real path works.

**Why this priority**: This is the only defect in scope that silently weakens
every future change. The other three produce wrong artifacts, which are visible.
This one hides breakage. It also removes a hazard: the untested helper rewrites
files inside the schema checkout in place, the same surface as the 2026-08-26
incident in which a corrupted checkout silently dropped two services.

**Independent Test**: Delete the unused helper and re-point its tests at the
path production runs. The suite must still pass, and must now fail if that real
path is broken.

**Acceptance Scenarios**:

1. **Given** the generator's schema-patching behaviour is covered by tests,
   **When** a maintainer inspects what those tests exercise, **Then** every
   assertion runs against the code path `make generate` uses.
2. **Given** the schema-patching code path is deliberately broken, **When** the
   test suite runs, **Then** at least one test fails.
3. **Given** the SDK is generated, **When** the run completes, **Then** no
   generator code has modified any file inside the schema checkout.

---

### User Story 2 - A reader sees only real API services in the documentation (Priority: P1)

As someone reading the SDK's documentation, I want the list of services to match
the Kentik API's actual services. Today an internal implementation directory is
presented as though it were an API service, and one real generated directory has
no reference page at all.

**Why this priority**: Wrong output that ships to readers. Both defects are
present on disk right now, and they partially cancel numerically, which is why
neither was noticed.

**Independent Test**: Regenerate, then compare the set of documented services
against the set of real services. Internal directories must be absent; every
real service must be present.

**Acceptance Scenarios**:

1. **Given** the SDK has been generated, **When** a reader browses the service
   documentation, **Then** no internal implementation directory appears as a
   service.
2. **Given** the SDK has been generated, **When** a reader browses the service
   documentation, **Then** every real generated service has a reference page.
3. **Given** the SDK has been generated, **When** the set of documented
   services is compared against the set of real services, **Then** the two sets
   are identical, with no extra and no missing member.

---

### User Story 3 - A contributor can trace generated output back to what produced it (Priority: P2)

As a contributor fixing wrong generated output, I want each generated file's
provenance note to name the code that actually wrote it, so I can go straight to
the right place. Today many generated pages name a function that does not exist.

**Why this priority**: It misdirects exactly the person who is already
debugging, but it costs them minutes rather than producing incorrect SDK
behaviour.

**Independent Test**: For every generated file that carries a provenance note,
confirm the function it names exists in the module it names.

**Acceptance Scenarios**:

1. **Given** a generated file carrying a provenance note, **When** a contributor
   looks up the named function, **Then** that function exists.
2. **Given** the code that writes a generated file is renamed, **When** the SDK
   is regenerated, **Then** the provenance note reflects the new name without a
   separate manual edit.

---

### User Story 4 - A maintainer is told when documentation extraction fails (Priority: P2)

As an SDK maintainer, when the generator cannot extract documentation for a
service, I want the run to tell me clearly. Today the failure is caught and
reduced to a console note, so the run reports success while publishing an empty
page.

**Why this priority**: Same silent-failure shape that previously removed the
entire gRPC runtime from an architecture diagram without any error. Lower than
P1 only because no instance is currently known to be firing.

**Independent Test**: Force an extraction failure for one service and confirm
the run surfaces it rather than completing quietly.

**Acceptance Scenarios**:

1. **Given** documentation extraction fails for a service, **When** the
   generation run completes, **Then** the failure is surfaced rather than
   reported as success.
2. **Given** documentation extraction succeeds for every service, **When** the
   generation run completes, **Then** behaviour is unchanged from today.

---

### Edge Cases

- What happens when a real service directory legitimately contains no
  operations? It must still be treated as a service and must not be silently
  reclassified as internal. Several such directories exist today.
- What happens when a new internal directory is added later? The rule that
  distinguishes internal directories from services must be stated in one place,
  so a new internal directory does not have to be excluded in several places
  independently.
- What happens to the published service count when the classification is
  corrected? It stays the same. There is one directory wrongly documented and
  one real service wrongly omitted, so the two errors cancel and the count is
  already correct for the wrong reason. Only the membership changes. This is
  precisely why the defect survived every count-based check, and it is why the
  acceptance criteria compare sets rather than totals.
- What happens if a provenance note is derived automatically and the writing
  function is private? The note must still resolve to a real function.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The generator MUST NOT retain a code path that modifies files
  inside the schema checkout in place.
- **FR-002**: Tests covering schema patching MUST exercise the code path used by
  a real generation run.
- **FR-003**: Generated documentation MUST exclude directories that are internal
  generator implementation rather than API services.
- **FR-004**: Generated documentation MUST include a reference page for every
  real generated service.
- **FR-005**: Any published count of services MUST continue to equal the number
  of real services. This currently holds and MUST NOT regress; because the count
  alone cannot distinguish a correct set from an offsetting pair of errors, it is
  a guard rather than a fix.
- **FR-006**: The rule distinguishing an internal directory from a service MUST
  be stated once and reused, rather than restated independently at each place
  that needs it.
- **FR-007**: Every provenance note in a generated file MUST name a function
  that exists in the module it names.
- **FR-008**: Provenance notes MUST be derived from the writing code rather than
  transcribed by hand, so a rename cannot leave them stale.
- **FR-009**: A documentation-extraction failure MUST be surfaced to the
  operator rather than reduced to a console note while the run reports success.
- **FR-010**: The generator's own description of its ordering guarantees MUST
  match what it actually enforces.
- **FR-011**: Generated SDK behaviour MUST be unchanged by this feature. Only
  documentation output, provenance notes, failure reporting, and tests change.
- **FR-012**: Hand-written documentation that states any fact this feature
  changes MUST be updated in the same change, so no document is left asserting
  something the code no longer does.
- **FR-013**: The project's domain glossary MUST state precisely which
  directories are Services, so the ambiguity that allowed an internal directory
  to be documented as a Service cannot recur through the glossary.
- **FR-014**: A helper defined in the generator MUST NOT be defined a second
  time in the test suite. A duplicate definition can drift from the original
  without any test noticing.

### Key Entities *(include if feature involves data)*

- **Service**: A top-level grouping of the Kentik API that maps to one generated
  directory and one attribute on the client. Defined in CONTEXT.md.
- **Internal directory**: A directory under the generated tree that supports
  generation but is not a Service, and therefore must not be documented as one.
- **Provenance note**: The comment in a generated file naming the code that
  wrote it.
- **Domain glossary**: The project's record of what each domain term means,
  including `Service`. Its precision is what keeps the classification rule from
  drifting back apart.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero generated files carry a provenance note naming a function
  that does not exist. The current count is 42.
- **SC-002**: The set of documented services is identical to the set of real
  services: no internal directory documented, no real service missing. The two
  sets currently differ by one member on each side, even though their totals
  already match.
- **SC-003**: No internal directory is documented as a service, and no real
  service is missing a reference page. Both faults are present today.
- **SC-004**: Every assertion about schema patching exercises the path a real
  generation run uses. Three assertions currently do not.
- **SC-005**: No generator code path can modify the schema checkout in place.
- **SC-006**: Regenerating produces no change to generated SDK behaviour: the
  only differences are documentation pages, provenance notes, and the corrected
  service count.
- **SC-007**: A forced documentation-extraction failure causes a visible,
  non-zero-exit failure rather than a silently empty page.
- **SC-008**: The full mocked test suite and the opt-in end-to-end suites pass
  unchanged.
- **SC-009**: No hand-written document contradicts another, or the code, about
  what this feature changes. Two such contradictions exist today and are fixed
  as part of this work.

## Assumptions

- The classification correction changes generated documentation output. This is
  intended, and the resulting regeneration diff will be reviewed deliberately
  rather than folded in silently.
- Correcting the published service count is in scope; deciding the count's value
  is not, because it follows from the corrected classification.
- Stating the internal-versus-service rule once satisfies FR-006. Introducing a
  full module for the Service concept is deliberately out of scope and deferred
  to a follow-up feature, so this feature stays small and low-risk.
- The broader structural work identified in the same review, namely consolidating
  generated-source introspection, making documentation renderers pure and
  testable, and encoding pipeline ordering constraints in interfaces, is out of
  scope here.
- Performance is explicitly not a goal. Measurement showed the relevant parsing
  costs about 58 milliseconds against a generation run of roughly 35 seconds,
  which is dominated by external tool invocations.
- The schema source and the hand-written versus generated split are unchanged by
  this feature.
