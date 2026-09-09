# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. Architecture v1.0 is adopted. `COMPANION-P00-QUAL-001` is continued under Architect Review 02 for one final evidence-hardening cycle. Roadmap Phase 01, dependency adoption, and ordinary product implementation remain closed.

## Current objective

Harden the corrected foundation qualification so its claims are independently reproducible and fail closed:

1. Commit sanitized machine-readable result and provenance records.
2. Add assertion-driven validation for the real multi-process direct-care IPC matrix.
3. Correct supervisor endpoint/secret ownership claims and prove expected lifecycle outcomes.
4. Complete every claimed Python/Rust/oracle behavior comparison or remove the unsupported claim.
5. Make SQLite concurrency, migration, disk-full, restore, commit-fault, and checkpoint-fault verdicts strict.
6. Reconcile PR #5, Notion, Issue #4, and task records without adopting a dependency or opening Phase 01.

## Active directive

- Directive: `COMPANION-P00-QUAL-001`
- Status: `ARCHITECT REVIEW 02 — CONTINUED FOR FINAL EVIDENCE HARDENING`
- Original verified pre-directive baseline: `4cfb0d5d62cd85737f88cd151d250ccf292a7e6d`
- Task-packet publication: `f8fc3149fcf039d2cec468aa8c3a37acdaf620d9`
- Reviewed correction head: `9be80e14e907f7973c1161bda041986e06f85a6e`
- Architect Review 01 commit: `9ea7cdbb824a9d5be88181a4374df7a4e593fbbe`
- Architect Review 02 repository authority: `.agent/tasks/active/COMPANION-P00-QUAL-001/ARCHITECT_REVIEW_02.md`
- Architect Review 02 Notion authority: https://app.notion.com/p/3d6833cb27ff8113bc7dcc42e96237f0
- Notion directive: https://app.notion.com/p/3d6833cb27ff815e90e8de161e6de185
- Required Notion report: https://app.notion.com/p/3d6833cb27ff81c7a89acb29ced1a1cc
- GitHub Issue #4: https://github.com/SketchOTP/companion/issues/4
- Pull request #5: https://github.com/SketchOTP/companion/pull/5
- Active packet: `.agent/tasks/active/COMPANION-P00-QUAL-001/`
- Required task branch: `codex/p00-qual-001`
- Required publication: existing draft/unmerged PR #5
- Acceptance authority: ChatGPT AI Architect
- Roadmap Phase 01: `CLOSED`
- Product implementation: `CLOSED`

## Adopted architecture authority

- Canonical Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Architecture acceptance review: https://app.notion.com/p/3d6833cb27ff81d88785f64d0629286c
- Repository mirror: `.agent/ARCHITECTURE_V1.md`
- Accepted architecture/archive commit: `4cfb0d5d62cd85737f88cd151d250ccf292a7e6d`
- Completed architecture packet: `.agent/tasks/completed/COMPANION-P00-ARCH-001/`
- GitHub Issue #3: closed as completed

## Protected operator work

The primary SSHFS worktree contains operator-owned uncommitted Graft changes to root `.gitignore` and `AGENTS.md`. They remain protected. Codex must continue only in the clean local-ext4/NVMe secondary worktree and must not commit, discard, reset, overwrite, stash, reformat, read into evidence, or reinterpret the protected edits.

## Evidence retained by Architect Review 02

- Weak same-UID pathname injection evidence: retained.
- Corrected real multi-process `SOCK_SEQPACKET`, kernel-credential, pidfd, generation, capability, restart, and revocation observations: retained as bounded candidate evidence.
- Python/Rust release-build timing and resource measurements: retained as provisional engineering measurements.
- Bounded oracle/profile observations: retained, but the claimed cross-language vector and service parity must be made exact.
- SQLite overlap, migration, restore, page-limit, and narrow `xSync` observations: retained as bounded candidate evidence.
- Godot 4.7.2 artifact and transient systemd-user evidence: accepted previously and need not be rerun.

## Final hardening boundary

Qualification-only source and sanitized result records may remain under `experiments/p00-foundation-qual/`. Generated binaries, toolchains, downloaded artifacts, databases, WAL files, secrets, private paths, and raw machine-specific data remain outside Git.

No Rust, IPC mechanism, SQLite, systemd supervisor, canonicalization package, Godot dependency, or other dependency is adopted. No product module, Godot project, media path, biometric, notification, live safety behavior, Phase 01 transition, security certification, reliability claim, or product-capability claim is authorized.

## Canonical counts at Architect Review 02

- Architecture decisions: `45` total.
- Research evidence: `55` total.

Counts are snapshots. Codex must query live Notion before publication.

## Next review point

Codex updates the existing `codex/p00-qual-001` branch and draft PR #5 with one focused hardening commit and at most one publication-reconciliation commit, publishes sanitized result/provenance evidence and fail-closed validation, updates Notion and Issue #4, leaves PR #5 and Issue #4 open, and stops for independent Architect review.
