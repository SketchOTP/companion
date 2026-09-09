# Foundation and Cross-Phase Integration Contracts

Status: `CORRECTED — PROPOSED CONTRACTS; NOT AUTHORIZED`

These are two distinct gates. Roadmap Phase 01 establishes the engineering foundation. “One remembered care loop plus shadow help” is a later cross-phase architecture-proof milestone whose prerequisites include bounded work from Phases 02, 03, 04, and 10. Neither contract is authorized by this planning document.

## Contract A — Roadmap Phase 01 engineering foundation

### Scope

Phase 01 expands the governance-only repository into a reproducible engineering workspace without claiming companion behavior:

- approved repository/module shells and authored/generated/runtime separation;
- pinned, reproducible development/build environment and exact toolchain records;
- process shells for `companion-core`, `care-core`, `identity-consent-vault`, adapters, Godot presentation, and supervision, with domain behavior absent;
- typed/versioned IPC schemas, `JCS-RFC8785-v1` canonical fixtures, digest/time profiles, peer authorization, bounded queues, and compatibility rules;
- local XDG config/data/state/cache/runtime boundaries, with canonical runtime state prohibited on SSHFS;
- structured payload-minimized logging, health/degradation reporting, and lifecycle/version inventory;
- supervisor start/stop/restart/backoff foundation without enabling live sensing, care, or external delivery;
- deterministic clock, boot epoch, seeds, fixture, fault-control, and per-run local test-root facilities;
- CI design/implementation and provenance/BOM foundations only when separately authorized;
- diagnostic device metadata surfaces that do not capture or play media.

### Acceptance

A clean clone with only approved prerequisites reproduces the environment, validates locked inputs, builds the authorized shells, runs non-hardware tests locally and in CI, starts/stops the empty process graph safely, verifies IPC/canonicalization/peer boundaries, confines all mutable test state to local XDG-like roots, reports unavailable capabilities honestly, emits rights/provenance records, and leaves no hidden network, model, data, voice, secret, biometric, contact, or personal-machine dependency.

The language/toolchain evidence gate blocks production implementation of `companion-core`, `care-core`, and `identity-consent-vault`, but it does not block language-neutral repository layout, schema/canonicalization contracts, test fixtures, XDG policy, logging/health contracts, or supervisor/CI planning. The Architect must explicitly decide which Phase 01 activities may begin and must approve the eventual language/toolchain result.

### Explicit exclusions

Phase 01 completion does not prove organism behavior, memory, production embodiment, care scenario efficacy, perception/speech, notification delivery, biometrics, identity matching, privacy/security qualification, endurance, accessibility, pilot readiness, or any product capability.

## Contract B — Cross-phase milestone: “One remembered care loop plus shadow help”

### Purpose and phase provenance

After its prerequisite gates are authorized and passed, a real Godot 4.7.2 bounded window on the adopted 1366×768 Openbox display presents the approved mon responding to a deterministic synthetic encounter. The encounter changes a named homeostatic drive, creates an evidence-backed episodic memory, and produces a body-neutral intent rendered by Godot. After controlled process restart, the same individual restores the committed change and references the encounter through structured non-LLM recall.

In parallel, an authorized synthetic safety producer sends an `explicit_help_candidate_v1` directly to `care-core`. Care durably records the safety-input receipt in its own append-only journal, traverses deterministic shadow policy, and exercises stub acknowledgment without a real notification or companion-state mutation. The producer may also send a separately addressed ordinary-observation copy to `companion-core`; both cite the same immutable source ID/digest, but neither store is shared.

The milestone combines bounded work from:

| Roadmap phase | Bounded contribution |
|---|---|
| Phase 02 — Mon body, habitat, and sprite pipeline | exact Godot body adapter, approved minimal authored sprite subset, bounded-window behavior |
| Phase 03 — Organism kernel and autonomous life | deterministic two-drive organism subset and body-neutral intents |
| Phase 04 — Evidence, world model, and persistent memory | ordinary-evidence event, episodic memory, replay, restart, and restore |
| Phase 10 — Caretaking core foundation | direct safety ingress, care-owned receipt/incident journals, signed policy, shadow-only incident flow |

Passing the milestone completes none of Phases 02, 03, 04, or 10. Early bounded `care-core` work retires the architecture-blocking risk that companion failure could control safety ingress; it does not bypass Phase 10’s full scenario, consent, accessibility, false/missed-event, contact, and operational qualification.

### Real, simulated, stubbed, absent

| Surface | Milestone treatment |
|---|---|
| Godot 4.7.2 build and bounded window | **Real**, exact verified build; adopted display |
| Approved mon identity | **Real authored test sprite subset** only after separate asset authority; must pass visual bible/MON_FRAME_V1 |
| `companion-core` event/memory store | **Real minimal implementation** |
| organism | **Real deterministic two-drive subset** with explicit arbitration |
| ordinary world/evidence | **Synthetic fixture**, schema-valid and clearly marked |
| recall | **Real structured retrieval**, no LLM |
| direct safety producer→care path | **Real IPC/receipt path** driven by an authorized synthetic producer; no media/model |
| `care-core` safety-input/policy/incident journals | **Real minimal deterministic shadow implementation**, independent of companion database |
| `identity-consent-vault` | **Real contract stub only**; reports `test_only`, exposes no secrets/biometrics/contacts, denies every live capability |
| spoken-help recognition | **Synthetic safety-candidate fixture**, not recorded media |
| notification | **Stub** producing deterministic queued/delivered/acknowledged/failure fixtures; no external transport |
| camera, microphone, speakers | **Absent** |
| models, weights, datasets, voice | **Absent** |
| biometrics, enrollment, real contacts/secrets/keys | **Absent** |
| dream/consolidation and online learning | **Absent** |
| cloud/network | **Absent** |

### Scenario

1. Start from a versioned seed containing one creature ID and neutral drives; assign a test `boot_id` and owner sequences.
2. Inject `care_interaction_v1` as an ordinary synthetic observation with source, quality, boot-scoped monotonic time, UTC observation/uncertainty, privacy class, and fixture provenance.
3. Companion core appends the ordinary evidence, deterministically reduces `connection_need`, creates one episodic memory linked to the evidence, and emits `approach_acknowledge`.
4. Godot renders a two-state intent sequence using the approved subset and reports exact intent/frame completion.
5. Stop companion core at controlled durable boundaries; restart; replay and verify identical canonical event bytes/digests, projection hash, creature ID, drive value, memory linkage, and next intent across same- and new-boot cases.
6. Through an independently authorized synthetic producer, send `explicit_help_candidate_v1` directly to care. Care authenticates the producer, validates schema/canonical bytes/digest/freshness/quality/replay indicators, then appends its own accepted or rejected receipt before policy evaluation.
7. Care policy creates a shadow incident, exercises confirmation timeout and accessible fallback branches, sends only to the stub, distinguishes delivered from acknowledged, and closes only under a defined terminal fixture.
8. Stop `companion-core`; redeliver a new valid safety candidate; prove care receipt/transition and recovery without companion IPC or database access.
9. Kill/restart Godot, producer stub, companion core, care core, vault stub, and notification stub one at a time; verify explicit degradation and recovery.

## Provisional minimum engineering evidence floors

These floors are early defect-finding gates, not statistical reliability, safety, endurance, availability, or production-SLA evidence.

| Floor | Intended to detect | Cannot establish |
|---|---|---|
| 100 replay/restart cases | deterministic reconstruction errors, non-idempotent commands, boundary-specific torn state, boot/time ordering defects | real crash frequency, hardware/power-loss reliability, long-history correctness, or operational availability |
| 1,000 deterministic interaction cycles | short-loop leaks, queue/store growth, schema drift, projection divergence, deadlocks under bounded synthetic load | realistic human/media distribution, statistical failure rate, product lifetime, or safety efficacy |
| 30 minutes continuous integrated execution | immediate resource growth, startup/warmup instability, adapter stalls, renderer/IPC liveness defects | 24-hour or multi-day endurance, thermal/noise acceptability, maintenance burden, or production SLA |

The suite must span multiple retained deterministic seeds, low/high drive and state boundaries, empty/nonempty/restored stores, multiple supported schema versions plus invalid/unsupported messages, kill points before/during/after durable commits, replay from multiple persisted states, same-boot and cross-boot time cases, and property/randomized tests whose failing and passing seeds are retained. Repeating one golden sequence does not satisfy a floor.

Later gates must explicitly escalate to 24-hour and multi-day soak, target-media qualification, shadow-safety false/missed-event measurement, accessibility testing with the intended population, controlled pilot evidence, and operational/update/recovery observation. None of those later gates is implied by the initial counts.

## Milestone acceptance

### Correctness, canonicalization, and authority

- Every golden event matches pinned `JCS-RFC8785-v1` UTF-8 bytes and `sha-256-jcs-event-v1` digest; duplicate keys, invalid Unicode, NaN/Infinity, out-of-range/noncanonical numbers, altered digest/signature scope, and unsupported schema major are rejected before authority logic.
- Creature ID/epoch, evidence link, memory version, fixed-point drive values, and incident sequence are identical before/after the diversified replay/restart matrix; owner sequence and causation determine cross-boot ordering while UTC steps do not reorder history.
- Zero unauthorized cross-store writes; filesystem, socket-peer, producer-capability, vault-capability, and schema-negative tests all reject.
- Duplicated ordinary or safety messages are idempotent. Duplicate safety candidates create at most one logical safety input and one corresponding transition, with care-owned duplicate receipts/reasons retained.
- Delivered and acknowledged states remain distinct in every incident trace.

### Independent safety ingress negatives

- A stopped `companion-core` cannot block producer→care delivery, durable receipt, policy processing, or care recovery.
- A syntactically valid or forged companion message cannot create a safety receipt or incident because companion peer identity is not an allowed safety producer.
- Mood, memory, language/model output, dream material, animation, and Godot status cannot produce, authorize, modify, delay, or suppress a care transition.
- Removing sensor/speech producer health creates explicit degraded safety coverage, never false normality.
- Care start, processing, restart, replay, and backup tests run with the companion database path absent and fail if any access is attempted.

### Latency and resources

Measured on the accepted host under the defined milestone workload, after warmup:

- synthetic input accepted/rejected p95 ≤ 50 ms and p99 ≤ 100 ms;
- deterministic organism-to-intent p95 ≤ 100 ms and p99 ≤ 200 ms;
- Godot intent receipt-to-first-frame p95 ≤ 100 ms; no main-thread stall > 50 ms during the 30-minute provisional run;
- direct safety fixture-to-durable receipt and shadow-incident persistence p95 ≤ 100 ms and p99 ≤ 250 ms;
- crash detection plus visible degraded state ≤ 2 s; stateful core recovery to readiness ≤ 5 s for bounded fixture stores;
- no unbounded queue/store/log growth; RSS growth from minute 10 to 30 ≤ 5% or ≤ 50 MiB, whichever is larger, without a monotonic leak signature.

These are milestone engineering gates, not speech, safety, endurance, or production latency/capacity promises.

### Privacy, network, visual, and recovery

- Egress observation shows zero outbound connections. Logs/fixtures/artifacts contain no private machine identifiers, credentials, real contacts, raw media, real transcripts, biometrics, or autobiographical content.
- Runtime/test data stays in local XDG-like storage, never SSHFS; unauthorized socket peers and vault calls fail.
- Window placement/scaling/focus/display fallback and approved anatomy/MON_FRAME_V1 metadata pass; captured media remains prohibited unless separately authorized.
- Kill every process before, during, and after each durable boundary. Recovery yields exact prior or full commits, never partial transitions.
- Corrupt copied stores and incompatible schemas fail closed. Disk-full/read-only, queue full, clock step, reboot, renderer loss, producer loss, care loss, vault loss, and stub timeout all produce typed visible/auditable degradation.
- A consistent backup restores into a fresh local directory with matching manifest, event counts/digests, projections, identity, memory linkage, policy version, safety receipts, and incident trace.

## Required completion evidence

- Exact source/release SHAs and toolchain locks; verified Godot 4.7.2 artifact identity; exact eligible SQLite build record if selected.
- Machine-readable test report with every seed, fixture, schema/canonicalization/digest version, boot ID, persisted starting state, kill point, timing/resource series, and result hash.
- Provisional 100-case replay/restart matrix, 1,000-cycle report, 30-minute report, property/randomized seed ledger, authority/fault matrix, egress/privacy scans, backup/restore equivalence, and window/display evidence.
- BOM/provenance/rights records with empty model/data/voice/asset/service surfaces explicitly stated.
- Independent Architect acceptance. Code existence or a narrow pass does not complete a roadmap phase or establish product capability.

## Milestone entry gates

Architecture v1.0 adoption; successful Phase 01 foundation gate; separate bounded authorization for the Phase 02/03/04/10 contributions; language/toolchain decision; exact Godot 4.7.2 and dependency approvals; exact persistence approval; privacy-safe fixtures; local-state policy; test thresholds; and separate minimal sprite authority. None is granted here.
