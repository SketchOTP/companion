# Architect Review 02 — COMPANION-P01-FOUNDATION-001

## Verdict

`CONTINUE — PHASE 01 NOT ACCEPTED; ONE FINAL PHASE-COMPLETION RUN REQUIRED`

- Reviewed PR: `#7`
- Reviewed branch: `codex/p01-foundation-001`
- Reviewed head: `3fbc4284d2a0053034c0e5dea2cd97cb61e6330f`
- Required PR state: `OPEN / DRAFT / UNMERGED`
- GitHub Issue: `#6 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 02 and later: `CLOSED`
- Product capability: `NOT ESTABLISHED`
- Canonical Notion review: https://app.notion.com/p/3d7833cb27ff810ba5abd1e1c4ee2237

## Review scope

The Architect independently re-synchronized GitHub and Notion, inspected PR #7,
the final branch head, the post-review implementation commits, both green CI
runs, and the current Codex report. The review covered the Rust workspace,
resident supervisor, direct-care transport, SQLite FFI/build path, XDG policy,
contract/schema system, Godot habitat, health/logging, integration/failure/soak
drivers, bootstrap, CI, SBOM, and evidence claims.

Current primary documentation was rechecked for Linux descriptor inheritance and
close-on-exec behavior, RustCrypto HMAC verification, Godot 4.7 Unix-domain
sockets and display APIs, XDG placement, JSON Schema 2020-12 validation, and
SQLite source/runtime identity.

## Retained implementation progress

Preserve and build on:

1. Modular Rust workspace and Rust 1.98.1 pin.
2. Role-specific binaries for the six Phase 01 process roles.
3. Direct SQLite FFI, prepared-statement direction, authority stores, and
   committed migration roots.
4. Corrected XDG defaults and fail-closed path error types.
5. Resident supervisor control socket and process registry direction.
6. Private capability-pipe direction, `SOCK_SEQPACKET`, kernel credentials, and
   care-owned receipt storage.
7. OS boot ID and monotonic-clock utilities.
8. Nine schema files and matching Rust type names.
9. Godot 4.7.2 project, display-topology helper, and bounded window shell.
10. Green CI history, full-history checkout correction, scripts, task records,
    and protected-work handling.

These are implementation assets. They do not establish Phase 01 completion.

## Material acceptance failures

### 1. Resident health and supervision remain self-asserting

The supervisor health response marks every registry entry `running`, `ready`,
and `healthy` without checking current process state or consuming a
post-initialization readiness protocol. Care coverage depends on registry
presence rather than a live `care-core` plus usable care store. Serialization
failure falls back to `{}` instead of failing visibly.

`sensor-gateway` and `care-core` terminate after a finite packet count. The
restart path replaces selected ordinary children only; it does not atomically
rebuild the producer/care channel, rotate the capability, retain and evaluate a
pidfd, restore care coverage, or revoke the previous direct-care generation.
The producer pidfd is opened and then dropped after a log statement. Services
emit `ready` before role-specific initialization completes.

### 2. The direct-care contract and authentication implementation disagree

The committed `SafetyCandidate` schema and Rust type require a plain
`capability` field. The producer instead emits a `mac` field and no
`capability`. The actual wire packet therefore does not satisfy its own
contract.

The current MAC is a handwritten HMAC-like construction and is compared with
ordinary string equality. Replace it with one exact reviewed RustCrypto `hmac`
crate and its verification API. Authenticate canonical bytes under a versioned
domain separator. Capability secret bytes must never enter an external schema,
message, environment, argv, log, health record, or filesystem record.

Retain a live pidfd or equivalent race-resistant handle for the active producer
generation and use it in the authorization lifecycle. Logging that
`pidfd_open()` succeeded is not binding.

### 3. The 3,000-message result is not one resident integration matrix

The driver runs `ops-supervisor --once` separately for each seed. It sends valid
candidates plus one duplicate, then exits. It does not keep one resident
foundation alive through replay, malformed framing, unsupported schema, stale
generation, stale MAC, producer replacement, care restart, companion restart,
store persistence, store failure, and recovery. The retained seed currently
does not alter the system behavior.

### 4. The failure matrix does not exercise the named failure properties

The care-outage case checks only that `care-core` text is absent; it does not
query an explicit degraded coverage state. The Godot reconnect case launches
`godot-bridge --once` and searches stdout; it does not connect Godot,
disconnect the bridge, or reconnect. The invalid-contract case is a missing-FD
startup failure, not malformed contract handling.

Readiness timeout, restart/backoff, crash loop, stale channel, producer
rotation, care-store loss, store corruption, vault denial, bridge loss, display
loss, and recovery remain untested.

### 5. Exact SQLite identity remains fail-open in normal and CI builds

`build.rs` compiles the accepted amalgamation only when
`COMPANION_SQLITE_SOURCE` is supplied. Otherwise it links a hard-coded host
`libsqlite3.so.0`. Current CI does not supply the exact source, so green Rust and
persistence checks do not prove SQLite 3.53.4.

Make exact-source identity mandatory for Phase 01 acceptance builds and CI.
Verify the accepted source digest before compilation and assert
`sqlite3_libversion()`, `sqlite3_sourceid()`, and compile options at runtime. A
host-library fallback may exist only behind an explicit nonauthoritative
developer feature and may not pass Phase 01 verification.

Broad SQLite `xWrite`, `xTruncate`, shared-memory, realistic power-cut,
lifetime, and endurance qualification is deferred to later resilience and
release phases. It is not a Phase 01 blocker. Phase 01 still requires bounded
restart/crash, read-only or disk-full, migration rejection, checkpoint,
integrity, backup, and full restore-equivalence tests against the exact build.

### 6. Contract validation is a name crosswalk, not a compatibility gate

The drift script checks only that expected struct names occur. The schema
validator structurally scans all schemas but validates only the event fixture.
There is no complete positive/negative fixture set and no deterministic
field/type/required/bounds comparison.

The safety-candidate mismatch demonstrates that the current gate can pass while
schema, Rust type, and wire implementation disagree. Establish one
authoritative contract representation or a semantic crosswalk that compares
every field, type, required/optional rule, enum, bound, and unknown-field
policy. Exercise all nine schemas with pinned Draft 2020-12 validation and Rust
round trips.

### 7. The Godot bridge is not end-to-end

Rust writes `bridge-state.json` beneath the XDG runtime directory. Godot polls
`user://foundation_bridge_v1.json`. These are different paths and filenames, so
no shared handshake exists.

The habitat hard-codes screen index `0`, does not select the current screen,
restores size but not position or output identity, and does not poll topology
changes. Use Godot 4.7 `StreamPeerUDS` or an equivalent real versioned local
channel to `godot-bridge`, then test connection, incompatibility, bridge
restart, Godot restart, selected-screen placement, geometry restoration,
simulated display loss, and safe visible fallback.

### 8. Health, logging, and network evidence remain incomplete

Control-plane health must derive from live process handles, readiness
acknowledgments, store checks, active channel generation, care receipt
availability, and Godot state. Do not hard-code `healthy`, `ready`, or
`deny_by_default`.

Add monotonic timestamp, UTC observation and uncertainty, and actual
monotonically increasing sequences to runtime records. A logging serialization
or write failure must be visible and fail the affected readiness path.

The runtime checker ignores `/proc` inspection failures and only examines PIDs
returned by self-asserting health. Record census completeness and fail when a
required process cannot be inspected.

### 9. CI, bootstrap, vulnerability, license, SBOM, and evidence are incomplete

CI does not compile exact SQLite 3.53.4, execute Godot 4.7.2, run the complete
resident failure suite, or upload sanitized evidence. The claimed vulnerability
and license check is an allow/deny string policy, not a vulnerability-database
or license-policy result.

The SBOM uses `NOASSERTION` licenses, placeholder checksum values, a placeholder
timestamp, and package IDs that can collide across versions. It is not a
complete SPDX evidence artifact.

Bootstrap still assumes the old private qualification cache exists. Add an
idempotent fetch-or-verify path for official artifacts with exact URLs and
digests while retaining offline cache reuse and avoiding system modification.

### 10. The continuously resident soak was not run and its driver is not ready

The result correctly reports the required 3,600-second injected resident soak
as `NOT RUN`. The current driver also hard-codes
`resident_supervisor=true` and `network_socket_count=0`, injects no required
failures, records no CPU/RSS or store/checkpoint state, and pipes child output
without continuously draining it.

Replace all conclusion constants with observations. Run one supervisor for at
least 3,600 seconds and, during that same lifetime, inject companion
failure/recovery, producer replacement with generation and secret rotation,
Godot disconnect/reconnect, and care outage/recovery.

## Final phase-completion objective

Complete Roadmap Phase 01 in this existing PR. Do not split this into
micro-directives. Return only after the complete gate passes or one genuine
stop condition is proven.

### Workstream A — resident supervisor and control plane

- Define child states: starting, ready, healthy, degraded, stopped, failed,
  backoff, and crash-loop.
- Receive readiness only after role initialization.
- Implement versioned control commands for health, test-only message injection,
  controlled kill/restart, producer rotation, bridge disconnect/reconnect, and
  shutdown.
- Atomically rebuild producer/care channels and rotate generations/capabilities
  when either endpoint is replaced.
- Retain and evaluate active pidfd or equivalent generation state.
- Restart every required child under bounded policy.
- Prove signal shutdown and orphan cleanup.

### Workstream B — direct-care implementation and contract

- Replace custom MAC code with an exact reviewed RustCrypto `hmac` dependency
  and constant-time verification.
- MAC canonical bytes under a versioned domain separator.
- Remove secret capability material from the external schema; define actual
  authentication metadata.
- Keep capability delivery private and test descriptor, argv, environment, log,
  and filesystem non-exposure.
- Persist accepted and rejected receipts before responding.
- Preserve idempotency across care restart.
- Exercise same-user injection, malformed input, replay, stale generation/MAC,
  old channel, producer replacement, care replacement, companion absence, and
  care-store failure against the actual foundation.

### Workstream C — exact persistence and storage

- Make exact SQLite 3.53.4 source verification and compilation mandatory in
  acceptance builds and CI.
- Assert runtime version, source ID, compile options, migration checksums, and
  store identity.
- Use committed migrations as the sole migration source.
- Use bound parameters for all data values.
- Test companion, care, and vault stores for restart, incompatible migration,
  read-only/disk-full behavior, integrity, checkpoint, backup, corruption
  detection, and fresh restore equivalence.
- Keep broader VFS/power/lifetime qualification explicitly deferred.

### Workstream D — contracts and canonicalization

- Reconcile every schema, Rust type, fixture, and real wire message.
- Add positive and negative fixtures for all nine domains.
- Implement semantic schema/type drift detection.
- Enforce profile and digest identifiers, I-JSON-safe integer bounds, decoded
  duplicate rejection, and canonical authenticated content.

### Workstream E — Godot and health integration

- Use a real versioned UDS connection between Godot and `godot-bridge`.
- Implement current-screen selection, persisted output/position/size, clamping,
  topology polling, reconnect, and safe fallback.
- Report actual bridge and habitat state through supervisor health.
- Add headless injectable-topology tests and bounded target-host Openbox tests.

### Workstream F — bootstrap, CI, SBOM, and evidence

- Make clean-clone bootstrap fetch or verify exact official artifacts
  deterministically.
- Run exact SQLite and Godot checks in CI.
- Run unit, property, contract, integration, negative, recovery, and
  qualification-regression tests.
- Use current locked vulnerability and license tools with documented ceilings.
- Generate and validate a complete SPDX or CycloneDX document with exact
  versions, sources, checksums, licenses, and relationships.
- Upload sanitized integration, failure, artifact, and SBOM evidence.

### Workstream G — one real integration matrix and one real soak

- Drive one resident foundation through at least 3,000 actual messages across
  retained seeds and the full valid/invalid/restart/recovery category set.
- Run the complete Phase 01 failure/recovery matrix.
- Run one continuously resident 3,600-second target-host soak with the four
  required controlled failures and recoveries.
- Every harness must exit nonzero on an unmet assertion. No pass field may be a
  hard-coded conclusion.

## Acceptance criteria

Phase 01 passes only when:

1. Required processes are genuinely supervised and health reflects observed
   state.
2. Producer/care replacement rotates and revokes channel, generation, pidfd
   binding, and capability state.
3. The actual direct-care wire contract matches schemas and Rust types.
4. A reviewed HMAC implementation verifies canonical authenticated content.
5. Care receipts and idempotency survive restart and fail closed on store loss.
6. Exact SQLite 3.53.4 is used in local acceptance and CI with verified runtime
   identity.
7. Committed migrations, prepared statements, integrity, checkpoint, backup,
   and restore pass for all stores.
8. XDG and unsafe-storage gates remain fail closed.
9. All nine contracts pass semantic drift, positive, negative, and round-trip
   tests.
10. Godot establishes a real UDS bridge and passes target-screen, reconnect,
    geometry, and display-loss tests.
11. Health, logs, and socket census contain observed rather than asserted state.
12. Bootstrap, CI, vulnerabilities, licenses, SBOM, and provenance are
    reproducible and evidence-bound.
13. One resident foundation passes at least 3,000 real messages across the
    complete category matrix.
14. The complete Phase 01 failure/recovery matrix passes.
15. One continuously resident 60-minute target-host soak passes with controlled
    failures and recovery.
16. PR #7, Issue #6, Notion, CI artifacts, commits, and task records agree.
17. No Phase 02–10 capability or prohibited product claim is introduced.

## Explicitly deferred beyond Phase 01

- Broad SQLite VFS operation coverage beyond the bounded Phase 01 matrix.
- Realistic power-cut testing and lifetime database reliability.
- Production security certification and root/kernel/full-account threat claims.
- Production reliability, availability, endurance, and SLA claims.
- Organism, memory, learning, dreaming, production embodiment, media, speech,
  vision, biometrics, notifications, and qualified caregiving behavior.

## Publication rules

Continue `codex/p01-foundation-001` and PR #7. Merge current `origin/main`
normally. Do not rebase, force-push, replace the PR, merge PR #7, close Issue
#6, or modify the protected primary worktree.

Use coherent subsystem commits. Update the active packet, `.agent` current
state, the Phase 01 Notion directive and report, PR #7, and Issue #6. Re-fetch
all mutable records. Leave the PR and issue open for independent Architect
review.

## Required result

Return one complete `CODEX RESULT — COMPANION-P01-FOUNDATION-001` containing
exact commits, dependency rights, schema/implementation crosswalk, CI runs and
artifacts, actual category counts, failure matrix, exact SQLite runtime
identity, Godot UDS/display evidence, continuous-soak timestamps/resources and
injections, every non-pass, Notion publication, PR/Issue state, and explicit
confirmation that Phase 02 remains closed.
