# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. Architecture v1.0 is adopted. `COMPANION-P00-QUAL-001` is the active bounded qualification directive. Roadmap Phase 01, dependency adoption, and ordinary product implementation remain closed.

## Current objective

Produce target-host synthetic evidence and decision recommendations for the foundation technologies and trust mechanisms that could otherwise force immediate redesign:

1. Python 3.12 versus exact Rust stable for authoritative local services.
2. Process-level producer identity/capability for direct safety ingress that blocks unauthorized same-user injection.
3. Exact official Godot 4.7.2 Linux x86_64 artifact provenance and version-only verification.
4. One exact supported non-withdrawn SQLite artifact/build under WAL, crash, checkpoint, disk, migration, backup, and restore tests on local ext4/NVMe.
5. User-level supervision feasibility without changing system configuration.

## Active directive

- Directive: `COMPANION-P00-QUAL-001`
- Status: `CODEX QUALIFICATION RESULT PREPARED — PUBLICATION/INDEPENDENT REVIEW PENDING`
- Verified pre-directive baseline: `4cfb0d5d62cd85737f88cd151d250ccf292a7e6d`
- Task-packet publication: `f8fc3149fcf039d2cec468aa8c3a37acdaf620d9`
- Notion directive: https://app.notion.com/p/3d6833cb27ff815e90e8de161e6de185
- Required Notion report: https://app.notion.com/p/3d6833cb27ff81c7a89acb29ced1a1cc
- GitHub Issue #4: https://github.com/SketchOTP/companion/issues/4
- Active packet: `.agent/tasks/active/COMPANION-P00-QUAL-001/`
- Required task branch: `codex/p00-qual-001`
- Required publication: unmerged pull request to `main`
- Acceptance authority: ChatGPT AI Architect
- Roadmap Phase 01: `CLOSED`
- Product implementation: `CLOSED`

## Adopted architecture authority

- Canonical Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Architect Review 02: https://app.notion.com/p/3d6833cb27ff81d88785f64d0629286c
- Repository mirror: `.agent/ARCHITECTURE_V1.md`
- Accepted architecture/archive commit: `4cfb0d5d62cd85737f88cd151d250ccf292a7e6d`
- Completed architecture packet: `.agent/tasks/completed/COMPANION-P00-ARCH-001/`
- GitHub Issue #3: closed as completed

## Protected operator work

Codex reported user-owned uncommitted Graft changes to root `.gitignore` and `AGENTS.md` in the primary worktree. They are protected. The active directive requires a clean secondary worktree from current `origin/main` and prohibits committing, discarding, resetting, overwriting, stashing, reformatting, or interpreting those local edits.

## Qualification boundary

Qualification-only source and exact locks may be created under `experiments/p00-foundation-qual/`. Generated binaries, toolchains, Godot artifacts, database files, WALs, raw measurements, and temporary worktrees belong in private local XDG qualification/cache roots and are not committed.

The directive permits no root/system changes, permanent services, product modules, Godot project/window/renderer, production sprites, media capture/playback, personal data, biometrics, contacts, notification delivery, live safety behavior, cloud model, dependency adoption, direct main push, PR merge, Phase 01 opening, or product-capability claim.

## Canonical counts at directive publication

- Architecture decisions: `45` total — `27 Adopted`, `16 Interim`, `2 Rejected`.
- Research evidence: `53` total — `40 Grade A`, `11 Grade B`, `2 Grade C`; `40 Reviewed`, `12 Candidate`, `1 Needs Deep Review`.

Counts are snapshots. Codex must query live Notion.

## Next review point

Codex has prepared bounded qualification evidence. SQLite remains partial because deterministic commit/checkpoint kill placement requires an unauthorized intrusive fault VFS. After normal branch publication, the Architect reviews the Rust, IPC Candidate 2, Godot artifact, SQLite-blocker, and systemd-user recommendations. Architecture v1.0 remains adopted; Phase 01, dependency adoption, and product implementation remain closed.
