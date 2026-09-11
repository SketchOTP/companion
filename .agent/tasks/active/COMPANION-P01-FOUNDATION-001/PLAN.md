# Phase 01 Execution Plan — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — VALIDATION RECORDED`

## Checkpoint 0 — authority and branch safety

- Reconstruct Notion and GitHub.
- Protect primary Graft edits.
- Create clean local secondary worktree and task branch.
- Complete authority acknowledgment.
- Research exact external versions and rights.

## Checkpoint 1 — repository and contracts

- Establish modular Rust workspace, Godot project location, contract/fixture/migration/test/evidence layout.
- Pin toolchains and exact artifact identities.
- Implement schemas, Rust types, canonicalization profile and golden/negative tests.
- Implement XDG path policy and unsafe-storage refusal.

## Checkpoint 2 — process, supervisor and storage shells

- Implement all six service shells.
- Implement project-owned supervisor, health, logging, restart/backoff and shutdown.
- Implement private synthetic direct-care channel and attack/lifecycle tests.
- Implement separate companion/care/vault development stores, migrations, integrity, backup and restore.

## Checkpoint 3 — Godot habitat and operator workflow

- Create exact Godot 4.7.2 bounded habitat shell.
- Implement screen selection, scaling, geometry persistence, visible degraded state, bridge handshake and headless smoke mode.
- Add bootstrap/build/run/health/injection/backup/restore/test commands.

## Checkpoint 4 — CI, provenance and integrated evidence

- Add pinned CI workflows and all required quality/security/provenance checks.
- Generate SBOM/license evidence.
- Run clean-clone verification.
- Run 1,000 deterministic cycles across retained seeds.
- Run 60-minute target-host soak and full failure matrix.

## Review 01 continuation plan

Implement and verify the resident supervisor and direct-care boundary first,
then replace subprocess persistence and unsafe XDG fallbacks. Bind live health
and actual packet-cycle runners to the same binaries, run the failure matrix,
and record any target-host or long-duration gaps as explicit non-pass outcomes.
No later-phase capability or dependency adoption is permitted.

## Checkpoint 5 — publication

- Inspect full diff and generated artifacts.
- Complete task documents and evidence map.
- Push one coherent PR to `main` without merging.
- Publish Notion report and update Issue #6.
- Re-fetch mutable records and return the canonical result.

Do not stop between checkpoints while the full phase remains feasible. A stop-condition blocker must identify the exact failed requirement, attempted evidence and smallest Architect decision needed.

## Checkpoint execution record

Checkpoints 0–3 are implemented in the clean secondary worktree. Checkpoint 4
has local locked builds, schema/artifact validation, direct-care and SQLite
smoke, headless and bounded visible Godot probes, SBOM generation, and a
3-seed/3,000-cycle matrix. The long-running 60-minute soak is executing as a
separate synthetic process and its sanitized result remains outside the
repository until completion. No system package, persistent service, product
runtime, media, model, or later-phase behavior was introduced.

## Architect Review 02 continuation — current run

The continuation hardens the resident control plane and contract boundary. It
adds post-initialization readiness markers, live child-state health (including
retained producer pidfd liveness), versioned health/fail/restart/rotate/shutdown
commands, direct-care channel rebuild with generation and capability rotation,
RustCrypto HMAC verification over canonical bytes, exact-source SQLite digest
gating and runtime compile-option identity, semantic schema fixtures/crosswalk,
and a real Godot 4.7 `StreamPeerUDS` handshake. The one-resident matrix now
drives 3,000 packets across retained seeds in a single supervisor lifetime;
the bounded failure matrix exercises observed restart/rotation/recovery.

The target-host 3,600-second injected soak remains intentionally `NOT RUN` in
this turn, and `/proc` census is `FAILED` when child dumpability hardening
blocks descriptor inspection. These are preserved as acceptance blockers, not
converted to passes.

## Evidence correction — 2026-09-10

The runtime validation was tightened to distinguish expected dumpable-hardening
`/proc` denial from the independent process-owned network census. The corrected
run passed the lifecycle and no-egress observations. No source, host policy, or
security setting was weakened; the 3,600-second continuous soak remains a
required, unrun gate.

## Final soak execution — 2026-09-10

The first full-duration run failed closed on a startup race before the control
socket was available. The harness was corrected to wait for explicit endpoint
readiness, then rerun for the full 3,600 seconds. The corrected result passed
with 60 samples, zero failures, and all four controlled injections; the exact
timestamps and bounded evidence ceiling are recorded in the evidence summary.

## Publication binding — 2026-09-10

The focused implementation/evidence commit is
`905a2c3980acfd8ee0ea2d58d3ba640701d9a7a0`; the summary binds this SHA. One
reconciliation commit remains allowed for executable modes and final branch
state only, followed by push and independent Architect review.

## CI correction — 2026-09-10

The initial push workflow exposed a health-query startup race and failed
closed. The runtime checker now waits for supervisor endpoint readiness;
publish this narrow correction and inspect both fresh push and pull-request
workflow results before reporting CI status.

Fresh push run `34488896386` and pull-request run `34488902059` both passed on
`12ee47bc5f4c556777eae43f35e3ec2f89f39e15`; the CI correction is complete and
the candidate is ready for independent Architect review.

## Final evidence-binding completion — 2026-09-10

The corrected 3,600-second resident soak and sanitized evidence manifest are
committed. Hash, fixture, ancestry, matrix, contract, and soak validation
passed, and a temporary tampered result failed closed. Publication is complete
on the existing branch; stop for independent Architect review.

## Review 03 closeout plan

1. Build and test the corrected resident controls and strict care validation.
2. Run the seed-diverse 3,000-message and 37-scenario matrices.
3. Complete the corrected resident soak and sanitize its output.
4. Bind fixture/result hashes and Git ancestry in the committed closeout
   manifest; run the validator and tamper-negative test.
5. Re-run required host-independent checks, inspect the final diff, publish on
   the existing PR, and stop for Architect review.

## Architect Review 04 execution record

The narrow correction replaced raw category fallthrough with exhaustive typed
injection, ran a truthful 3,000-message resident matrix over seeds 17/23/41,
and directly exercised twelve acceptance groups. Contract wire executions are
derived from the resident ordinary/direct-care run; Godot client state and
topology fallback are observed by the headless bridge probe. A focused
900-second resident regression passed lifecycle, store-fault, restart,
idempotency, checkout, and network-census assertions. The committed Review 04
bundle is validated by `validate_phase01_review04.py`; tamper-negative mutations
all fail. No later-phase behavior or dependency adoption is claimed.
