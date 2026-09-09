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
