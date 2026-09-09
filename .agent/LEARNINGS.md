# Durable Learnings

Historical entries are append-only after adoption.

## COMPANION-L001 — Repository bootstrap predates Authority installation

### Learning

GitHub `SketchOTP/companion` began on `main` at `b7266b5806ef0612a14d2d6b7d324841070625ac` with only `.gitignore` and an Apache-2.0 `LICENSE`; no product source existed.

### Why it matters

Future agents must preserve that history and must not infer a language, architecture, or dependency from the Python-oriented bootstrap ignore file.

### Recheck trigger

Recheck the remote and working tree at every substantial directive.

## COMPANION-L002 — Repository authorization is governance-only

### Learning

The operator explicitly authorized the named GitHub repository and Authority 3.0 setup on 2026-09-08. This supersedes the earlier "no repository exists or is authorized" status only enough to host governance; it does not satisfy or waive the Research Phase 01 implementation gates.

### Why it matters

Repository existence must not be mistaken for authorization to write product code, add dependencies, create CI, or begin experiments.

### Recheck trigger

A new operator/Architect ruling that explicitly opens an implementation, experiment, dependency, CI, or deployment gate.

## COMPANION-L003 — Prior projects are not donors

### Learning

This project is independent ground zero. Prior companion, lifeform, monitoring, and assistant projects are not predecessors, donors, baselines, constraints, or default sources of code, design, models, schemas, tests, terminology, or decisions.

### Why it matters

Reusable governance procedure may be installed from the canonical Authority package, but project substance requires fresh evidence and explicit adoption through this project's Notion decision process.

### Recheck trigger

Any proposed reuse, migration, import, or comparison to a prior project.

## COMPANION-L004 — Identifier coverage is not semantic traceability

### Learning

A document can contain every required RQ, ADR, risk, pillar, and phase identifier while still mapping those identifiers to the wrong meaning. Structural presence, counts, JSON validity, and reference closure do not prove that a relationship is substantively correct.

### Why it matters

Future architecture, risk, and requirement traceability must verify exact ID-title-status pairs and manually review whether each cited record actually supports the statement. Automated crosswalks are supporting evidence, not a substitute for source-aware review.

### Recheck trigger

Every directive that creates or materially changes requirement, decision, risk, evidence, or roadmap traceability.

## COMPANION-L005 — Environment metadata does not qualify the companion workload

### Learning

The iteration-one host exposes ample general-purpose resources and accelerated OpenGL 4.6, but labels such as CPU model, RAM amount, GPU model, VRAM, and generic Godot requirements do not prove concurrent rendering, perception, speech, memory, model, or safety performance.

### Why it matters

Architecture and model sizing must be based on bounded integrated measurements with explicit latency, resource, thermal, power, and degradation criteria. Generic specifications only preserve options.

### Recheck trigger

Every renderer, model, camera mode, audio path, process-placement, and resource-budget decision.

## COMPANION-L006 — Source, runtime state, and backup need separate storage domains

### Learning

The Git repository is on network-backed SSHFS while the host provides local ext4/NVMe storage. These have different latency, availability, locking, and failure semantics.

### Why it matters

Canonical organism state, memory, caches, audit data, and recovery material must not inherit repository-volume assumptions. Source transport, runtime persistence, model cache, export, and backup require separate explicit policies.

### Recheck trigger

Architecture v1.0 storage design, persistence selection, backup/export planning, and any environment migration.

## COMPANION-L007 — Privacy filtering must begin at collection

### Learning

A hardware serial can appear in otherwise useful camera or audio metadata before a post-processing filter runs. In `COMPANION-P00-ENV-001` the value was immediately discarded and never entered durable artifacts, but the exposure shows that redaction after broad collection is weaker than field-limited collection.

### Why it matters

Future probes and runtime telemetry should use source-level field allowlists, bounded parsers, pre-reviewed command forms, and data minimization before persistence. Post-processing redaction is a secondary defense.

### Recheck trigger

Every machine inventory, sensor diagnostic, support bundle, telemetry design, biometric flow, and privacy review.

## COMPANION-L008 — Isolate by consequence, not by conceptual noun

### Learning

The Companion requires hard process boundaries around caregiving authority, raw sensors, models, rendering, secrets, and external transports, but splitting every tightly coupled organism and memory concept into an independent service would introduce distributed state reconciliation before evidence justifies it.

### Why it matters

A cohesive transactional companion truth owner plus consequence-driven edge isolation preserves deterministic personal continuity and testability while retaining future split seams.

### Recheck trigger

Measured resource isolation, privilege, independent upgrade/restart, database contention, second-device, or multi-owner evidence that makes a further split necessary.

## COMPANION-L009 — Persistence version is a safety and continuity input

### Learning

An embedded database's broad reputation or API is insufficient. Current SQLite documentation records a rare 2026 WAL-reset corruption issue across many releases and requires a fixed exact version/backport for the proposed multi-connection WAL use.

### Why it matters

Persistence selection must capture the exact embedded library, compile options, filesystem semantics, writer topology, checkpoint behavior, and crash/backup/restore evidence. The host binding and SSHFS checkout cannot be accepted by assumption.

### Recheck trigger

Every persistence shortlist, runtime/toolchain lock, database upgrade, writer-topology change, or migration/backup design.

## COMPANION-L010 — Safety independence requires independent ingress and persistence

### Learning

A separate care process is not architecturally independent if its qualifying inputs must be validated, forwarded, queued, or persisted by the companion authority. Independence requires an authenticated producer-to-care path, a care-owned receipt journal, and explicit common-mode input degradation.

### Why it matters

Companion failure, compromise, mood, memory, generated language, dreams, animation, or database availability must be unable to suppress or manufacture a care transition. Shared source identifiers are useful for reconciliation but cannot create shared mutable truth.

### Recheck trigger

Every sensor/speech topology, care scenario, queue, IPC authorization, persistence, degradation, and integration test design.

## COMPANION-L011 — Deterministic schemas require canonical bytes and reboot epochs

### Learning

JSON Schema constrains structure but does not make JSON bytes invariant. Repeatable hashes/replay require a pinned canonical encoding/digest scope and canonical numeric rules; monotonic time also requires a boot identifier and cannot order records across reboots by itself.

### Why it matters

Cross-language serialization, Unicode/numeric edge cases, signatures, wall-clock steps, and reboot resets otherwise create divergent history despite schema-valid content. Owner sequence and causation remain the durable cross-boot order.

### Recheck trigger

Every event schema, parser/canonicalizer, hash/signature, language/toolchain, migration, replay, clock, and cross-boot test decision.

## COMPANION-L012 — Numeric version floors can admit withdrawn releases

### Learning

An eligibility rule expressed only as a minimum version can admit a later withdrawn or incompatible release. SQLite 3.52.0 demonstrates that security/correctness fixes and compatibility/support disposition must be evaluated per exact build.

### Why it matters

Persistence approval requires exact source identity, binding, compile options, support/withdrawal/vulnerability status, topology, and reproduced recovery behavior—not lexical or numeric version comparison.

### Recheck trigger

Every dependency/toolchain/runtime upgrade and every exact-build qualification record.
