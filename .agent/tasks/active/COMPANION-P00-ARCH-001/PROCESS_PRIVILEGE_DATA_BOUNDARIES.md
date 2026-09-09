# Process, Privilege, Authority, and Data Boundaries

Status: `CORRECTED — PROPOSAL FOR ARCHITECT REVIEW`

## Trust zones

| Zone | Members | Trust posture |
|---|---|---|
| Z0 Authority/build | reviewed source, schemas, release/policy manifests, migrations, signed artifacts | Offline/versioned authority; cannot be mutated by runtime |
| Z1 Care authority | `care-core`, care incident store, signed policy | Highest runtime consequence; deterministic, no model/device/network privileges |
| Z2 Companion authority | `companion-core`, companion store | Owns creature truth; no direct devices, external network, or secrets |
| Z3 Secret/identity vault | `identity-consent-vault` | Explicit consent/contact/credential/key/biometric authority; interface stub only in the cross-phase milestone, with all privileged capabilities denied |
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
| Ordinary perception evidence | companion core evidence ledger | memory/organism through scoped views | authenticated ordinary-evidence proposal → validation → append |
| Safety-input receipt | care core append-only safety-input journal | care policy/auditor through scoped reads | authenticated direct producer candidate → immutable accepted/rejected receipt; never via companion core |
| Typed memories/beliefs | companion core | bounded retrieval APIs | evidence-backed promotion/correction event |
| Dream/synthetic material | companion core, distinct synthetic namespace | bounded reflection/planning | synthetic proposal; cannot promote itself |
| Developmental gates/skills | companion core | Godot/models | qualified promotion/revoke event |
| Display/window/session | Godot body | supervisor | adapter-local; reconstructable |
| Consent grants/revocations | identity-consent vault; callers hold only expiring purpose handle | sensor/care via scoped decision API | authenticated user workflow; contract stub denies live capabilities in milestone |
| Biometric templates/handles | identity-consent vault only | authorized matcher via opaque, purpose-bound handle | enrollment/revocation workflow; absent in milestone |
| Trusted contacts/roles | identity-consent vault only | care gets role decision; notify gets one-operation delivery capability | authenticated configuration/change workflow; absent in milestone |
| Scenario policy | care core loads signed, versioned read-only policy | supervisor/reporting | reviewed release artifact only |
| Incident state/audit | care core | owner/auditor/export | deterministic policy transition |
| Provider delivery/receipt | notify adapter | care core | idempotent adapter response; never rewrites incident |
| Provider credentials/key references/recovery metadata | identity-consent vault/selected keystore | specific adapter through one-operation capability; recovery workflow through authenticated interface | never IPC plaintext, foreign store, model context, renderer, or log |
| Enrollment/privileged-change audit | identity-consent vault append-only audit | owner/auditor through redacted export | authenticated create/revoke/recover/change operation |
| Operational health | supervisor | Godot/diagnostics/care | process health/event; no domain authority |
| Release provenance | build/release pipeline | supervisor/auditor | signed immutable artifact |

There is no shared writable database and no process can approve its own authority escalation. `care-core` accepts safety candidates only from an independently authorized sensor/speech producer over its direct socket; it does not consume a companion-forwarded safety input. A separate ordinary-observation copy may reach `companion-core` under the same source message ID/evidence digest, but neither receipt grants mutation rights over the other store. Notify can report a provider receipt but only care interprets it. Operations can restart a service but cannot fabricate readiness.

## Capability/privilege matrix

| Process | Filesystem | Devices | Network | Secrets | Allowed IPC |
|---|---|---|---|---|---|
| companion core | RW own local store/state; RO config/schemas | none | none | none | ordinary sensor evidence, model proposals, Godot status/input, care presentation request only |
| care core | RW own safety-input/incident/audit store; RO signed policy | none in milestone | none | none; only opaque contact-role decision after live authorization | direct safety candidate from authorized producer, notification request/receipt, vault decision handles |
| sensor gateway / authorized speech producer | RW private ephemeral runtime; no durable raw-media path | explicit camera/audio nodes only | none | expiring purpose consent handle only | frames/samples to one worker; ordinary observation to companion; safety candidate directly to care |
| model worker | RW regenerable cache; RO selected model artifact | none | none by default | none | input from gateway/core; typed proposal out |
| identity-consent vault | RW own encrypted candidate store/audit; RO recovery/config metadata | approved secure-hardware interface only if later selected | none by default | sole secret/biometric material authority | scoped consent/role decisions and opaque expiring capabilities only |
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

1. **Ordinary companion loop:** simulated/device ordinary-evidence proposal → companion validation → D3/D2 evidence event → deterministic organism/memory projection → body-neutral intent → Godot animation/status → user action command → event.
2. **Model assistance:** core sends minimized bounded context → worker returns typed untrusted proposal → core validates/accepts/rejects → event. Worker cannot call tools or mutate stores.
3. **Dual sensor/speech output:** the authorized producer creates independently addressed ordinary and safety-candidate messages from one observation. Both may cite the same immutable source `message_id`, producer identity, evidence digest, confidence, freshness, quality, and replay/media flags. Ordinary observation goes to `companion-core`; safety candidate goes directly to `care-core`. The producer cannot decide a care transition.
4. **Spoken-help safety path:** authorized audio/speech producer → direct care socket → peer/capability/schema/digest/freshness/quality/replay validation → append-only accepted/rejected safety-input receipt → deterministic policy transition → confirmation/fallback → notification request → receipt/acknowledgment. The cross-phase milestone substitutes an authorized synthetic producer and stub transport.
5. **Vault decision/capability path:** caller submits purpose, subject/contact opaque reference, and operation → vault authenticates caller and evaluates current consent/role → vault returns deny or a short-lived least-data capability. Template bytes, credentials, key bytes, full contacts, and recovery secrets never leave the vault.
6. **Backup/export:** owner-authenticated request → owning services produce consistent snapshots → manifest/hashes/encryption → restore verification. Operations coordinates but does not interpret domain truth.
7. **Update:** signed manifest → offline verification and rights/security gates → backup → compatibility/migration preflight → staged activation → health/regression checks → rollback if failed.

## Boundary invariants and tests

- Every durable row/event maps to exactly one owner.
- No IPC request can write a foreign store.
- Unsupported schema major, stale evidence, unknown authority, duplicate message, duplicate JSON key, invalid canonical bytes/digest, cross-boot monotonic comparison, or absent consent fails closed and is audited.
- Care decisions are reproducible from policy version plus ordered inputs.
- Godot/model/network failure cannot mutate or erase canonical state.
- Companion messages are not an allowed safety-input producer. Companion mood, memory, model prose, language output, dream material, and animation state cannot cause or suppress a care transition.
- Stopping `companion-core` cannot close, delay, or apply backpressure to the producer→care socket; care processing and recovery never open the companion database.
- Duplicate direct safety candidates are idempotent by producer identity plus source `message_id`/evidence digest; accepted and duplicate receipts remain auditable without duplicate incident transitions.
- A provider send receipt is not a trusted-contact acknowledgment.
- Logs contain IDs/classifications, not raw media, secrets, transcripts, or memory payloads.
- Socket/file permissions and peer-credential rejection receive automated integration tests.
- Process dependency graph is acyclic: authority/build → owners → adapters/presentation; no lower zone becomes upstream authority.

## Failure/degradation

Queues use bounded capacity and explicit overflow policy. The safety producer has a dedicated care queue/socket and cannot share companion backpressure. Durable inputs use producer outbox plus owner-local receipt transactions; at-least-once delivery is made safe with idempotency keys. Loss of noncritical telemetry increments a counter. Loss of safety-input or incident persistence stops care from advancing and exposes degraded coverage. A sensor/model outage or expired producer capability explicitly sets `coverage_input_unavailable`; it never reports false normality. A missing renderer never causes synthetic user interaction; a missing transport leaves an incident unacknowledged.

Vault states are explicit: **absent** means the component/contract is not installed and every live privileged operation is denied; **locked** means records exist but no protected material or capability is released; **corrupted** freezes mutation, invalidates issued capabilities, preserves recovery evidence, and requires authenticated restore; **unavailable** returns typed temporary failure with no cache fallback; **revoked consent** invalidates purpose handles, stops new acquisition/processing/delivery, and exposes pending retention/deletion obligations. In every state, companion and care may continue only capabilities independent of the vault and must publish the precise degradation.

## Required negative integration tests

1. Stop `companion-core`, deliver a valid safety candidate over the direct producer→care path, and prove a care-owned receipt/incident transition without opening the companion store.
2. Send a well-formed, malformed, and digest-valid message from companion peer credentials to the care safety socket; all are rejected as unauthorized and create no incident.
3. Redeliver one valid safety candidate before and after care restart; one logical input and at most one policy transition result, with duplicate receipts/reasons retained.
4. Withdraw sensor or speech-model health/capability; care changes to explicit degraded input coverage and cannot retain or display normal coverage.
5. Remove or corrupt the companion database while care processes a synthetic direct input; care remains functional and makes no companion-store access.
6. Attempt care transitions from mood, memory, LLM text, dream, animation, and Godot status messages; every attempt is rejected and audited.
