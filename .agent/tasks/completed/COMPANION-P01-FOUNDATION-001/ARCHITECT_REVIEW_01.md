# Architect Review 01 — COMPANION-P01-FOUNDATION-001

## Verdict

`CONTINUE — PHASE 01 NOT ACCEPTED; COMPLETE THE ACTUAL RESIDENT FOUNDATION`

- Reviewed PR: `#7`
- Reviewed branch: `codex/p01-foundation-001`
- Reviewed head: `9d9e897d8fe6d74b0f4c3aedceab5761c55cc9be`
- Pull request state required after review: `OPEN / DRAFT / UNMERGED`
- GitHub Issue: `#6 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 02 and later: `CLOSED`
- Product capability: `NOT ESTABLISHED`
- Canonical Notion review: https://app.notion.com/p/3d7833cb27ff81b58987ca15fda7c0f1

## Review scope

The Architect independently inspected PR #7 metadata, all 79 changed paths, the successful GitHub Actions run, the Rust workspace and service implementation, IPC and persistence foundations, contracts and schema validation, XDG path policy, Godot habitat shell, operator health tooling, bootstrap and artifact checks, deterministic-cycle script, failure matrix, soak harness, SBOM/provenance files, the current Notion result, and GitHub Issue #6.

Current primary sources were rechecked for Linux file-descriptor inheritance and close-on-exec behavior, the XDG Base Directory defaults, Godot window/screen APIs, and SQLite prepared-statement parameter binding.

## Retained work

Preserve and build on the following rather than restarting:

1. Modular Rust workspace and locked Rust 1.98.1 baseline.
2. Nine authored Draft 2020-12 schema files and the bounded canonical-event direction.
3. Exact Godot 4.7.2 and SQLite 3.53.4 artifact identities.
4. Separate companion, care, and vault migration roots.
5. Initial XDG path-policy library.
6. Six executable role targets and a project-owned supervisor entry point.
7. Neutral Godot project shell and bounded visible-window observation.
8. Pinned checkout action and successful basic CI job.
9. Useful scripts, documentation boundaries, and protected primary-worktree handling.
10. The honest statement that the submitted soak was repeated one-shot execution rather than continuous residency.

These items are retained implementation progress. They do not satisfy the Phase 01 acceptance gate by themselves.

## Material acceptance failures

### 1. The supervisor is one-shot rather than resident

`ops-supervisor` starts child shells once, waits for them to exit, and exits. It has no resident control loop, process registry, readiness gate, active health collection, bounded restart/backoff, crash-loop handling, verified orphan cleanup, generation rotation after failure, or reconnect management.

The 60-minute script repeatedly starts this one-shot program. It does not exercise a continuously resident foundation.

### 2. The direct-care implementation violates descriptor and capability boundaries

The supervisor clears `FD_CLOEXEC` on both socket endpoints before spawning unrelated children. Non-close-on-exec descriptors survive `exec`, so unrelated children can inherit endpoints they are not authorized to own. Producer and care are also spawned while both endpoints are inheritable, so each may inherit the opposite endpoint.

The capability is a UUID placed in child environment variables and copied directly into the JSON message. This is not the accepted rotated HMAC-capability design, not a private capability-delivery channel, and not pidfd-bound authorization. The Phase 01 code contains no implemented pidfd check.

`care-core` keeps duplicate state only in memory, treats its store as optional, ignores store failures, and may report acceptance without a durable care-owned receipt. That violates fail-closed care authority.

### 3. The deterministic matrix does not exercise the foundation

`cycle_matrix.py` generates category labels and hashes them. It does not invoke Rust contracts, canonicalization, the resident supervisor, IPC, stores, migrations, recovery, or service processes. Its 3,000 cycles are deterministic data-generation observations, not integrated-system cycles.

### 4. The failure matrix is incomplete and fail-open

The matrix leaves companion-store failure, care outage, Godot reconnect, invalid contracts, restart/backoff, and most required scenarios `NOT_RUN`. It infers orphan cleanup from the absence of text in stdout. It can return success while its own result is partial.

### 5. Persistence is a CLI wrapper rather than the adopted exact library foundation

The Rust store launches a `sqlite3` subprocess for each operation and defaults to whichever executable is on `PATH`. It does not bind authoritative services to the exact SQLite 3.53.4 artifact. Migrations are duplicated as hard-coded SQL rather than executed from committed migration files. Values are interpolated into SQL text instead of using bound parameters. Backup destinations and errors are not governed strongly enough, and callers silently ignore store failures.

### 6. XDG and path enforcement are not specification-correct or fail-closed

Default configuration and cache paths are derived under `~/.local` instead of the XDG defaults `~/.config` and `~/.cache`. Missing `HOME` silently falls back to `/tmp`; missing runtime directory silently falls back beneath state. Target paths and parents are not robustly canonicalized against symlink traversal. Authority names are not constrained. Network-mount detection is prefix-based and fails open if mount metadata cannot be read.

### 7. Contracts and validation are incomplete

Only five of the nine schema domains have matching Rust types. The schema script validates one event instance only when an optional Python package happens to be installed; CI does not install or pin that validator, so most schema checks are structural. There is no schema/type drift gate or complete positive/negative fixture set for every contract.

### 8. Godot and health integration are static placeholders

The Godot shell has no real `godot-bridge` handshake, target-screen selection, output identity, screen-change handling, reconnect, position restoration, or display-loss fallback. The visible probe checks only that a titled window exists.

The health command scans process names and hard-codes network-deny and degradation statements. It does not query the supervisor, children, stores, channel, or Godot bridge. Logging uses wall-clock nanoseconds as a per-process boot identifier and hard-coded sequence values rather than the adopted boot/monotonic/sequence model.

### 9. CI, SBOM, bootstrap, and evidence are incomplete

CI does not run the release build, exact artifact verification, direct-care implementation tests, storage/failure tests, Godot headless validation, the accepted qualification-result validator, vulnerability/license checks, or SBOM generation.

The committed SBOM has no packages and a placeholder timestamp. Its generator records names without exact versions, checksums, or licenses. Bootstrap assumes the earlier private qualification cache and a random Godot unpack-directory name. SQLite verification checks a version substring instead of exact source identity. The committed result summary is not bound to the final head and overstates incomplete areas.

## Architect disposition

This is a substantial implementation candidate, but it does not satisfy the adopted Phase 01 acceptance contract. Phase 01 remains active. PR #7 must remain open, return to draft state, and receive one phase-completion continuation—not a series of micro-directives.

# CODEX CONTINUATION DIRECTIVE

## Objective

Complete the actual resident Roadmap Phase 01 foundation in the existing PR. Preserve useful code, but replace every fake, one-shot, fail-open, or self-asserting substitute with an executable foundation and evidence that directly exercises it.

Do not return after internal checkpoints while the complete correction remains feasible.

## Required workstream 1 — resident supervisor

Implement a long-running `ops-supervisor` with:

- explicit child registry and dependency graph;
- readiness protocol with startup deadlines;
- continuously queryable health state;
- bounded restart, justified backoff, and crash-loop state;
- generation and capability rotation on producer replacement;
- clean shutdown, signal handling, orphan cleanup, and stale-channel revocation;
- optional-component degradation without false healthy status;
- stable supervisor control socket for health and test control;
- one-shot test mode only as a separate explicit mode.

Split role-specific code into reviewable modules or binaries and remove the shared-target warning.

## Required workstream 2 — correct direct-care boundary

Keep all descriptors close-on-exec by default. Pass exactly one intended endpoint to each authorized child through an explicit descriptor-mapping step and close all unrelated descriptors before `exec`. Prove through `/proc` or equivalent observation that unrelated children, producer, and care do not receive opposite or unrelated endpoints.

Do not expose capability material through argv, environment, logs, files, or repository state. Use a private inherited channel, sealed memory object, or another reviewed least-exposure mechanism. Implement an actual MAC/capability check, pidfd or equivalent race-resistant live-generation binding, kernel-credential validation, replay protection, and restart revocation.

Persist accepted and rejected care receipts and idempotency state in the care store before reporting durable acceptance. Store failure must produce explicit degraded or failed coverage, never silent acceptance. The care path must remain usable with `companion-core` and its store absent, but not with its own receipt authority unavailable.

Move the accepted same-user attack and lifecycle matrix from disposable qualification into tests of the actual foundation implementation.

## Required workstream 3 — exact persistence implementation

Replace subprocess-per-operation SQLite use with one reviewed Rust binding or minimal FFI compiled against the exact SQLite 3.53.4 source identity. A build-only helper is permitted when necessary and must be locked, licensed, and documented.

Use prepared statements and bound parameters. Execute versioned migrations from committed migration files with checksums, compatibility preflight, transactional application, and recorded schema identity. Enforce one process writer per authority store. Implement integrity, explicit checkpoint, backup, fresh-directory restore, and fail-closed error propagation.

Test companion, care, and vault stores independently, including restart, incompatible migration, disk-full/read-only behavior, and restore equivalence.

## Required workstream 4 — XDG and filesystem correctness

Implement the XDG defaults exactly:

- data: `$XDG_DATA_HOME` or `$HOME/.local/share`;
- config: `$XDG_CONFIG_HOME` or `$HOME/.config`;
- state: `$XDG_STATE_HOME` or `$HOME/.local/state`;
- cache: `$XDG_CACHE_HOME` or `$HOME/.cache`;
- runtime sockets: a valid private `$XDG_RUNTIME_DIR`, except explicit isolated test overrides.

Missing required bases must fail visibly. Do not silently use `/tmp` for canonical state. Canonicalize existing parents, reject symlink and traversal escapes, constrain authority identifiers, verify mount type, permissions, and ownership, and fail closed when safe placement cannot be established.

Add positive and negative tests for checkout, SSHFS/network, symlink, relative, missing-runtime, and unsafe-permission cases.

## Required workstream 5 — complete contract system

Provide matching Rust types and serialization tests for every Phase 01 schema. Pin and run a real Draft 2020-12 validator in CI. Add positive and negative fixtures for each contract, including unknown fields, missing fields, bounds, invalid UUID/time, unsupported schema major, duplicate decoded keys, malformed framing, and canonical-profile violations.

Add a deterministic schema/type compatibility gate and golden canonical bytes/digests. Enforce project numeric bounds and explicit profile/digest-version semantics.

## Required workstream 6 — real Godot bridge and habitat recovery

Implement a real versioned local handshake between Godot and `godot-bridge`. The UI must reflect actual bridge state rather than a static string.

Implement configurable target-screen selection for the dedicated 1366×768 Openbox-managed output, saved screen/position/size, minimum and maximum geometry, visible-area clamping, content scaling, reconnect, and safe fallback when the target display is absent or changes.

Add a deterministic injectable display-topology abstraction for headless tests and a bounded target-host Openbox test. Do not capture media or add production sprites.

## Required workstream 7 — live health, logging, and no-network evidence

Use the OS boot identifier or an explicitly versioned boot epoch plus monotonic time, UTC observation/uncertainty, and monotonically increasing process/authority sequences. Do not fabricate health from process-name scans.

Implement a supervisor-backed health command that reports child readiness, restarts, crash-loop state, store integrity, direct-care coverage, channel generation, Godot connection, and known degradation. Logs must fail visibly when serialization/output fails and must exclude secrets and unrestricted payloads.

Demonstrate that resident foundation processes open no AF_INET/AF_INET6 sockets by default using a runtime FD/socket census or an equivalent nonprivileged observation. This is engineering evidence, not a security certification.

## Required workstream 8 — clean-clone bootstrap, CI, SBOM, and provenance

Create deterministic cache paths and an idempotent artifact bootstrap that can retrieve or validate the official Godot archive and exact SQLite source/build without relying on a random prior unpack path. Preserve the existing Godot 4.6 installation.

CI must run:

- locked debug and release builds;
- format, clippy, unit, property, contract, integration, negative, and recovery tests;
- real Draft 2020-12 validation and canonical vectors;
- actual foundation direct-care and persistence tests;
- the accepted Phase 00 qualification-result validator;
- Godot exact-artifact verification and headless project validation;
- secret and forbidden-runtime-data scans;
- vulnerability and license checks;
- generation and validation of a complete SBOM with exact package versions, sources, checksums, and declared/concluded licenses;
- concise sanitized evidence artifacts.

Use immutable action revisions. Document every dependency and right separately.

## Required workstream 9 — real integration and recovery evidence

Replace the synthetic category counter with a driver that exercises a resident foundation instance through at least 3,000 actual messages across retained seeds. Cover valid, duplicate, replayed, malformed, unsupported, stale-generation, stale-capability, restart, persistence, and recovery cases and verify exact expected outcomes.

Execute the full failure matrix:

- kill and restart every shell;
- restart/backoff/crash-loop behavior;
- companion absent and corrupt-store cases while care remains independently visible;
- care failure and explicit degraded coverage;
- vault failure and denied protected operations;
- producer replacement and capability rotation;
- stale channel and stale capability rejection;
- Godot absent, disconnect, reconnect, and simulated display loss;
- invalid contracts and framing;
- unsafe storage refusal;
- migration failure;
- backup and fresh-directory restore;
- orphan cleanup.

Run one continuously resident 60-minute target-host soak. During the same supervisor lifetime, sample CPU/RSS, process health, restart counts, store integrity/checkpoint state, channel generation, Godot bridge/window status, log volume, runtime socket census, no-network evidence, and no-checkout-write evidence. Inject at least one controlled companion failure, one producer replacement, one Godot disconnect/reconnect, and one care outage/recovery.

The previous repeated-invocation soak remains historical evidence only.

## Acceptance criteria

Phase 01 is accepted only when:

1. One supervisor stays resident and demonstrably supervises all shells.
2. Restart/backoff, crash-loop, signal shutdown, orphan cleanup, and health query work.
3. Descriptor and capability ownership match Architecture v1.0 in the real process graph.
4. The care path authenticates the producer through the selected process/capability design and persists receipts before durable acceptance.
5. Care remains independent of companion, while care-store failure fails visibly.
6. Exact SQLite 3.53.4 is linked or compiled into the Rust persistence implementation, not selected by `PATH`.
7. Committed migrations, prepared statements, integrity, checkpoint, backup, and restore paths pass.
8. XDG defaults and unsafe-path refusals are specification-correct and fail closed.
9. All nine contracts have matching Rust types, real schema validation, fixtures, and drift tests.
10. Godot performs a real bridge handshake, target-screen selection, geometry restoration, reconnect, and safe display fallback.
11. Health and logs reflect observed runtime state and the adopted event/time profile.
12. CI covers release, integration, recovery, Godot, qualification validator, licenses, vulnerabilities, SBOM, and scans.
13. At least 3,000 real resident-system cycles pass across retained seeds.
14. The full failure/recovery matrix passes or returns one precise stop-condition blocker.
15. A continuously resident 60-minute target-host soak passes with injected failures and recorded resources.
16. A clean clone can bootstrap and reproduce the phase without undocumented prior cache layout.
17. Notion, PR #7, Issue #6, commits, CI, and sanitized evidence agree.
18. No Phase 02–10 capability or prohibited claim is introduced.

## Publication rules

Continue on `codex/p01-foundation-001` and the existing PR #7. Merge current `origin/main` normally after this review is published. Do not rebase, force-push, create a replacement PR, merge PR #7, close Issue #6, or modify protected primary-worktree files.

Use several coherent commits grouped by major subsystem. Do not return after each commit. Publish one final reconciled result after the complete phase passes or a genuine stop condition is proven.

## Prohibited scope and claims

Do not implement or claim real organism drives, memory, learning, dreaming, production sprite embodiment, camera/microphone capture, STT/TTS, models, biometrics, real contacts, notification delivery, spoken-help recognition, live escalation, medical capability, security certification, production reliability, or SLA performance.

## Required result

Return one complete `CODEX RESULT — COMPANION-P01-FOUNDATION-001` containing exact commits, changed paths, dependency rights, commands, CI runs, real integration counts, full failure matrix, resident-soak resources and injected events, remaining failures, Notion publication, PR/Issue state, and explicit confirmation that Phase 02 remains closed pending Architect acceptance.
