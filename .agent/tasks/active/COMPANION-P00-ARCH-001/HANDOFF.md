# Handoff

Status: `COMPLETE FOR INDEPENDENT ARCHITECT REVIEW`

## Recommendation

Adopt, after independent review, a local-first event-sourced modular companion core with consequence-driven isolation: `companion-core` is the single writer for creature truth; `care-core` is separately persisted and deterministically owns scenario/incident authority; sensor, model, Godot, notification, and operations processes are nonauthoritative adapters. Use versioned JSON Schema messages over private Unix sockets and local XDG storage. Shortlist a fixed SQLite build only after crash/checkpoint/backup qualification.

The credible alternative is a fully decomposed service graph. It offers narrower independent restart/scale boundaries but introduces distributed consistency, interface, supervision, mixed-version, and resource complexity unsupported by current single-host evidence.

## Proposed first slice

“One remembered care loop plus shadow help” integrates a real exact Godot 4.7.2 bounded window, a real deterministic two-drive organism subset, real append-only persistence/typed memory/restart, and a separate real minimal care policy/incident journal. Inputs are synthetic; notification is a stub; media, models, biometrics, contacts, network, voice, and dream learning are absent. Acceptance includes deterministic replay, 100 restarts, 1,000 cycles, IPC/authority negatives, fault injection, privacy/egress checks, window recovery, and backup/restore equivalence.

## Unresolved gates

- Operator: RQ-07 role/privacy/authority; RQ-08 language/voice/wake/interruption/accessibility; RQ-09 retention/deletion/export/backup promises; RQ-11 lifespan/support/key/replacement promise.
- Evidence then operator: RQ-04 cloud/compute/power/noise/cost.
- Deferred safely: RQ-10 uses only a stub until transport ruling; RQ-12 uses internal working labels until name/trademark authority.
- Experiments: exact Godot 4.7.2 supply, Vulkan/GPU, window/display, fixed persistence, service recovery, slice concurrency, camera/audio, model/resource, backup/restore, power/noise, and soak.

## Dependencies and rights

No dependency is approved. Godot 4.7.2 is operator-selected but absent/unqualified. Python and Rust/Go remain implementation comparators; JSON Schema is the recommended contract standard; SQLite is conditional on a fixed exact release and tests; systemd user services are conditional on recovery tests. Speech/perception/model/cloud/notification/vault candidates are deferred. InsightFace supplied pretrained artifacts are rejected absent exact commercial rights. BOM/provenance format candidates are CycloneDX/SPDX plus SLSA 1.2 concepts.

## Priority risks

Missed/false help, inaccessible response, biometric spoofing, private-data exposure, false memory, prompt/teaching injection, vendor shutdown, artifact rights, runtime instability, developmental leakage, update regression, and distributed authority duplication. Controls and required evidence are explicit; none is claimed effective in runtime.

## Validation and publication

`EVIDENCE.md` contains exact authority totals, sources, validation, publication addendum, changed paths, and SHAs. The dedicated Notion report and GitHub Issue #3 receive the canonical result; Issue #3 remains open. The repository publication is a normal fast-forward and final `HEAD == origin/main`.

## Acceptance boundary

- Architecture v1.0: `RECOMMENDED — NOT ADOPTED`.
- Roadmap Phase 00: `ACTIVE / INCOMPLETE`.
- Phase 01: `NOT AUTHORIZED`.
- Product implementation and capability: `NOT IMPLEMENTED / NOT ACCEPTED`.
- Architect review: `REQUIRED`.

Codex has not self-accepted the architecture, closed the issue, resolved open product decisions, or opened implementation.
