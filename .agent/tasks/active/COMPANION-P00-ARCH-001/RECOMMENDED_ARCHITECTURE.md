# Recommended Architecture v1.0

Status: `COMPLETE — RECOMMENDED, NOT ADOPTED`

## Recommendation

Use a **local-first, event-sourced modular core with consequence-driven process isolation**. One `companion-core` owns ordinary creature truth; one independent `care-core` owns scenario qualification and incidents. Sensors, model execution, Godot, notification transport, and operations are adapters with no canonical mutation authority.

## Process and component map

| Process | Internal components | Canonical ownership | Explicitly does not own |
|---|---|---|---|
| `companion-core` | command gate; clock/world model; organism/homeostasis; goal/arbitration; evidence ledger; memory projections; developmental/skill lifecycle; intent scheduler | creature ID/epoch, organism/world state, accepted evidence, typed memories, relationships/preferences, developmental gates, learned-skill versions, body-neutral intents | raw devices, renderer state, biometrics, contacts/secrets, caregiving incidents, external delivery |
| `care-core` | signed policy loader; deterministic scenario state machine; confirmation/fallback policy; incident journal; acknowledgment state | active policy version, incident lifecycle, degraded coverage, safety audit | companion mood/goals, free-form model output, transport credentials, delivery claims |
| `sensor-gateway` | camera/audio ownership adapters; consent/session gates; quality metadata; ephemeral buffers | device leases and ephemeral frames/samples only | durable belief, raw-media archive, identity, safety decision |
| `model-workers` | replaceable perception/speech/language inference sandboxes | ephemeral model working state and cache | canonical memory/state, direct tools, secrets, device ownership, network by default |
| `godot-body` | intent consumer; animation director; habitat/window adapter; input/status producer | presentation/session state only | organism, memory, consent, sensors, safety, credentials |
| `notify-adapter` | channel-specific send/receipt interface | provider request/receipt metadata only when live transport is separately authorized | incident policy, contact master, success-by-send assertion |
| `ops-supervisor` | service orchestration, health collection, backup/migration jobs, version inventory | operational health and lifecycle state | product decisions or domain truth |

Internally, `companion-core` must retain module boundaries and dependency direction:

`commands → append-only domain events → deterministic projections → decisions/intents`.

Evidence can cause proposed beliefs; a validation/promotion rule can append a belief event; no model or adapter writes a projection directly. Dream/replay emits synthetic proposal events in a distinct namespace and cannot satisfy factual promotion rules.

## Interfaces

- Transport: local `AF_UNIX` `SOCK_STREAM` sockets under a private `$XDG_RUNTIME_DIR/companion/`; no localhost TCP by default.
- Envelope: UTF-8 JSON, length-prefixed, validated against pinned JSON Schema Draft 2020-12 documents.
- Required envelope fields: `schema_uri`, `schema_version`, `message_id`, `causation_id`, `correlation_id`, `producer`, `producer_version`, `occurred_at_monotonic`, `observed_at_utc`, `privacy_class`, `authority_class`, `payload`.
- Compatibility: additive fields only within a major version; consumers reject unsupported major versions and unknown authority classes; unknown non-authority fields are ignored. Schemas and golden fixtures are versioned.
- Commands require an idempotency key and return accepted/rejected plus the resulting event sequence. Events are immutable and globally ordered per owning store.
- Backpressure is bounded. Noncritical telemetry may be dropped with an explicit counter; evidence, commands, incidents, acknowledgments, and audit may never be silently dropped.
- Peer authorization uses filesystem ownership/mode plus Unix peer credentials. Message-declared identity is never trusted by itself.

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

Shortlist SQLite for the companion event/projection store and a separate care incident store, each with one writer. Do not approve it until the exact embedded version includes the WAL-reset fix (SQLite 3.51.3+, or an explicitly documented fixed backport) and crash/checkpoint/migration/backup experiments pass. Multi-database transactions are not assumed atomic. Secrets and biometric templates require a separately encrypted vault implementation selected after threat/legal review; neither is present in the first slice.

## Startup, shutdown, and recovery

1. Supervisor verifies version manifest, schema compatibility, local-directory permissions, and store integrity.
2. `care-core` starts independently and publishes policy/coverage health.
3. `companion-core` opens its single-writer store, replays from the last verified snapshot, checks projection hashes, and publishes readiness.
4. Device/model adapters start only with required consent/config and advertise capabilities as available/unavailable.
5. Godot starts last, binds to the adopted display, receives a full presentation snapshot, then consumes intents.
6. On orderly shutdown, new commands stop, in-flight durable messages settle, snapshots/checkpoints complete, adapters release leases, and an exit marker records versions and sequence positions.

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

This recommendation depends on: exact Godot 4.7.2 acquisition/integrity; Vulkan and GPU selection; window/display recovery; camera/audio quality and contention; resource concurrency; fixed SQLite version and crash behavior; service supervision on the degraded host; backup/restore; power/thermal/noise; and endurance. RQ-04, RQ-07–RQ-12 remain as dispositioned in `PRODUCT_CONTRACT_DISPOSITIONS.md`.

Architect adoption is required before any implementation.
