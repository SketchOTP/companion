# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. Architecture v1.0 is adopted. `COMPANION-P00-QUAL-001` is continued under Architect Review 03 for one narrow evidence-binding correction. Roadmap Phase 01, dependency adoption, and ordinary product implementation remain closed.

## Current objective

Bind the final-hardening qualification evidence to exact provenance and observed runner outcomes without broadening scope:

1. Recompute and validate committed result-file and fixture hashes.
2. Correct timestamp precision and record exact `canonicalize@5.0.0` source identity.
3. Add a reproducible results-regeneration procedure.
4. Make IPC pass fields observed, explicitly code-inspected, or removed; assert every required runtime outcome.
5. Align JCS/toolchain claims with exact executed results.
6. Tie SQLite overlap and fault conclusions to explicit before/after state and exact count relations.
7. Reconcile PR #5, Notion, Issue #4, and Authority records without adopting a dependency or opening Phase 01.

## Active directive

- Directive: `COMPANION-P00-QUAL-001`
- Status: `ARCHITECT REVIEW 03 — NARROW EVIDENCE-BINDING CORRECTION REQUIRED`
- Original verified pre-directive baseline: `4cfb0d5d62cd85737f88cd151d250ccf292a7e6d`
- Task-packet publication: `f8fc3149fcf039d2cec468aa8c3a37acdaf620d9`
- Reviewed final-hardening head: `fd6f4752ed4fed33c79bbcf8d1da2475724c40ba`
- Architect Review 01 commit: `9ea7cdbb824a9d5be88181a4374df7a4e593fbbe`
- Architect Review 02 commit: `0cce392a3706f26530d0bccf00d095c444b18279`
- Architect Review 03 repository authority: `.agent/tasks/active/COMPANION-P00-QUAL-001/ARCHITECT_REVIEW_03.md`
- Architect Review 03 Notion authority: https://app.notion.com/p/3d6833cb27ff81b38ea9e132d31888ab
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

## Evidence retained by Architect Review 03

- Weak same-UID pathname injection: accepted evidence of insufficiency.
- Actual multi-process `SOCK_SEQPACKET`, kernel-credential, pidfd, generation, capability, restart, replay, and revocation observations: retained as bounded candidate evidence.
- Python/Rust/oracle bounded profile and release-build timing/resource observations: retained; language remains unselected.
- SQLite identity, overlap, migration, restore, page-limit, and narrow `xSync` observations: retained as bounded candidate evidence; database remains unselected.
- Godot 4.7.2 artifact and transient systemd-user evidence: previously accepted and must not be rerun without a material change.

## Narrow correction boundary

Qualification-only source and sanitized result records may remain under `experiments/p00-foundation-qual/`. Generated binaries, toolchains, downloaded artifacts, databases, WAL files, secrets, private paths, and raw machine-specific data remain outside Git.

No Rust, IPC mechanism, SQLite, systemd supervisor, canonicalization package, Godot dependency, or other dependency is adopted. No product module, Godot project, media path, biometric, notification, live safety behavior, Phase 01 transition, security certification, reliability claim, or product-capability claim is authorized.

## Canonical counts at Architect Review 03

- Architecture decisions: `45` total — `27 Adopted`, `16 Interim`, `2 Rejected`.
- Research evidence: `55` total.

Counts are snapshots. Codex must query live Notion before publication.

## Next review point

Codex merges current `origin/main` normally into the existing `codex/p00-qual-001` branch, performs only the evidence-binding correction defined by `ARCHITECT_REVIEW_03.md`, updates draft PR #5, Notion, and Issue #4, leaves the PR and issue open, and stops for independent Architect review.
