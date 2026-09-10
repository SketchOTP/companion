# Architecture v1.0 — Adopted Local Runtime and Authority Model

Status: `ADOPTED — PHASE 01 IMPLEMENTATION BASELINE ACTIVE`

Canonical Notion: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556

Architecture acceptance: https://app.notion.com/p/3d6833cb27ff81d88785f64d0629286c

Foundation qualification acceptance: https://app.notion.com/p/3d6833cb27ff819fabc2e5c9cb443aae

This file is a repository routing mirror. Live Notion remains authoritative for project meaning and decisions.

## Adopted topology

- `companion-core` is the sole ordinary creature-truth owner: identity/epoch, organism and world state, needs/drives/goals, ordinary accepted evidence, typed memory, relationships/preferences, development/skills and body-neutral intents.
- `care-core` is independently persisted and is the sole writer of accepted/rejected safety-input receipts, scenario policy results, degraded safety coverage, incidents, acknowledgment state and care audit.
- `identity-consent-vault` is the sole authority for consent/revocation, biometric templates or opaque handles, trusted contacts/roles, provider credential handles, encryption-key references/recovery metadata and privileged-change audit.
- `sensor-gateway` and authorized speech/perception producers own device leases, ephemeral buffers, quality/health state, uncertain observations and independently addressed safety candidates. They do not decide safety outcomes.
- `model-workers`, `godot-body`, `notify-adapter` and `ops-supervisor` are nonauthoritative adapters within explicit capabilities.

## Independent safety path

```text
authorized sensor/speech producer
├── ordinary observation → companion-core
└── safety candidate → care-core directly
```

`companion-core` cannot forward, gate, delay, suppress, modify or authorize a safety candidate. Companion outage or database failure cannot block the direct care path. Companion mood, memory, model/language output, dream content, animation and Godot state cannot create or suppress a care transition.

## Identity, consent, contacts and secrets

The vault is a required authority even when an implementation exposes only deny-all or synthetic contracts. Foreign processes receive only purpose-bound decisions, opaque role results, expiring capabilities, key references and redacted receipts. Biometric bytes, credential bytes, key material, full contact records and recovery secrets do not flow to Godot, models, ordinary logs, `companion-core` or `care-core`. Absent, locked, corrupt, unavailable and revoked states fail closed.

## Canonical event and time profile

- Canonical encoding: `JCS-RFC8785-v1`.
- Event digest: `sha-256-jcs-event-v1` over canonical UTF-8 semantic event content; transport framing/routing, retries, digest and signatures are excluded.
- Duplicate decoded keys, invalid Unicode/lone surrogates, NaN, Infinity, unsupported ranges and noncanonical representations are rejected.
- Canonical truth uses bounded integers, declared fixed-point integers or canonical decimal strings rather than platform-dependent floating point.
- Required ordering/time fields include `boot_id`, `monotonic_ns`, `utc_observed`, `utc_uncertainty_us`, owner `event_sequence` and `causation_id`.
- Monotonic time orders only within one boot. Owner sequence and causation establish cross-boot order.

## Storage and network

- Configuration, data, state, cache, logs, secrets, sockets, backups and exports use explicit local XDG paths.
- Canonical stores, WALs, locks, runtime sockets and backup staging use local ext4/NVMe, never the SSHFS checkout.
- Every mutable authority class has one writer. Shared writable databases are prohibited.
- Outbound runtime network is disabled by default. Cloud and notification adapters are optional, minimized, purpose-bound and never own continuity.

## Lifecycle and degradation

The supervisor verifies versions, schemas and directories, starts independent services, creates private channels and reports explicit readiness/degradation.

- Godot loss removes the visible body but does not alter organism or care truth.
- Companion loss stops ordinary creature activity but cannot block direct care input.
- Care loss removes the assistance claim and must produce visible degraded coverage.
- Vault loss denies protected operations.
- Sensor/model loss expires affected evidence and changes coverage.
- Store integrity failure freezes mutation and requires recovery; identity is never silently reseeded.
- Network/provider loss cannot be reported as delivery or acknowledgment.

## Phase 01 technology decisions

- **Authoritative service foundations:** Rust 1.98.1. Python is limited to qualification tooling and future nonauthoritative model/perception adapters behind typed IPC.
- **Godot:** exact official 4.7.2 Linux x86_64 artifact is approved as the implementation baseline. Existing 4.6 is not a substitute.
- **Persistence:** exact SQLite 3.53.4 is authorized as the Phase 01 development baseline for separate single-writer local stores using WAL, synchronous FULL, explicit checkpointing, versioned migrations, integrity checks and Backup API tests. Release eligibility remains conditional on later binding, broader fault and endurance evidence.
- **Direct-care IPC:** supervisor-created private `AF_UNIX` `SOCK_SEQPACKET`, kernel credentials, pidfd/generation binding and rotated capability material is the interim Phase 01 baseline under the documented threat ceiling.
- **Supervision:** project-owned Rust `ops-supervisor` is the child lifecycle and capability authority. systemd-user may be an optional outer launcher after later deployment qualification.
- **Contracts:** JSON Schema Draft 2020-12 plus the adopted canonical-event profile.
- **Dependency boundary:** exact crates/actions remain locked, rights-reviewed and independently accepted with the Phase 01 pull request.

## Roadmap placement

Roadmap Phase 00 has closed its implementation-opening gate.

Roadmap Phase 01 is active under `COMPANION-P01-FOUNDATION-001`. It covers the reproducible repository, process shells, schemas/canonicalization, XDG boundaries, isolated development stores, supervisor, direct synthetic care transport, Godot habitat shell, logs/health, deterministic controls, CI, SBOM/provenance, 1,000-cycle matrix and 60-minute soak.

“One remembered care loop plus shadow help” remains a later cross-phase architecture-proof milestone with bounded contributions from Phases 02, 03, 04 and 10. It completes none of those phases.

## Product and evidence boundary

No living mon, organism autonomy, long-term memory, speech, vision, learning, dreaming, production sprite body, notification delivery, spoken-help detection, safety efficacy, security certification, production reliability, SLA or medical capability is established by Phase 00 evidence or by this architecture document.

RQ-04 and RQ-07 through RQ-12 retain their open or partial status. Their safe bounded defaults constrain Phase 01; only the Architect records later resolution under operator guidance.

## Current execution authority

- Phase 00 qualification merge: `80dab0c1942e4a799328a957331381104b892945`.
- Phase 01 routing: `e41c0f92208c823450b029a0c5906398087cc419`.
- Active packet: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/`.
- Required branch: `codex/p01-foundation-001`.
- GitHub Issue #6: https://github.com/SketchOTP/companion/issues/6
- Notion directive: https://app.notion.com/p/3d7833cb27ff815ebe3ed1999f05beba
