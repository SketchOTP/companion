# Recommended Architecture v1.0

Status: `CORRECTED FOR ARCHITECT REVIEW — RECOMMENDED, NOT ADOPTED`

## Recommendation

Use a **local-first, event-sourced modular core with consequence-driven process isolation**. One `companion-core` owns ordinary creature truth; one independent `care-core` owns scenario qualification and incidents. Sensors, model execution, Godot, notification transport, and operations are adapters with no canonical mutation authority.

## Process and component map

| Process | Internal components | Canonical ownership | Explicitly does not own |
|---|---|---|---|
| `companion-core` | command gate; clock/world model; organism/homeostasis; goal/arbitration; ordinary-evidence ledger; memory projections; developmental/skill lifecycle; intent scheduler | creature ID/epoch, organism/world state, accepted ordinary evidence, typed memories, relationships/preferences, developmental gates, learned-skill versions, body-neutral intents | raw devices, renderer state, biometrics, contacts/secrets, safety-input validation or forwarding, caregiving incidents, external delivery |
| `care-core` | safety-input verifier/receipt journal; signed policy loader; deterministic scenario state machine; confirmation/fallback policy; incident journal; acknowledgment state | append-only safety-input receipts, active policy version, incident lifecycle, degraded coverage, safety audit | companion mood/goals, free-form model output, transport credentials, biometric/secret material, delivery claims |
| `sensor-gateway` / authorized speech producer | camera/audio ownership adapters; consent/session gates; pinned inference chain; quality metadata; ephemeral buffers; dual scoped output | device leases and ephemeral frames/samples only; source identity for its signed/peer-authenticated messages | durable belief, raw-media archive, identity, safety decision, care transition |
| `model-workers` | replaceable perception/speech/language inference sandboxes | ephemeral model working state and cache | canonical memory/state, direct tools, secrets, device ownership, network by default |
| `identity-consent-vault` | consent/revocation authority; biometric/contact/credential/key-reference storage; recovery metadata; privileged-change audit | consent grants/revocations, biometric templates or opaque handles, trusted contacts/roles, provider credential handles, encryption-key references/recovery metadata, enrollment/change audit | creature state, care policy or incidents, rendering, model inference, raw-media processing |
| `godot-body` | intent consumer; animation director; habitat/window adapter; input/status producer | presentation/session state only | organism, memory, consent, sensors, safety, credentials |
| `notify-adapter` | channel-specific send/receipt interface | provider request/receipt metadata only when live transport is separately authorized | incident policy, contact master, success-by-send assertion |
| `ops-supervisor` | service orchestration, health collection, backup/migration jobs, version inventory | operational health and lifecycle state | product decisions or domain truth |

Internally, `companion-core` must retain module boundaries and dependency direction:

`commands → append-only domain events → deterministic projections → decisions/intents`.

Evidence can cause proposed beliefs; a validation/promotion rule can append a belief event; no model or adapter writes a projection directly. Dream/replay emits synthetic proposal events in a distinct namespace and cannot satisfy factual promotion rules.

Safety candidates do not traverse `companion-core`. An authorized sensor/speech producer emits two independently addressed messages when one source observation is relevant to both domains:

```text
authorized sensor/speech producer
    ├── ordinary observation ──> companion-core
    └── safety candidate ──────> care-core directly
```

The messages may retain the same source `message_id`, evidence digest, producer identity, confidence, freshness, quality, and replay/media indicators, but each owner writes only its own immutable receipt/event. Shared identifiers support reconciliation; they confer no shared mutable authority. `companion-core` cannot validate, forward, delay, suppress, modify, or authorize a safety candidate. Only `care-core` authenticates the direct producer, appends a safety-input receipt, and evaluates the signed deterministic policy. A common sensor or speech-model outage sets explicit degraded safety coverage; it never preserves a false `normal` state.

## Interfaces

- Transport: local `AF_UNIX` `SOCK_STREAM` sockets under a private `$XDG_RUNTIME_DIR/companion/`; no localhost TCP by default.
- Envelope: length-prefixed UTF-8 JSON, parsed with duplicate-key rejection, validated against pinned JSON Schema Draft 2020-12 documents, then canonicalized under `JCS-RFC8785-v1` (RFC 8785 without local extensions).
- Required canonical event-content fields: `canonicalization_version`, `digest_version`, `schema_uri`, `schema_version`, `message_id`, `causation_id`, `correlation_id`, `producer`, `producer_version`, `boot_id`, `monotonic_ns`, `utc_observed`, `utc_uncertainty_us`, `event_sequence`, `privacy_class`, `authority_class`, and `payload`.
- Compatibility: additive fields only within a major version; consumers reject unsupported major versions and unknown authority classes; unknown non-authority fields are ignored. Schemas and golden fixtures are versioned.
- Commands require an idempotency key and return accepted/rejected plus the resulting event sequence. Events are immutable and globally ordered per owning store.
- Backpressure is bounded. Noncritical telemetry may be dropped with an explicit counter; evidence, commands, incidents, acknowledgments, and audit may never be silently dropped.
- Peer authorization uses filesystem ownership/mode plus Unix peer credentials. Message-declared identity is never trusted by itself.

### Canonical bytes, digests, numbers, and time

- `JCS-RFC8785-v1` emits the RFC 8785 representation as UTF-8: no token whitespace, recursively sorted object properties, unchanged array order, and Unicode strings preserved as supplied. Parsers reject duplicate object names, invalid Unicode/lone surrogates, NaN, Infinity, and any non-I-JSON value before authority logic. Unicode normalization is not performed; canonically equivalent but byte-different strings remain distinct and schema/domain validation decides whether a field permits them.
- `sha-256-jcs-event-v1` is lowercase hexadecimal SHA-256 over the JCS bytes of the complete `event_content` object. That object includes the semantic envelope fields listed above and the payload. It excludes only transport framing/routing, retry counters, `event_digest`, and any `signatures` collection, preventing recursive hashing. A signature, when later authorized, signs the ASCII domain separator `COMPANION-EVENT-SHA256-V1\n` followed by the 32 digest bytes and declares key handle/algorithm separately; signatures never make an unauthorized producer authoritative.
- Canonical organism, policy, drive, sequence, and event values never use binary floating-point. Quantities use bounded JSON integers within the interoperable exact range `[-9007199254740991, 9007199254740991]`, fixed-point integers with an explicit unit/scale in schema, or canonical decimal strings matching `0|-[1-9][0-9]*|[1-9][0-9]*` when a wider integer range is required. Fractional observations use fixed-point integers or a separately specified canonical decimal-string grammar; exponent notation, leading plus, leading zero, and negative zero are rejected for those strings.
- `boot_id` is a fresh opaque 128-bit identifier per OS boot and is not a stable machine identifier. `monotonic_ns` is a nonnegative canonical decimal string meaningful only with its `boot_id`. `utc_observed` is normalized RFC 3339 UTC text with fixed microsecond precision; `utc_uncertainty_us` is a nonnegative bounded integer. UTC is an observation, never the sole ordering authority.
- Each canonical owner assigns a strictly increasing, gap-tolerant `event_sequence` (canonical decimal string) when it durably appends an event. Cross-boot order is owner identity plus `event_sequence`; `causation_id` establishes the causal chain. Within one boot, `(boot_id, monotonic_ns)` can measure intervals. No comparison of monotonic values from different boot IDs is valid.
- Golden fixtures must include canonical bytes and digest, duplicate-key/Unicode/numeric rejection, signature-scope checks, same-boot interval cases, reboot epochs, UTC steps/uncertainty, and cross-boot sequence/causation replay.

## Persistence and directories

Proposed XDG layout (exact paths remain implementation-time configuration):

| Class | Default | Content |
|---|---|---|
| Config | `$XDG_CONFIG_HOME/companion/` | nonsecret user configuration and selected display |
| Durable owner data | `$XDG_DATA_HOME/companion/` | canonical stores, exports, sprite packs after authorization |
| Operational state | `$XDG_STATE_HOME/companion/` | logs, health history, migration journal |
| Cache | `$XDG_CACHE_HOME/companion/` | regenerable model/asset caches |
| Runtime | `$XDG_RUNTIME_DIR/companion/` mode 0700 | sockets, leases, ephemeral buffers |

The SSHFS checkout is source/governance only. Live stores, WALs, locks, sockets, exports, and backup staging must be on local ext4/NVMe.

Shortlist SQLite for the companion event/projection store and a separate care safety-input/incident store, each with one writer. Eligibility requires one exact supported, non-withdrawn SQLite release or one specifically documented fixed backport; numeric comparison such as `3.51.3+` is forbidden. The record must include the exact version, source ID/digest, binding, compile options, local filesystem, writer/connection topology, checkpoint policy, Backup API use, migration behavior, and current vulnerability/compatibility disposition. Approval remains conditional on crash, concurrent read/write/checkpoint, disk-full/read-only, backup, restore, and migration tests. Multi-database transactions are not assumed atomic.

The `identity-consent-vault` boundary exists in v1 even if the first authorized foundation uses only a contract stub. Its minimum interfaces are: purpose-scoped `evaluate_consent`; opaque `resolve_subject_handle`; least-data `resolve_contact_role`; one-operation `mint_provider_capability`; `resolve_key_reference`; and authenticated enrollment/revoke/recovery operations with append-only privileged audit. Responses contain decisions, opaque handles, and expiry—not biometric templates, credentials, key bytes, or full contact records. Godot, model workers, general logs, `companion-core`, and `care-core` never receive secret or biometric material.

## Startup, shutdown, and recovery

1. Supervisor verifies version manifest, schema/canonicalization compatibility, local-directory permissions, and store integrity.
2. `identity-consent-vault` starts or publishes a typed unavailable/locked state; no caller substitutes cached secret material.
3. `care-core` starts independently, opens its safety-input and incident journals without the companion database, and publishes policy/coverage health.
4. `companion-core` opens its single-writer store, replays from the last verified snapshot, checks projection hashes, and publishes readiness.
5. Device/model adapters start only with required consent/config and advertise capabilities as available/unavailable.
6. Godot starts last, binds to the adopted display, receives a full presentation snapshot, then consumes intents.
7. On orderly shutdown, new commands stop, in-flight durable messages settle, snapshots/checkpoints complete, adapters release leases, and an exit marker records versions, boot ID, and sequence positions.

After a crash, stores are recovered before accepting mutation; idempotent commands are reconciled from the journal; projections are reproducible from events; the renderer receives a new snapshot; expired evidence is not replayed as current perception. Repeated failure enters a visible degraded state rather than a silent loop.

## Degradation policy

| Failure | Required behavior |
|---|---|
| Godot unavailable | Creature truth continues; no presentation claim; care core remains independent; health records `body_unavailable`. |
| Model worker unavailable | Deterministic organism/reflexes continue; affected capability is explicitly unavailable; no invented result. |
| Camera unavailable | Vision evidence stops and expires; no inference from stale frames; no effect on explicit spoken-help path. |
| Microphone unavailable | Spoken-help coverage becomes unavailable; visible/accessibility fallback is required before any live claim. |
| Network/cloud unavailable | Local core continues; optional augmentation and transport report unavailable; never claim contact delivery. |
| Notification stub/provider unavailable | Incident continues with unacknowledged/unavailable state; no success-by-send. |
| Companion core unavailable | Care core may continue its already-qualified input path; Godot shows degraded state without simulating normal continuity. |
| Care core unavailable | Companion may continue, but must not claim check-in/trusted-contact assistance. |
| Vault absent/locked/unavailable | Live sensing requiring consent, identity matching, privileged changes, contact resolution, credential use, and external delivery are unavailable; companion/care publish the exact degraded capability. Preapproved synthetic test fixtures may run only in explicit test/shadow mode. |
| Vault corrupted | Freeze vault mutations, invalidate issued capabilities, preserve forensic/recovery evidence, and require authenticated recovery; never auto-reseed consent, contacts, biometrics, credentials, or keys. |
| Consent revoked | Revoke acquisition and derived capability tokens for that purpose, reject later inputs, stop new processing/delivery, and expose retention/deletion work still required by policy. Revocation never silently appears as normal coverage. |
| Store integrity failure | Freeze mutations, preserve evidence, expose recovery-required; never auto-reseed identity. |

## Update, migration, backup, and replacement seams

- Immutable release manifest identifies code, schemas, migrations, Godot build, models, weights, datasets, voices, assets, plugins, policies, and services independently.
- Migration is forward, preflighted, backed up, checksummed, resumable, and rollback-safe; old readers never write newer stores.
- Backup uses a database-consistent snapshot/API, then encrypts and verifies it before declaring success. Copying a live database file is not a backup.
- Export is a documented, versioned owner-portable bundle with a manifest, hashes, schema versions, data-class inventory, and restore report.
- Restore is proven only by replacement-directory/body equivalence tests, not archive creation.
- Updates are staged, signed, vulnerability/rights-reviewed, regression-qualified, and rollback-capable. Safety policy and model changes have separate approvals.

## Network and cloud boundary

Default all processes to no outbound network. Only a future, explicitly configured cloud/notification adapter may cross the boundary. It receives a purpose-bound, minimized request, never the canonical store or raw ambient media; it returns an untrusted proposal/receipt. Credentials remain in a dedicated vault and never enter Godot, models, logs, or the repository. RQ-04 and RQ-10 remain open.

## Open experiments and decisions

This recommendation depends on: exact Godot 4.7.2 acquisition/integrity; Vulkan and GPU selection; window/display recovery; camera/audio quality and contention; resource concurrency; the Python 3.12 versus one Architect-approved Rust-or-Go comparator evidence gate; one exact eligible SQLite build and crash behavior; vault implementation/security selection; service supervision on the degraded host; backup/restore; power/thermal/noise; and endurance. RQ-04, RQ-07–RQ-12 remain as dispositioned in `PRODUCT_CONTRACT_DISPOSITIONS.md`.

Architect adoption is required before any implementation.
