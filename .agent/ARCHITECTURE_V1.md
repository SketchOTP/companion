# Architecture v1.0 — Adopted Local Runtime and Authority Model

Status: `ADOPTED — ARCHITECT REVIEW 02`

Canonical Notion: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556

Architect Review 02: https://app.notion.com/p/3d6833cb27ff81d88785f64d0629286c

Reviewed correction: `25b1c737d6f8f1f861a36355909c2a51ea5c64ea`

Reviewed publication: `1ceb330d4c2321b500a138b8acfdfeb4279c08e7`

This file is a repository routing mirror. Live Notion remains authoritative for project meaning and decisions.

## Adopted topology

- `companion-core` is the sole ordinary creature-truth owner: identity/epoch, organism and world state, needs/drives/goals, ordinary accepted evidence, typed memory, relationships/preferences, development/skills, and body-neutral intents.
- `care-core` is independently persisted and is the sole writer of accepted/rejected safety-input receipts, scenario policy results, degraded safety coverage, incidents, acknowledgment state, and care audit.
- `identity-consent-vault` is the sole authority for consent/revocation, biometric templates or opaque handles, trusted contacts/roles, provider credential handles, encryption-key references/recovery metadata, and privileged-change audit.
- `sensor-gateway` and authorized speech/perception producers own device leases, ephemeral buffers, quality/health state, ordinary observations, and independently addressed safety candidates. They do not decide safety outcomes.
- `model-workers`, `godot-body`, `notify-adapter`, and `ops-supervisor` are nonauthoritative adapters within explicit capabilities.

## Independent safety path

```text
authorized sensor/speech producer
├── ordinary observation → companion-core
└── safety candidate → care-core directly
```

`companion-core` cannot forward, gate, delay, suppress, modify, or authorize a safety candidate. A companion outage/database failure cannot block the direct care path. Companion mood, memory, model/language output, dream content, animation, and Godot state cannot create or suppress a care transition.

## Event and time profile

- Canonical encoding: `JCS-RFC8785-v1`.
- Event digest: `sha-256-jcs-event-v1` over canonical UTF-8 semantic `event_content`; transport framing/routing, retries, digest, and signatures are excluded.
- Duplicate keys, invalid Unicode/lone surrogates, NaN, Infinity, unsupported ranges, and noncanonical representations are rejected.
- Canonical truth uses bounded integers, declared fixed-point integers, or canonical decimal strings rather than platform-specific floating-point serialization.
- Required order/time fields: `boot_id`, `monotonic_ns`, `utc_observed`, `utc_uncertainty_us`, owner `event_sequence`, and `causation_id`.
- Monotonic time orders only within a boot. Owner sequence and causation are authoritative across boots.

## IPC trust implementation gate

AF_UNIX socket permissions, peer credentials, and message fields do not by themselves prove an authorized safety producer when processes may share one Linux UID. Before direct safety ingress is implemented, Phase 01 must select and target-test an enforceable process identity/capability mechanism. Candidate mechanisms include distinct OS identities, supervisor-created private descriptor channels plus confinement and peer verification, Linux security labels, or a separately justified cryptographic capability.

Unauthorized same-user processes must be unable to create valid safety inputs. Message-declared identity alone is never authority.

## Storage and network

- Runtime configuration/data/state/cache/logs/secrets/sockets/backups/exports use explicit local XDG paths.
- Canonical stores, WALs, locks, sockets, and backup staging use local ext4/NVMe, never the SSHFS checkout.
- One writer exists per mutable authority class; shared writable databases are prohibited.
- Outbound network is disabled by default. Cloud and notification services are optional, minimized, purpose-bound adapters and never own continuity.
- SQLite is conditional only: one exact currently supported non-withdrawn release or documented fixed backport, exact build/binding/topology evidence, and successful crash/checkpoint/disk/migration/backup/restore qualification. No numeric minimum rule.

## Roadmap placement

Roadmap Phase 01 is the engineering foundation: reproducible workspace, process shells, schemas/canonicalization fixtures, XDG boundaries, logs/health, deterministic controls, supervisor foundation, CI, and provenance.

“One remembered care loop plus shadow help” is a later cross-phase architecture-proof milestone with bounded contributions from Phases 02, 03, 04, and 10. Passing it completes none of those phases.

## Technology state

- Godot 4.7.2: operator-selected, absent/unqualified on the host.
- Core language: Python 3.12 candidate versus Rust selected as the single compiled comparator. No winner.
- Contracts: JSON Schema Draft 2020-12 plus the adopted JCS/digest profile; implementation unselected.
- Persistence: SQLite conditional exact-build candidate; no build approved.
- Supervision: systemd user services conditional on host qualification.
- Speech, vision, LLM, TTS voice, biometrics, notification provider, and vault implementation remain unselected.

## Authority boundary

Architecture v1.0 is adopted. Roadmap Phase 00 remains active. Roadmap Phase 01, experiments, dependencies, product implementation, and product capability require later explicit Architect directives and acceptance.
