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
- Active directive: `COMPANION-P01-FOUNDATION-001`
- Notion directive: https://app.notion.com/p/3d7833cb27ff815ebe3ed1999f05beba
- Required Notion report: https://app.notion.com/p/3d7833cb27ff81c5b0eee3e6c98b54b5
- GitHub Issue #6: https://github.com/SketchOTP/companion/issues/6
- Active task packet: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/`
- Full execution directive: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/CODEX_FULL_DIRECTIVE.md`
- Required task branch: `codex/p01-foundation-001`
- Required clean secondary worktree: `YES`
- Required publication: `ONE UNMERGED PULL REQUEST TO MAIN`
- Accepted Phase 00 baseline: `80dab0c1942e4a799328a957331381104b892945`
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

## Mandatory Codex startup

Codex cannot see the operator–Architect conversation. Do not infer hidden decisions.

1. Inspect the primary SSHFS worktree read-only without reading the modified contents of root `.gitignore` or `AGENTS.md` into evidence.
2. Preserve those operator-owned changes exactly. Do not commit, discard, reset, overwrite, stash, reformat or reinterpret them.
3. Fetch current `origin/main` and inspect every commit after the accepted baseline recorded by the active directive.
4. Create a clean local-ext4/NVMe secondary worktree and branch `codex/p01-foundation-001`.
5. Read root and nested `AGENTS.md`, `.agents/skills/authority/SKILL.md`, `.agent/PROJECT_GOAL.md`, `.agent/PROJECT_PROFILE.md`, `.agent/CURRENT.md`, `.agent/ARCHITECTURE_V1.md`, this index, and every file in the active packet.
6. Fetch every exact Notion authority named in `CODEX_FULL_DIRECTIVE.md`, query the live ADR and evidence databases, read merged PR #5 and closed Issue #4, and read Issue #6 with all comments.
7. Complete `AUTHORITY_CONTEXT_ACKNOWLEDGMENT.md` with `ADEQUATE` retrieval confidence before implementation.
8. Research current official sources before locking exact crates, actions, artifacts or implementation patterns.
9. Execute the full phase while feasible. Do not stop at internal checkpoints.
10. Open one pull request, update Notion and Issue #6, leave both open, and stop for Architect review.

## Adopted Phase 01 direction

- Rust 1.98.1 authoritative service foundations.
- Exact Godot 4.7.2 Linux x86_64 artifact.
- Exact SQLite 3.53.4 development baseline, one writer per isolated local-WAL store.
- Project-owned Rust supervisor.
- Private sequenced-packet direct-care channel with kernel credentials, pidfd/generation and rotated capability material.
- JSON Schema Draft 2020-12 and `JCS-RFC8785-v1` bounded canonical event profile.
- XDG-aligned local storage and default-deny outbound network.

## Phase 01 output contract

The run must produce a clean-clone buildable foundation with:

- modular Rust workspace and Godot project shell;
- locked dependencies and reproducible artifact bootstrap;
- schemas, Rust types, canonical vectors and negative tests;
- XDG path and forbidden-storage enforcement;
- six process shells and bounded lifecycle supervisor;
- direct synthetic safety transport independent of `companion-core`;
- separate companion, care and vault development stores;
- operator health command and payload-minimized logs;
- bounded resizable Godot habitat with headless and target-window tests;
- CI, SBOM, license and provenance artifacts;
- 1,000 deterministic cycles and 60-minute target-host soak.

## Protected-work rule

The operator-owned primary-worktree changes are outside every Codex task unless separately authorized. All task implementation and testing must occur in the clean secondary worktree.

## Historical ledgers

- `DIRECTIVES.md` — issued directives and acceptance boundaries
- `OUTCOMES.md` — results and evidence
- `LEARNINGS.md` — durable verified learnings
- `RECORD.md` — decisions, milestones and reversals
- `REPO_MAP.md` — repository structure and ownership
- `EXTERNAL.md` — external sources and dispositions

`CURRENT.md` is mutable. Historical ledgers are append-only after adoption.
