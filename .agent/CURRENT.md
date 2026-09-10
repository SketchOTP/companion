# Current Project State

## Current stage

Planning Phase 02 remains the governing delivery roadmap.

Roadmap Phase 00 is complete at the implementation-opening boundary. Architecture v1.0 remains adopted. Roadmap Phase 01 — Environment and Engineering Foundation is active but **not accepted**.

PR #7 at `9d9e897d8fe6d74b0f4c3aedceab5761c55cc9be` received Architect Review 01 and must continue in the existing phase-sized branch and pull request.

## Active objective

Complete the actual resident Roadmap Phase 01 foundation. Retain useful source, but replace every one-shot, fail-open, self-asserting, or incomplete substitute with directly exercised implementation and evidence.

The current critical path is:

1. a continuously resident Rust `ops-supervisor` with readiness, health, restart/backoff, crash-loop, signal, and orphan handling;
2. exact descriptor and capability isolation for the direct-care process graph, with persisted care receipts and idempotency;
3. an exact SQLite 3.53.4 Rust binding or FFI layer using committed migrations and prepared statements;
4. specification-correct, fail-closed XDG and filesystem placement;
5. complete Rust types, real Draft 2020-12 validation, fixtures, canonical vectors, and schema/type drift checks for all Phase 01 contracts;
6. a real Godot-to-bridge handshake, selected-screen placement, geometry restoration, reconnect, and display-loss fallback;
7. supervisor-backed health, correct boot/monotonic/sequence logging, and observed no-network evidence;
8. reproducible artifact bootstrap, complete CI, vulnerability/license checks, SBOM, and provenance;
9. at least 3,000 actual resident-system message cycles, the full failure/recovery matrix, and one continuously resident 60-minute target-host soak with controlled failures.

## Active directive and review

- Directive: `COMPANION-P01-FOUNDATION-001`
- Status: `ARCHITECT REVIEW 01 — CONTINUE; PHASE 01 NOT ACCEPTED`
- Original Phase 01 routing baseline: `4171a02385b67f3e8d7ecbd6349d45c0bf1e0a8e`
- Reviewed candidate head: `9d9e897d8fe6d74b0f4c3aedceab5761c55cc9be`
- Repository review: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/ARCHITECT_REVIEW_01.md`
- Notion review: https://app.notion.com/p/3d7833cb27ff81b58987ca15fda7c0f1
- Notion directive: https://app.notion.com/p/3d7833cb27ff815ebe3ed1999f05beba
- Required Notion report: https://app.notion.com/p/3d7833cb27ff81c5b0eee3e6c98b54b5
- GitHub Issue #6: https://github.com/SketchOTP/companion/issues/6
- Pull request #7: https://github.com/SketchOTP/companion/pull/7
- Active packet: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/`
- Required branch: `codex/p01-foundation-001`
- Required publication: continue existing draft/unmerged PR #7
- Acceptance authority: ChatGPT AI Architect
- Roadmap Phase 02 and later: `CLOSED`
- Product capability claims: `PROHIBITED`

## Useful work retained

The current PR retains a modular Rust workspace, exact Rust/Godot/SQLite identities, initial schemas and canonicalization, migration roots, XDG guard, six role targets, a supervisor entry point, a neutral Godot project, basic CI, scripts, documentation, and a bounded window observation.

These are implementation assets, not accepted Phase 01 capability.

## Material defects requiring completion

- `ops-supervisor` is one-shot rather than resident.
- Socket endpoints are made inheritable too broadly; unrelated children may receive unauthorized descriptors.
- Capability material is placed in the environment and compared as a plain string; pidfd binding is not implemented.
- Care idempotency is memory-only and store errors are ignored.
- The 3,000-cycle script does not exercise the running foundation.
- Most required failure/recovery scenarios remain `NOT_RUN`.
- Persistence shells out to whichever `sqlite3` is selected rather than binding exact SQLite 3.53.4.
- Committed migrations are not the migrations executed by the Rust store.
- XDG defaults and fail-closed placement are incomplete.
- Four schema domains lack matching Rust types; CI schema validation is mostly structural.
- Godot has no real bridge handshake, target-screen selection, reconnect, or display-loss recovery.
- Health is inferred from process-name scanning rather than queried runtime state.
- CI, SBOM, artifact bootstrap, license/vulnerability, and evidence coverage are incomplete.
- The submitted 60-minute run is repeated one-shot invocation rather than one resident runtime.

## Mandatory Codex continuation startup

Codex cannot see the operator–Architect conversation. Do not infer hidden decisions.

1. Inspect the protected primary SSHFS worktree read-only; do not read the modified contents of root `.gitignore` or `AGENTS.md` into evidence.
2. Fetch current `origin/main` and `origin/codex/p01-foundation-001`.
3. Continue only in the existing clean local-ext4/NVMe secondary worktree.
4. Merge current `origin/main` normally into `codex/p01-foundation-001`; do not rebase, reset, or force-push.
5. Read `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/ARCHITECT_REVIEW_01.md` in full.
6. Fetch the live Notion review, directive, report, canonical project, roadmap, Architecture v1.0, PR #7, and Issue #6 with all comments.
7. Preserve accepted Phase 00 evidence and useful Phase 01 source. Do not restart the repository or repeat unaffected work.
8. Complete all required workstreams in the same phase-sized PR. Use coherent subsystem commits, but do not return after internal checkpoints while the full phase remains feasible.
9. Update Notion, PR #7, Issue #6, the task packet, and Authority state; leave PR and issue open; stop for independent review.

## Adopted Phase 01 technology direction

- Authoritative service foundations: Rust 1.98.1.
- Python: qualification tooling and future nonauthoritative model/perception adapters only.
- Embodiment engine: exact official Godot 4.7.2 Linux x86_64 artifact.
- Persistence: exact SQLite 3.53.4 for separate single-writer local development stores; release qualification remains conditional.
- Direct-care transport: supervisor-created private `AF_UNIX` `SOCK_SEQPACKET`, kernel credentials, pidfd/generation binding, rotated capability material, and care-owned receipts under the documented threat ceiling.
- Supervision: project-owned Rust `ops-supervisor`; systemd-user may be an optional non-installed outer launcher.
- Canonical event profile: `JCS-RFC8785-v1` / `sha-256-jcs-event-v1`, bounded to authoritative integer/fixed-point/string values.
- Storage: local XDG paths on ext4/NVMe; no canonical database, WAL, lock, runtime socket, or backup staging in the SSHFS checkout.

## Protected operator work

The primary SSHFS worktree has operator-owned uncommitted changes to root `.gitignore` and `AGENTS.md`. Codex must not read their modified contents into evidence, commit, discard, reset, overwrite, stash, reformat, or otherwise alter them.

## Foundation boundary

Phase 01 may implement engineering foundations and synthetic process/store/IPC behavior only. It may not implement or claim real mon personality, needs, drives, goals, autonomy, long-term memory, learning, dreaming, production sprites, camera/microphone capture, STT/TTS, model inference, biometrics, real user/contact data, notification delivery, spoken-help recognition, live care escalation, medical capability, security certification, production reliability, or SLA performance.

## Next review point

Codex completes the full resident Phase 01 foundation in PR #7, runs the real integration and failure matrices and continuous soak, publishes a reconciled Notion/GitHub result, leaves PR #7 and Issue #6 open, and stops for independent Architect review.

## Review 01 continuation update — 2026-09-10

The continuation replaces the one-shot service entry point with a resident
`ops-supervisor` and explicit `--once` test mode, separate role binaries,
supervisor-backed health, direct SQLite ABI calls with prepared statements and
the Online Backup API, corrected XDG defaults with fail-closed placement, and
private capability delivery for the real direct-care socket. Three retained
seeds now drive 3,000 actual packet cycles through separate processes. The
remaining full failure/recovery injection, target-host Godot recovery, exact
3.53.4 host-library binding verification, and completed continuous 60-minute
injected soak remain tracked as unqualified until independently observed.

## Review 01 continuation recheck — 2026-09-10

The private exact SQLite 3.53.4 amalgamation build path is now exercised when
`COMPANION_SQLITE_SOURCE` is present; the resulting release binary statically
exposes SQLite 3.53.4 and has no SQLite dynamic dependency. The verification
script also starts a resident supervisor before querying the operator health
command, so the health result reflects live child state. The bounded verify
run completed successfully. Full injected one-hour soak, broad restart and
display-loss recovery, adversarial IPC, and VFS/power-loss coverage remain
unrun and continue to block phase acceptance.

## Publication re-fetch — 2026-09-10

The live Architecture Decision Ledger currently has 52 rows (31 Adopted,
19 Interim, 2 Rejected); the live Research Evidence Register has 55 rows
(42 Grade A, 11 Grade B, 2 Grade C, 0 Grade D). The branch and PR remain
unaccepted pending the explicitly unrun long soak and recovery matrices.
