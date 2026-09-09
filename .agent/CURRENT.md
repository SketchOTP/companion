# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. The canonical ingest, Linux environment inventory, and Operator Decision Packet 01 are complete. `COMPANION-P00-ARCH-001` has received Architect Review 01; Codex has prepared the focused correction for publication and independent re-review. Product implementation remains closed.

## Current objective

Publish and independently review the corrected Architecture v1.0 proposal. The packet now addresses the seven review findings: independent safety-evidence ingress, explicit identity/consent/contact/secret authority, canonical event encoding and reboot-aware time, roadmap-consistent milestone placement, language/toolchain selection gate, exact SQLite eligibility, and properly labeled/diversified evidence floors.

## Active directive

- Directive: `COMPANION-P00-ARCH-001`
- Status: `CORRECTION PREPARED — CODEX RESUBMISSION / ARCHITECT REVIEW REQUIRED`
- Verified task baseline: `db33d8a597f79a01e569482dc00583dcf50249f9`
- Starting routing head for original execution: `6559cec1beaf27bf958c2b9517b0717f04c83ea9`
- Codex planning result: `5d6d87d93b017e42647e260b69d80b5ad3f8becc`
- Codex publication head reviewed: `d8c7209e0ec0370c17fc4cf980fde879e54f10b5`
- Architect review file: `.agent/tasks/active/COMPANION-P00-ARCH-001/ARCHITECT_REVIEW_01.md`
- Architect review Notion: https://app.notion.com/p/3d6833cb27ff81bd834cf3693f8ae9a5
- Parent directive: https://app.notion.com/p/3d6833cb27ff8183a210e560883d96ab
- Coder report: https://app.notion.com/p/3d6833cb27ff8141837fdaa087841324
- GitHub Issue #3: https://github.com/SketchOTP/companion/issues/3
- Active packet: `.agent/tasks/active/COMPANION-P00-ARCH-001/`
- Acceptance authority: Architect
- Architecture v1.0 adoption: `NOT GRANTED`
- Roadmap Phase 01: `CLOSED`
- Dependency approval: `NONE`
- Product implementation: `CLOSED`

## Architect review disposition

Accepted for retention:

- `ADEQUATE` source/context reconstruction.
- Current live totals and ADR-33 through ADR-37 semantics.
- Governance/planning-only scope and normal result publication.
- Local-first cohesive companion-core topology with consequence-driven edge isolation.
- Separate deterministic care authority; nonauthoritative Godot/model/sensor/notification adapters.
- Local XDG state on ext4/NVMe; no canonical state on SSHFS; no default outbound network.
- Typed/versioned local IPC, explicit degradation, owner portability, rights separation, and Kentucky/nonmedical claims boundaries.
- The remembered-interaction plus shadow-help concept as an architecture-proof milestone after correction.

Not accepted yet:

1. Safety evidence ownership/ingress is contradictory. `care-core` needs a direct authenticated producer path and its own durable safety-input journal; `companion-core` may not gate or suppress it.
2. Identity, consent, contacts, credentials, biometric handles, and key references need one explicit vault authority and degraded behavior.
3. Byte-stable JSON/hash claims need a pinned canonical event encoding, numeric rules, event-digest scope, and boot/clock epoch.
4. The cross-phase slice cannot be mislabeled as the Roadmap Phase 01 contract. Define a separate Phase 01 foundation gate and preserve phase semantics.
5. Python versus a compiled core/care candidate needs an explicit language/toolchain evidence gate before implementation.
6. SQLite eligibility must require one exact supported non-withdrawn build; a loose `3.51.3+` rule is insufficient because 3.52.0 was withdrawn.
7. The 100-restart, 1,000-cycle, and 30-minute values must be provisional engineering floors with diversified seeds/boundaries, not reliability claims.

## Codex correction disposition

- Direct safety path: independently authorized sensor/speech producer sends safety candidates directly to `care-core`; care owns accepted/rejected receipt and incident journals; companion has no safety forwarding/gating/suppression/authorization role.
- Safety negatives: companion stopped, forged companion input, duplicate candidate, producer/model outage, companion database absent, and companion mood/memory/language/dream/animation sources are explicitly covered.
- Vault: `identity-consent-vault` owns consent/revocation, biometric handles/templates, contacts/roles, provider credential handles, key references/recovery metadata, and privileged-change audit; foreign processes receive only decisions/opaque expiring capabilities.
- Canonical events: `JCS-RFC8785-v1` plus `sha-256-jcs-event-v1`, exact hash/signature scope, duplicate-key/Unicode/numeric rules, fixed-point/wide-integer rules, boot-scoped monotonic time, UTC uncertainty, owner event sequence, and causation are defined.
- Phase semantics: the Roadmap Phase 01 foundation contract is separate from the later Phase 02/03/04/10 cross-phase architecture-proof milestone; passing the milestone completes no phase.
- Toolchain: EXP-00 compares Python 3.12 with one Architect-selected Rust-or-Go comparator; no winner/install/benchmark exists; the gate blocks authoritative-service implementation rather than every language-neutral foundation task.
- SQLite: only one exact supported non-withdrawn release or documented fixed backport may be considered, with complete build/topology/security metadata and target tests.
- Evidence floors: 100 replay/restart cases, 1,000 cycles, and 30 minutes are provisional minimum engineering floors with multiple seeds/states/schemas/kill points/boots; later soak, media, shadow-safety, accessibility, pilot, and operational evidence remains separate.

This is a Codex correction claim only. Architect Review 01 remains the last acceptance authority event until independent re-review.

## Required correction behavior

1. Read `ARCHITECT_REVIEW_01.md` in full.
2. Re-fetch only mutable live authorities whose state may have changed; the accepted full ingest need not be repeated unless a source changed.
3. Check current local/remote Git state and Issue #3 before editing.
4. Update only affected planning/evidence files and append new superseding ledger entries rather than rewriting history.
5. Use current primary sources for every changed technical assertion.
6. Publish a focused correction result to Notion and Issue #3.
7. Leave Issue #3 open and stop for a new independent Architect review.

## Adopted product boundary remains unchanged

- One adult primary user aged 18 or older who may have support needs; configured trusted caregivers/contacts; no minors in iteration one.
- Consumer-product development under a narrow non-medical companion and trusted-contact assistance claim.
- Explicit spoken help request is the first caregiving scenario in Kentucky, United States; qualification begins with simulation, replay, and shadow mode.
- Existing Linux PC, existing webcam/microphone/speakers, and dedicated 1366×768 Openbox-managed display.
- Bounded resizable Godot habitat window.
- Godot 4.7.2 selected but absent; Godot 4.6 is not an approved substitute.
- Approved flat cel-shaded sprite mon and `MON_FRAME_V1` remain unchanged.

## Accepted environment limits remain unchanged

- Ubuntu 24.04.5 LTS, x86_64, X11; Ryzen 7 5800XT; approximately 67.3 GB RAM.
- GTX 1660 SUPER and RTX 3050 6 GB on NVIDIA 595.84; direct OpenGL 4.6 observed; exact Vulkan capability unknown.
- Camera/audio metadata is known; real quality, latency, contention, and integrated behavior are unqualified.
- Repository checkout is SSHFS; local ext4/NVMe is available for later runtime state.
- Godot 4.7.2 execution, service recovery, workload headroom, power, thermals, noise, and endurance remain unqualified.

## Canonical counts at Architect Review 01

- Research evidence: `46` records — `33 A`, `11 B`, `2 C`; `33 Reviewed`, `12 Candidate`, `1 Needs Deep Review`.
- Architecture decisions: `37` records — `21 Adopted`, `14 Interim`, `2 Rejected`.
- No new ADR or dependency was adopted by the review.

## Hard boundary

No product source, Godot project or execution, sprite production, dependency installation or approval, package manifest, CI workflow, deployment, database implementation, model/weight/data/voice download, media capture/playback, benchmark, biometric implementation, notification integration, safety runtime, architecture self-approval, Roadmap Phase 01, or product-capability claim is authorized.

## Next review point

Codex publishes the focused correction commit, updated Notion report/directive, and Issue #3 handoff. The Architect independently verifies the safety path, vault authority, canonical encoding/time model, phase sequencing, language gate, SQLite rule, evidence floors, traceability, scope, and repository state before any Architecture v1.0 adoption.
