# CODEX DIRECTIVE — COMPANION-P01-FOUNDATION-001

## Objective

Complete Roadmap Phase 01 — Environment and Engineering Foundation — in one coherent implementation run.

Convert the governance/planning repository into a reproducible, executable, observable local foundation on the existing Linux PC. The result must build, boot, supervise isolated service shells, enforce canonical contracts and safe local storage, exercise an independent synthetic direct-care path, open the approved bounded Godot habitat shell, persist isolated synthetic development state, fail visibly, and produce CI/provenance evidence.

This is a phase-sized directive. Do not stop at an internal checkpoint while the complete phase remains feasible.

## Why this is next

Roadmap Phase 00 has closed its implementation-opening gate. The project has an accepted end goal, roadmap, operator product boundaries, Linux environment evidence, adopted Architecture v1.0, accepted foundation qualification, approved mon identity and Architect technology dispositions. No executable product foundation exists yet; that is the current bottleneck.

## Authoritative basis

Codex cannot see the operator–Architect conversation. Fetch and read the full live content of:

- Canonical project: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- Complete operational end goal: https://app.notion.com/p/3d5833cb27ff81b09c20e2b52d537e1e
- Master roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Governance contract: https://app.notion.com/p/3d5833cb27ff81e2b3b2eabc70f9f6b3
- Adopted Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Qualification acceptance: https://app.notion.com/p/3d6833cb27ff819fabc2e5c9cb443aae
- Approved mon design: https://app.notion.com/p/3d5833cb27ff8108a3acf202fc268b6d
- Sprite production contract: https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Open decisions: https://app.notion.com/p/3d5833cb27ff81118ac8e4139ce1c873
- Initial risk register: https://app.notion.com/p/3d5833cb27ff817698eed33e1ffcc779
- Architecture Decision Ledger, especially ADR-38 through the live maximum
- Research Evidence Register, especially Rust, Godot, SQLite, RFC 8785, Linux IPC, XDG and systemd records
- This directive: https://app.notion.com/p/3d7833cb27ff815ebe3ed1999f05beba
- Required report: https://app.notion.com/p/3d7833cb27ff81c5b0eee3e6c98b54b5
- GitHub Issue #6: https://github.com/SketchOTP/companion/issues/6
- Merged PR #5 and closed Issue #4
- Complete archived packets under `.agent/tasks/completed/`

Read repository authority in this order:

1. root and nested `AGENTS.md`;
2. `.agents/skills/authority/SKILL.md`;
3. `.agent/PROJECT_GOAL.md`;
4. `.agent/PROJECT_PROFILE.md`;
5. `.agent/CURRENT.md`;
6. `.agent/INDEX.md`;
7. `.agent/ARCHITECTURE_V1.md`;
8. every file in `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/`.

Complete `AUTHORITY_CONTEXT_ACKNOWLEDGMENT.md` before implementation. Stop if retrieval confidence is below `ADEQUATE` or authority conflicts materially.

## Protected operator work

The primary SSHFS worktree contains operator-owned uncommitted changes to root `.gitignore` and `AGENTS.md`.

Do not read their modified contents into evidence, commit, discard, reset, overwrite, stash, reformat or otherwise alter them.

Create a clean secondary worktree on local ext4/NVMe from current `origin/main` and branch:

```text
codex/p01-foundation-001
```

Do not execute builds, stores, sockets, Godot or soak tests from the SSHFS checkout.

## Adopted technology direction

The Architect authorizes this Phase 01 development baseline:

- Authoritative local services: Rust 1.98.1.
- Python: qualification tooling and future nonauthoritative model/perception adapters only.
- Godot: exact official 4.7.2 Linux x86_64 artifact with accepted SHA-256 `cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4`.
- Persistence: exact SQLite 3.53.4 source identity for separate single-writer development stores on local ext4/NVMe, WAL, synchronous FULL and explicit checkpoint/migration policy. Release eligibility remains conditional.
- Direct-care IPC: supervisor-created private `AF_UNIX` `SOCK_SEQPACKET` channel, kernel credentials, pidfd/generation binding, rotated capability material, idempotency and care-owned receipts within the documented threat ceiling.
- Supervision: project-owned Rust `ops-supervisor`; systemd-user may be an optional non-installed outer launcher.
- Canonical event profile: JSON Schema Draft 2020-12 plus `JCS-RFC8785-v1` / `sha-256-jcs-event-v1`, bounded to authoritative integers, fixed-point integers and canonical strings.
- Storage: XDG-aligned local configuration, data, state, cache, logs, secrets, backups, exports and runtime sockets; canonical state may not live in the repository or on SSHFS.
- Network: no outbound runtime network by default.

## Approved dependency envelope

Codex may select exact locked patch versions from these narrow families when necessary, after current official source, license, maintenance, telemetry, security and transitive-dependency review:

- `serde`, `serde_json`; optional `schemars` or equivalent maintained schema generator;
- `sha2`, `hmac`;
- standard library plus one of `rustix`, `nix`, or narrowly scoped `libc` usage;
- `thiserror`, `tracing`, `tracing-subscriber`;
- one reviewed Rust binding to the exact SQLite 3.53.4 build, or a minimal direct FFI wrapper when stronger artifact identity justifies it;
- `uuid`, `time`, `tempfile`, `proptest` or equivalent deterministic test tooling;
- isolated Cargo audit/license/SBOM tooling and SPDX or CycloneDX generators;
- GitHub Actions pinned by immutable commit SHA.

Any runtime dependency outside this envelope requires a targeted stop-and-return Architect question. No speech, vision, biometric, LLM, TTS, voice, notification, analytics, telemetry or cloud dependency is authorized.

## Scope

### 1. Repository and reproducible toolchain

Create a modular layout separating:

- Rust authoritative services and shared libraries;
- Godot embodiment shell;
- contracts and fixtures;
- database migrations;
- bootstrap/build tooling;
- tests and deterministic simulations;
- documentation and generated evidence;
- source assets and generated runtime outputs.

Pin Rust 1.98.1. Commit Cargo locks and required checksums/manifests. Provide an idempotent bootstrap/verify workflow that uses repository-local metadata and private XDG caches without modifying system packages, shell profiles or Godot 4.6.

### 2. Canonical contracts

Implement versioned JSON Schema Draft 2020-12 contracts and matching Rust types for:

- canonical event envelope and digest profile;
- process lifecycle/readiness;
- health and degraded state;
- ordinary observation envelope;
- safety-candidate envelope;
- care receipt result;
- body-neutral embodiment intent/result;
- consent/vault decision stub;
- backup/export manifest shell.

Reject duplicate decoded keys, invalid Unicode, unsupported schema majors, noncanonical numbers and unknown authoritative variants where required. Preserve extension fields only where explicitly allowed. Maintain golden vectors, oracle comparison and negative tests.

### 3. XDG and filesystem boundary

Implement one shared path-policy library for configuration, durable data, mutable state, cache, logs, runtime sockets, backups, exports and secrets.

It must:

- resolve local XDG paths;
- create private directories with appropriate permissions;
- refuse canonical state, SQLite/WAL, locks, runtime sockets or backup staging under the repository or on detected SSHFS/network filesystems;
- support isolated test overrides;
- report an explicit fatal or degraded state instead of silently falling back.

### 4. Authoritative service shells

Implement Rust executables for:

- `ops-supervisor`;
- `companion-core`;
- `care-core`;
- `identity-consent-vault`;
- `sensor-gateway`;
- `godot-bridge`.

These are engineering shells, not finished product logic. Each exposes exact version/build identity, readiness, health, degraded state, payload-minimized structured logs, bounded shutdown and deterministic test controls. Every mutable authority has exactly one writer.

Do not implement real mon personality, needs, drives, memory, biometric enrollment, sensor capture, spoken-help recognition, notification delivery or escalation.

### 5. Supervisor and process boundaries

Implement `ops-supervisor` to:

- establish local runtime directories and private channels;
- start services in dependency order;
- provision/revoke producer generations and capabilities;
- aggregate health without owning child canonical state;
- enforce bounded restart/backoff and expose crash loops;
- perform clean shutdown and orphan cleanup;
- report missing/degraded optional components honestly;
- keep `care-core` startup and direct synthetic safety ingress independent of `companion-core` and its store.

Commit non-installed systemd-user unit templates if useful. Validate syntax and reversible transient behavior only; do not install persistent units or enable lingering.

### 6. Direct synthetic care path

Implement:

```text
synthetic authorized producer
├── ordinary synthetic observation → companion-core
└── synthetic safety candidate → care-core directly
```

`care-core` owns its synthetic receipt journal and test incident state. `companion-core`, Godot, model stubs, mood, memory, language and animation messages cannot create, suppress or authorize care transitions.

Test valid, duplicate, replay, malformed, unsupported version, stale generation, stale capability, producer restart, care restart, companion absence, companion-store corruption, same-user unauthorized client, descriptor inheritance and producer outage/degraded coverage.

This is a transport/policy-shell foundation only, not spoken-help detection or safety efficacy.

### 7. Isolated persistence foundation

Create separate development stores for companion, care and vault authority with one writer per store and versioned migrations.

Include:

- store identity/schema version;
- append-only event/audit records;
- health and migration metadata;
- crash-safe transaction wrappers;
- integrity checks;
- explicit WAL/checkpoint policy;
- Backup API snapshot and fresh-directory restore;
- synthetic test records only.

No real user, biometric, contact, organism, memory or safety data.

### 8. Godot 4.7.2 habitat shell

Create the first Godot 4.7.2 project shell for the approved bounded resizable habitat on the dedicated 1366×768 Openbox-managed output.

Implement:

- configurable screen/output selection;
- bounded resizable window and content-scaling policy;
- safe geometry persistence outside the repository;
- fallback to a visible safe window when the target output is missing or changes;
- IPC handshake with `godot-bridge`;
- visible foundation health/degraded status;
- neutral non-production placeholder only;
- headless smoke-test mode.

Do not generate or import the production sprite library. Do not implement camera, microphone, TTS, STT, model or notification behavior.

### 9. Logging, health and operator workflow

Implement payload-minimized structured logs with process/version/build identity, `boot_id`, sequence, correlation/causation, severity, privacy class, readiness, health, restart and degradation reasons. Never log secrets, capabilities, raw user data or unrestricted payloads.

Provide an operator health command summarizing each process, store, channel, Godot connection and known degraded capability without claiming normal coverage when evidence is missing.

Provide concise documented commands for bootstrap, verify, build, test, start, health, synthetic ordinary input, synthetic safety input, stop, backup, restore, Godot headless test, Openbox window test and soak.

### 10. CI, security and provenance

Add CI that:

- builds locked Rust code;
- runs formatting, linting, unit, property, contract, integration and negative tests;
- validates schemas and canonical golden vectors;
- runs the accepted qualification-result validator;
- validates the Godot project headlessly using the exact artifact;
- generates dependency/license and SBOM evidence;
- scans for secrets and forbidden runtime data;
- uses actions pinned to immutable SHAs;
- retains sanitized evidence artifacts.

Runtime network remains default-deny. CI network is limited to locked dependency/artifact retrieval.

### 11. Phase-level integration and soak

Run and retain:

- at least 1,000 deterministic contract/message cycles across multiple retained seeds;
- at least 60 minutes of supervised foundation operation on the target host;
- clean start/stop and repeated restart cycles;
- kill/restart for every service shell;
- companion absence and corrupt-store cases while care transport remains visible;
- care failure and explicit degraded coverage;
- Godot absent/disconnected/reconnected;
- safe target-display unavailable/change simulation where possible;
- invalid schema, malformed frame, duplicate, stale generation/capability cases;
- migrations, integrity, backup and restore;
- no-network/default-deny checks;
- proof that no canonical writes occur beneath the checkout.

These are engineering evidence floors, not reliability or safety statistics.

## Do not change

- Complete end goal.
- Architecture v1.0 ownership and independent care path.
- One primary adult user, no minors in iteration one.
- Kentucky and narrow nonmedical claim boundary.
- Approved purple mon identity and `MON_FRAME_V1`.
- Godot as a nonauthoritative embodiment adapter.
- Local-first continuity and no-default-network policy.
- Safe bounded defaults for unresolved RQ-04 and RQ-07 through RQ-12.

## Required external discovery

Before locking exact crate/action/artifact versions, recheck current official Rust, Godot, SQLite, Cargo/crates.io, systemd, GitHub Actions, JSON Schema, SPDX/CycloneDX and component-maintainer sources. Record version/date, source identity, integrity, license, maintenance, telemetry/network behavior, limitations and recheck trigger.

Do not use popularity, stars, benchmark marketing or an umbrella license as the sole basis.

## Acceptance criteria

Phase 01 passes only when:

1. A clean clone can bootstrap, verify exact artifacts, build and test without system-level modification.
2. A modular Rust workspace and Godot 4.7.2 shell exist and are documented.
3. All foundation contracts have schemas, Rust types, golden vectors and negative tests.
4. Canonical bytes and digests are deterministic under the adopted profile.
5. XDG policy prevents canonical state under the checkout or on SSHFS.
6. All six process shells start, report readiness/health, shut down and fail visibly.
7. The supervisor enforces dependency order, bounded restart/backoff and capability rotation.
8. Direct synthetic care ingress works without `companion-core` or its store; same-user unauthorized injection remains blocked within the adopted threat ceiling.
9. Companion, care and vault stores are separate, single-writer, migratable, integrity-checked and restorable.
10. The bounded Godot shell opens on the selected Openbox output, reconnects to `godot-bridge`, persists geometry safely and recovers visibly from display loss.
11. CI passes approved checks and emits SBOM/license/provenance artifacts.
12. The 1,000-cycle matrix and 60-minute target-host soak pass without silent data loss, unbounded restart loops, repository-state writes or unintended outbound network.
13. Negative, blocked and unqualified surfaces are preserved.
14. Notion, GitHub issue, pull request, commits and evidence agree.
15. No Phase 02–10 capability is claimed or smuggled into the foundation.

## Required validation

At minimum:

- locked debug and release builds;
- `cargo fmt --check`;
- `cargo clippy --all-targets --all-features -- -D warnings`;
- full Rust tests and property tests with retained seeds;
- schema and canonical-vector validation;
- process and IPC integration/negative tests;
- unauthorized same-user tests;
- migrations, integrity, backup and restore tests;
- Godot 4.7.2 headless validation and bounded-window target-host test;
- CI from a clean checkout;
- SBOM/license/provenance verification;
- secret/private-data and forbidden-path scans;
- no-default-network verification;
- 1,000-cycle deterministic run;
- 60-minute target-host soak;
- complete diff and generated-file review.

## Prohibited claims and work

Do not claim or implement:

- a living mon;
- organism autonomy, real needs/drives/goals or long-term memory;
- learning or dreaming;
- production sprite embodiment;
- speech, vision, identity recognition or sensor capture;
- spoken-help recognition, notification delivery or emergency escalation;
- real biometrics, contacts or user data;
- cloud model behavior;
- security certification, production reliability, SLA, medical capability or safety efficacy;
- Phase 02 or later completion.

Do not use root/sudo, install system packages, modify drivers/displays/audio/services/power policy, alter Godot 4.6, enable persistent services/lingering, or modify protected primary-worktree changes.

## Stop and return to Architect if

- mandatory authority conflicts materially;
- protected work cannot remain untouched;
- an exact required artifact cannot be verified;
- a dependency outside the approved envelope is required;
- Openbox testing would modify unrelated displays or expose private desktop content;
- direct care isolation cannot be preserved;
- canonical state requires SSHFS/network storage;
- Architecture v1.0 ownership would need to change;
- real media, biometrics, contacts, notifications, cloud models, root privileges, permanent host changes or later-phase behavior would be required.

Return one precise blocker with evidence. Do not return a broad avoidable question list.

## Required project updates

- Work on `codex/p01-foundation-001` in a clean local secondary worktree.
- Use logical internal-checkpoint commits, not commit spam.
- Open one pull request to `main`; do not merge it.
- Maintain `.agent` routing and append-only records.
- Complete every task-packet artifact.
- Publish the complete result to the required Notion report.
- Update Issue #6 and leave it open.
- Preserve negative and partial outcomes.

## Required handoff

Return:

```text
# CODEX RESULT — COMPANION-P01-FOUNDATION-001

## Verdict
## Retrieval confidence
## Protected-work verification
## Baseline / branch / worktree / PR state
## Repository and toolchain foundation
## Dependencies and rights
## Contracts and canonicalization
## XDG and storage enforcement
## Service shells and supervisor
## Direct-care IPC
## Persistence
## Godot habitat
## Health and observability
## CI / SBOM / provenance
## 1,000-cycle matrix
## 60-minute soak
## Failure and recovery matrix
## Tests and commands
## Evidence levels and ceilings
## Files changed
## Assumptions confirmed/disproven
## Failures and blockers
## Notion and GitHub publication
## Recommendation to Architect
```

Include exact baseline, branch, commits, PR, test commands, retained seeds, timings, resource observations, dependency identities/licenses, changed paths, issue/report state and explicit confirmation that no Phase 02–10 product capability or safety claim is established.

Complete the whole phase while feasible. Stop only for a directive stop condition.
