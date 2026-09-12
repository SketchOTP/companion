# Authority Project-State Index

## Canonical project

- Canonical project: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- End goal: https://app.notion.com/p/3d5833cb27ff81b09c20e2b52d537e1e
- Roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- R04 embodiment research: https://app.notion.com/p/3d5833cb27ff81d79680f362491287a7
- R10 sprite contract: https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Repository: https://github.com/SketchOTP/companion

## Current pointers

- Active roadmap phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase acceptance: `NOT GRANTED`
- Active directive: `COMPANION-P02-EMBODIMENT-001-R04-C03`
- Reviewed task head: `1d7ea24295b505c6beb0f612a6b248a6f8d5edfb`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_07.md`
- Notion review: https://app.notion.com/p/3d9833cb27ff81109a7add09837f7b2b
- Phase 02 directive: https://app.notion.com/p/3d8833cb27ff810e858acd029ac0ea05
- Phase 02 report: https://app.notion.com/p/3d8833cb27ff817d9d01d754ec852c10
- Pull request: `#9 — DRAFT / OPEN / UNMERGED`
- GitHub issue: `#8 — OPEN`
- Required branch: `codex/p02-embodiment-001`
- Required worktree: local ext4/NVMe secondary worktree
- Phase 03 and later: `CLOSED`

## Completed gates

- Canonical ingest: `.agent/tasks/completed/COMPANION-P00-INGEST-001/`
- Linux environment evidence: `.agent/tasks/completed/COMPANION-P00-ENV-001/`
- Architecture v1.0: `.agent/tasks/completed/COMPANION-P00-ARCH-001/`
- Foundation qualification: `.agent/tasks/completed/COMPANION-P00-QUAL-001/`
- Roadmap Phase 01 foundation: `.agent/tasks/completed/COMPANION-P01-FOUNDATION-001/`
- Phase 01 merge: `fc31717bba8c4833736d1792d7a5fe1c6cca4900`

## Review 07 retained boundary

Retain as bounded engineering evidence:

- exact references and hashes;
- source/ingested/receipt contract split;
- complete positive 8-track / 31-frame bounded synthetic pack;
- request-profile, orientation, event, reuse, PNG and durable intake semantics;
- actual generated-pack Rust consumption;
- local Godot render-boundary result;
- local result validator/tamper negatives;
- hosted Phase 01 success;
- direct hosted Phase 02 Godot step success.

Do not accept:

- `READY_FOR_ARCHITECT_FRAME_PACK`;
- the hosted sanitized evidence result;
- classification of the unknown Godot `ERROR:` line;
- Phase 02.

## Decisive blocker

Hosted Phase 02 run `34667692926` passed its direct Godot gate and failed only when the evidence runner re-ran Godot and captured an `ERROR:` from application stdout/stderr. The direct gate and evidence runner use different capture policies, and the exact error line was not retained. Artifact publication is skipped on validator failure.

C03 therefore resolves diagnostic parity rather than reopening C02 semantics.

## R04-C03 required package

1. One canonical Godot runner and classification policy.
2. Separate Godot stdout/stderr/engine log and Xvfb diagnostics.
3. Exact retained Godot error lines and log hashes.
4. Cold and warm identical hosted qualification runs.
5. Evidence-based root-cause classification before runtime modification.
6. Always-published sanitized diagnostics on failure.
7. Classifier negatives proving Godot stderr errors fail and wrapper diagnostics stay separate.
8. Green Phase 01 and Phase 02 hosted CI.
9. One additional hosted rerun after green.
10. Final status `READY_FOR_ARCHITECT_FRAME_PACK` only after all above pass.

## Authority boundary

Identity-critical sprite pixels and temporal key poses are authored by the AI Architect and approved by the operator. Codex owns contracts, immutable intake, deterministic derivatives, Godot integration, CI, and evidence. No procedural production character art is permitted.

## Protected-work rule

Do not modify, inspect for evidence, commit, reset, stash, overwrite, or reformat the operator-owned primary-worktree `.gitignore` or `AGENTS.md` changes.

## Capability boundary

No production frame pack, accepted construction, approved motion language, production embodiment, visual aliveness, or Phase 03+ capability is established.
