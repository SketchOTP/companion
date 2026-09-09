# First Vertical-Slice Contract

Status: `COMPLETE — PROPOSED PHASE-01 CONTRACT; NOT AUTHORIZED`

## Slice: “One remembered care loop plus shadow help”

On the adopted 1366×768 Openbox display, a real Godot 4.7.2 bounded window presents the approved mon responding to a deterministic synthetic encounter. The encounter changes a named homeostatic drive, creates an evidence-backed episodic memory, and produces a body-neutral intent that Godot renders. After controlled process restart, the same individual restores the committed change and references the encounter through a structured, non-LLM recall. In parallel, a synthetic explicit-help fixture traverses the separate care policy to a shadow incident and stub acknowledgment without sending a real notification or changing companion state.

This exercises identity continuity, organism causality, typed memory, uncertain evidence, embodiment separation, care separation, restart/recovery, degradation, and evidence/provenance. It intentionally does not claim conversation, real perception, real speech recognition, caregiving efficacy, or deployment readiness.

## Real, simulated, stubbed, absent

| Surface | Slice treatment |
|---|---|
| Godot 4.7.2 build and bounded window | **Real**, exact verified build; adopted display |
| Approved mon identity | **Real authored test sprite subset** only after separate asset authority; must pass visual bible/MON_FRAME_V1 |
| companion core/event/memory store | **Real minimal implementation** |
| organism | **Real deterministic two-drive subset** with explicit arbitration |
| world/evidence | **Synthetic fixture**, schema-valid and clearly marked |
| recall | **Real structured retrieval**, no LLM |
| care core/policy/incident journal | **Real minimal deterministic shadow implementation** |
| spoken-help recognition | **Synthetic transcript/evidence fixture**, not recorded media |
| notification | **Stub** producing deterministic queued/delivered/acknowledged/failure fixtures; no external transport |
| camera, microphone, speakers | **Absent** |
| models, weights, datasets, voice | **Absent** |
| biometrics, enrollment, contact secrets | **Absent** |
| dream/consolidation and online learning | **Absent** |
| cloud/network | **Absent** |

## Scenario

1. Start from a versioned seed containing one creature ID and neutral drives.
2. Inject `care_interaction_v1` synthetic evidence with source, quality, monotonic/UTC time, privacy class, and fixture provenance.
3. Companion core appends the evidence, deterministically reduces `connection_need`, creates one episodic memory linked to the evidence, and emits `approach_acknowledge`.
4. Godot renders a two-state intent sequence using the approved subset and reports exact intent/frame completion.
5. Stop companion core at a controlled point; restart; replay and verify identical projection hash, creature ID, drive value, memory linkage, and next intent.
6. Inject a distinct `explicit_help_candidate_v1` synthetic fixture to care core.
7. Care policy creates a shadow incident, exercises confirmation timeout and accessible fallback branches, sends only to the stub, distinguishes delivered from acknowledged, and closes only under a defined terminal fixture.
8. Kill/restart Godot, model-stub, companion core, care core, and notification stub one at a time; verify required degradation and recovery.

## Acceptance thresholds

### Correctness and authority

- 100% of a fixed golden sequence produces byte-stable canonical event payloads after normalization and identical projection hashes across 100 replay runs.
- Creature ID/epoch, evidence link, memory version, drive values, and incident sequence are identical before/after 100 controlled restarts.
- 0 unauthorized cross-store writes across capability tests; filesystem and IPC peer-negative tests all reject.
- 100% duplicate command/evidence/notification messages with identical idempotency keys create no duplicate domain event or incident transition.
- 100% unsupported schema-major, stale evidence, malformed fixture, unknown producer, or missing authority class is rejected and audited.
- Synthetic dream/model data cannot satisfy a factual-memory promotion test; companion output cannot trigger care policy in any negative test.
- Delivered and acknowledged states are distinct in every incident trace.

### Latency

Measured on the accepted host under the defined slice workload, after warmup:

- synthetic input accepted/rejected p95 ≤ 50 ms and p99 ≤ 100 ms;
- deterministic organism-to-intent p95 ≤ 100 ms and p99 ≤ 200 ms;
- Godot intent receipt-to-first-frame p95 ≤ 100 ms; no main-thread stall > 50 ms during the 30-minute run;
- care fixture-to-shadow-incident persistence p95 ≤ 100 ms and p99 ≤ 250 ms;
- crash detection plus visible degraded state ≤ 2 s; stateful core recovery to readiness ≤ 5 s for the bounded fixture store.

These are slice gates, not final speech/safety latency claims.

### Resource/endurance

- Define baseline and test with all slice processes active for 30 minutes.
- No unbounded queue/store/log growth; each bounded queue reaches neither silent drop nor deadlock.
- RSS growth from minute 10 to 30 ≤ 5% or ≤ 50 MiB, whichever is larger, with no monotonic leak signature.
- CPU/GPU/memory/storage measurements are recorded per process; no final workload-capacity inference is permitted.
- 1,000 deterministic interaction cycles complete with zero crash, deadlock, schema error, or projection mismatch.

### Privacy and network

- Network namespace/egress observation shows zero outbound connections.
- Repository, logs, fixtures, and test artifacts contain no username, hostname, hardware serial, credential, real contact, raw media, real transcript, biometric, or autobiographical content.
- Runtime data is local XDG storage, never SSHFS; runtime sockets are mode 0700 directory and unauthorized peer tests fail.
- Logs pass a sensitive-payload scanner and contain only fixture IDs, classifications, state transitions, and timing.

### Window/visual behavior

- Starts on the adopted output in a documented initial size; remains usable at proposed minimum and maximum sizes; aspect/scaling rule produces no clipping or identity distortion.
- Placement restores after normal restart; display removal/geometry-change test selects documented safe fallback; focus/input never traps the desktop.
- Approved anatomy counts/silhouette and MON_FRAME_V1 root alignment pass automated metadata checks and Architect visual review.

### Fault injection/recovery

- Kill -9 each process at every durable boundary; restart yields either exact prior commit or exact full commit, never a partial transition.
- Corrupt copied test stores and incompatible schema fixtures fail closed without modifying the only preserved copy.
- Disk-full/read-only, socket unavailable, queue full, clock step, stale monotonic timestamp, renderer loss, care loss, and stub timeout all produce the specified visible/auditable degraded states.
- Backup taken through the selected consistent mechanism restores into a fresh local directory with matching manifest, event count, projection hash, creature ID, memory linkage, policy version, and incident trace.

## Completion evidence

- Exact source/release SHA and toolchain lock; verified Godot 4.7.2 artifact identity.
- Machine-readable test report with all seeds, fixtures, schemas, versions, timings, resource series, and result hashes.
- Golden replay, 100 restart traces, 1,000-cycle endurance report, fault matrix, network observation, privacy scan, backup/restore equivalence, and window/display evidence.
- SBOM plus separately enumerated model/data/voice/asset/service BOM fields (empty surfaces explicitly recorded), license review, build provenance, migration manifest, and signed checksums.
- Screenshots/media are allowed only if a later test directive explicitly authorizes privacy-safe capture; otherwise Architect visual inspection is recorded without captured household media.
- Independent Architect acceptance. Code existence or a passing narrow test does not open Phase 02 or establish product capability.

## Entry gates

Architecture adoption; Phase 01 authorization; exact Godot 4.7.2 acquisition approval; runtime/dependency shortlist approval; privacy-safe fixture approval; local-state directory decision; test thresholds accepted; and separate authority for the minimal approved sprite subset. None is granted here.
