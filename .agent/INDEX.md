# Authority Project-State Index

## Project identity

- Project: Living Companion & Caretaking Core; public product name provisional
- Canonical Notion: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- Complete end goal: https://app.notion.com/p/3d5833cb27ff81b09c20e2b52d537e1e
- Master roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Governance contract: https://app.notion.com/p/3d5833cb27ff81e2b3b2eabc70f9f6b3
- Adopted Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Qualification acceptance: https://app.notion.com/p/3d6833cb27ff819fabc2e5c9cb443aae
- Approved mon design: https://app.notion.com/p/3d5833cb27ff8108a3acf202fc268b6d
- Sprite production contract: https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Open decisions: https://app.notion.com/p/3d5833cb27ff81118ac8e4139ce1c873
- GitHub: https://github.com/SketchOTP/companion

## Current pointers

- Active roadmap phase: `01 — Environment and Engineering Foundation`
- Phase acceptance: `NOT GRANTED`
- Active directive: `COMPANION-P01-FOUNDATION-001`
- Current continuation: `ARCHITECT REVIEW 01 — COMPLETE THE ACTUAL RESIDENT FOUNDATION`
- Notion directive: https://app.notion.com/p/3d7833cb27ff815ebe3ed1999f05beba
- Required Notion report: https://app.notion.com/p/3d7833cb27ff81c5b0eee3e6c98b54b5
- Notion Architect Review 01: https://app.notion.com/p/3d7833cb27ff81b58987ca15fda7c0f1
- GitHub Issue #6: https://github.com/SketchOTP/companion/issues/6
- Pull request #7: https://github.com/SketchOTP/companion/pull/7
- Active task packet: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/`
- Full original directive: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/CODEX_FULL_DIRECTIVE.md`
- Current review authority: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/ARCHITECT_REVIEW_01.md`
- Required task branch: `codex/p01-foundation-001`
- Required clean secondary worktree: `YES`
- Required publication: `CONTINUE EXISTING DRAFT/UNMERGED PR #7`
- Original Phase 01 routing baseline: `4171a02385b67f3e8d7ecbd6349d45c0bf1e0a8e`
- Reviewed candidate head: `9d9e897d8fe6d74b0f4c3aedceab5761c55cc9be`
- Architecture v1.0: `ADOPTED`
- Phase 02 and later: `CLOSED`
- Product capability: `NOT ESTABLISHED`

## Completed gates

- Canonical ingest: `.agent/tasks/completed/COMPANION-P00-INGEST-001/`
- Linux environment evidence: `.agent/tasks/completed/COMPANION-P00-ENV-001/`
- Architecture v1.0: `.agent/tasks/completed/COMPANION-P00-ARCH-001/`
- Foundation qualification: `.agent/tasks/completed/COMPANION-P00-QUAL-001/`
- Qualification PR #5: merged at `80dab0c1942e4a799328a957331381104b892945`
- Qualification Issue #4: closed as completed

## Architect Review 01 disposition

Retained:

- modular Rust workspace and exact Rust/Godot/SQLite identities;
- initial schemas, canonicalization, migrations, XDG guard, role targets, supervisor entry point, Godot shell, scripts, docs, and basic CI;
- protected-work handling and bounded window observation.

Not accepted:

- one-shot supervisor and repeated-invocation soak;
- descriptor/capability ownership and direct-care durability;
- subprocess/PATH-selected SQLite persistence;
- incomplete XDG, contract, Godot, health, CI, SBOM, bootstrap, and provenance behavior;
- synthetic category-count matrix and partial failure/recovery matrix.

## Mandatory Codex continuation startup

Codex cannot see the operator–Architect conversation. Do not infer hidden decisions.

1. Inspect the protected primary SSHFS worktree read-only without reading modified root `.gitignore` or `AGENTS.md` contents into evidence.
2. Fetch current `origin/main` and `origin/codex/p01-foundation-001`.
3. Continue only in the existing clean local-ext4/NVMe secondary worktree.
4. Merge current `origin/main` normally into the task branch. Do not rebase, reset, rewrite, or force-push.
5. Read root and nested `AGENTS.md`, `.agents/skills/authority/SKILL.md`, `.agent/PROJECT_GOAL.md`, `.agent/PROJECT_PROFILE.md`, `.agent/CURRENT.md`, `.agent/ARCHITECTURE_V1.md`, this index, and every active packet file.
6. Read `ARCHITECT_REVIEW_01.md` completely.
7. Fetch the live Notion Architect review, directive, report, canonical project, roadmap, Architecture v1.0, live ADR/evidence databases, PR #7, and Issue #6 with all comments.
8. Preserve useful current source and completed Phase 00 evidence. Do not restart the repository or repeat unaffected work.
9. Complete every workstream in the Architect review within the same PR. Use coherent subsystem commits but do not return after each internal checkpoint.
10. Update Notion, PR #7, Issue #6, task records, and Authority state; leave the PR and issue open; stop for independent review.

## Required Phase 01 completion package

- continuously resident supervisor with readiness, health, restart/backoff, crash-loop, signal, and orphan behavior;
- exact descriptor ownership, private capability delivery, live-generation binding, persistent care receipts/idempotency, and actual same-user attack tests;
- exact SQLite 3.53.4 Rust binding/FFI, committed migrations, prepared statements, integrity, checkpoint, backup, and restore;
- specification-correct fail-closed XDG placement and mount/symlink/permission tests;
- all nine schemas with matching Rust types, real Draft 2020-12 validation, positive/negative fixtures, canonical vectors, and drift checks;
- real Godot bridge handshake, selected-screen placement, geometry persistence, reconnect, and safe display-loss fallback;
- supervisor-backed health, correct boot/monotonic/sequence logging, and runtime no-network observation;
- deterministic clean-clone artifact bootstrap, release CI, vulnerability/license checks, complete SBOM, provenance, and artifact retention;
- at least 3,000 actual messages through one resident foundation across retained seeds;
- complete failure/recovery matrix;
- one continuously resident 60-minute target-host soak with controlled child, producer, care, and Godot failures.

## Adopted Phase 01 technology direction

- Rust 1.98.1 authoritative service foundations.
- Exact Godot 4.7.2 Linux x86_64 artifact.
- Exact SQLite 3.53.4 development baseline, one writer per isolated local-WAL store.
- Project-owned Rust supervisor.
- Private sequenced-packet direct-care channel with kernel credentials, pidfd/generation, and rotated capability material.
- JSON Schema Draft 2020-12 and `JCS-RFC8785-v1` bounded canonical event profile.
- XDG-aligned local storage and default-deny outbound network.

## Protected-work rule

The operator-owned primary-worktree changes are outside every Codex task unless separately authorized. Do not commit, discard, reset, overwrite, stash, reformat, read into evidence, or reinterpret them.

## Scope boundary

No real organism, memory, learning, dreaming, production sprite body, camera/microphone capture, STT/TTS, model inference, biometrics, real contacts, notification delivery, spoken-help recognition, live escalation, medical capability, security certification, production reliability, SLA, or Phase 02–10 capability may be added or claimed.

## Historical ledgers

- `DIRECTIVES.md` — issued directives and acceptance boundaries
- `OUTCOMES.md` — results and evidence
- `LEARNINGS.md` — durable verified learnings
- `RECORD.md` — decisions, milestones and reversals
- `REPO_MAP.md` — repository structure and ownership
- `EXTERNAL.md` — external sources and dispositions

`CURRENT.md` is mutable. Historical ledgers are append-only after adoption.
