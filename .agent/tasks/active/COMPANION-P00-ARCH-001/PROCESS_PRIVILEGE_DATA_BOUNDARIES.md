# Process, Privilege, Authority, and Data Boundaries

Status: `COMPLETE — PROPOSAL FOR ARCHITECT REVIEW`

## Trust zones

| Zone | Members | Trust posture |
|---|---|---|
| Z0 Authority/build | reviewed source, schemas, release/policy manifests, migrations, signed artifacts | Offline/versioned authority; cannot be mutated by runtime |
| Z1 Care authority | `care-core`, care incident store, signed policy | Highest runtime consequence; deterministic, no model/device/network privileges |
| Z2 Companion authority | `companion-core`, companion store | Owns creature truth; no direct devices, external network, or secrets |
| Z3 Secret/identity vault | future vault service | Separate encryption/key/credential/biometric authority; absent in first slice |
| Z4 Untrusted compute | model workers, optional cloud response | Treat all outputs as proposals/evidence with provenance and limits |
| Z5 Device edge | sensor gateway and ephemeral buffers | Private raw media; least retention; uncertain evidence only |
| Z6 Presentation | Godot body | User-visible but nonauthoritative; input/status must be validated |
| Z7 External | notification providers, contacts, update sources, cloud models | Untrusted availability/content; every crossing purpose-bound and audited |
| Z8 Operations | supervisor, health, backup/migration tooling | Can start/stop and report, but cannot forge domain events or incidents |

## Single-owner authority table

| State/authority class | Sole writer/owner | Readers | Mutation path |
|---|---|---|---|
| Creature identity/epoch | companion core | Godot, export, care by opaque ID | validated command → event |
| World/organism/drives/goals | companion core | Godot, bounded model context | deterministic tick/command → event |
| Raw perception | sensor gateway, ephemeral only | designated model worker | consented lease; never durable by default |
| Perception evidence | companion core evidence ledger | memory/organism/care through scoped views | authenticated evidence proposal → validation → append |
| Typed memories/beliefs | companion core | bounded retrieval APIs | evidence-backed promotion/correction event |
| Dream/synthetic material | companion core, distinct synthetic namespace | bounded reflection/planning | synthetic proposal; cannot promote itself |
| Developmental gates/skills | companion core | Godot/models | qualified promotion/revoke event |
| Display/window/session | Godot body | supervisor | adapter-local; reconstructable |
| Consent grants | future vault/consent authority; companion core holds nonsecret reference | sensor/care via scoped decision API | authenticated user workflow; absent first slice |
| Biometric templates | future vault only | identity matcher via opaque handle | enrollment workflow; absent first slice |
| Trusted contacts | future vault only | care core receives minimum routing token | authenticated configuration; absent first slice |
| Scenario policy | care core loads signed, versioned read-only policy | supervisor/reporting | reviewed release artifact only |
| Incident state/audit | care core | owner/auditor/export | deterministic policy transition |
| Provider delivery/receipt | notify adapter | care core | idempotent adapter response; never rewrites incident |
| Secrets/keys | future vault/OS keystore | specific adapter through capability handle | never IPC plaintext or log |
| Operational health | supervisor | Godot/diagnostics/care | process health/event; no domain authority |
| Release provenance | build/release pipeline | supervisor/auditor | signed immutable artifact |

There is no shared writable database and no process can approve its own authority escalation. Care can consume a minimized companion/sensor observation but companion cannot direct a care transition. Notify can report a provider receipt but only care interprets it. Operations can restart a service but cannot fabricate readiness.

## Capability/privilege matrix

| Process | Filesystem | Devices | Network | Secrets | Allowed IPC |
|---|---|---|---|---|---|
| companion core | RW own local store/state; RO config/schemas | none | none | none | sensor evidence, model proposals, Godot status/input, care minimized observations |
| care core | RW own incident/audit store; RO signed policy | none in first slice | none | opaque contact capability only after authorization | qualified evidence input, notification request/receipt |
| sensor gateway | RW private ephemeral runtime; no durable raw-media path | explicit camera/audio nodes only | none | consent decision token only | frames/samples to one worker; evidence proposal out |
| model worker | RW regenerable cache; RO selected model artifact | none | none by default | none | input from gateway/core; typed proposal out |
| Godot body | RW presentation config/cache only; RO approved assets | display/input; no camera/mic | none | none | intents in; user action/body status out |
| notify adapter | minimal operational state | none | destination-specific egress only | one provider credential handle | requests from care; receipts to care |
| supervisor | RO release/config; RW health/state/backup staging | none | update network only in separately authorized job | signing verification keys, not provider/user secrets | health/start-stop only |

Later service units should default to `NoNewPrivileges`, read-only system paths, private temporary storage, restricted address families, explicit device allowlists, and explicit writable paths. Each setting must be target-host tested; camera/audio/display services require carefully scoped exceptions, not blanket weakening.

## Data classes and retention defaults

| Class | Examples | Default rule |
|---|---|---|
| D0 public | version, nonpersonal schema | loggable |
| D1 operational | health, latency, error code | structured/minimized; no private payload |
| D2 personal | preferences, relationship, routine | local encrypted-at-rest candidate; owner rights apply |
| D3 highly sensitive | ambient evidence, autobiographical memory, distress incident | local, purpose-limited, access-audited, shortest justified retention |
| D4 biometric/secret | templates, provider credentials, encryption keys | separate vault, opaque handles, never renderer/model/log |
| D5 synthetic | dream/model proposals | explicit synthetic provenance; no factual promotion without real evidence |

Raw camera/audio is D3 and ephemeral. The first slice uses synthetic fixtures only. Any later raw retention requires a separate operator decision, consent UX, retention/deletion contract, legal review, and validation.

## Principal flows

1. **Ordinary companion loop:** simulated/device evidence proposal → companion validation → D3/D2 evidence event → deterministic organism/memory projection → body-neutral intent → Godot animation/status → user action command → event.
2. **Model assistance:** core sends minimized bounded context → worker returns typed untrusted proposal → core validates/accepts/rejects → event. Worker cannot call tools or mutate stores.
3. **Spoken-help path:** audio gateway/ASR later emits uncertain transcript evidence → care input gate checks source/quality/freshness/replay flags → deterministic policy transitions → confirmation/fallback → notification request → receipt/acknowledgment. First slice substitutes a signed synthetic fixture and stub transport.
4. **Backup/export:** owner-authenticated request → owning services produce consistent snapshots → manifest/hashes/encryption → restore verification. Operations coordinates but does not interpret domain truth.
5. **Update:** signed manifest → offline verification and rights/security gates → backup → compatibility/migration preflight → staged activation → health/regression checks → rollback if failed.

## Boundary invariants and tests

- Every durable row/event maps to exactly one owner.
- No IPC request can write a foreign store.
- Unsupported schema major, stale evidence, unknown authority, duplicate message, or absent consent fails closed and is audited.
- Care decisions are reproducible from policy version plus ordered inputs.
- Godot/model/network failure cannot mutate or erase canonical state.
- Companion mood, model prose, and dream material cannot cause a care transition.
- A provider send receipt is not a trusted-contact acknowledgment.
- Logs contain IDs/classifications, not raw media, secrets, transcripts, or memory payloads.
- Socket/file permissions and peer-credential rejection receive automated integration tests.
- Process dependency graph is acyclic: authority/build → owners → adapters/presentation; no lower zone becomes upstream authority.

## Failure/degradation

Queues use bounded capacity and explicit overflow policy. Durable inputs use outbox/inbox or owner-local transactions; at-least-once delivery is made safe with idempotency keys. Loss of noncritical telemetry increments a counter. Loss of evidence/incident persistence stops the affected authority from advancing. A missing sensor expires capability immediately; a missing renderer never causes synthetic user interaction; a missing transport leaves an incident unacknowledged.
