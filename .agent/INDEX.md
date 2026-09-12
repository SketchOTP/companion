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
- Active directive: `COMPANION-P02-EMBODIMENT-001-R04-C04`
- Reviewed task head: `4263ae7cc085475e9b80f1c00615639ebbba679b`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_08.md`
- Notion review: https://app.notion.com/p/3d9833cb27ff81f5a5e6f29d53888e48
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

## Review 08 retained boundary

Retain as bounded engineering evidence:

- complete C02 authored-frame synthetic pack and intake/runtime contract evidence;
- canonical C03 Godot runner and log classifier;
- exact historical ALSA diagnostic capture;
- explicit Dummy-audio qualification;
- cold/warm Godot qualification;
- fail-closed application-error policy;
- always-upload diagnostics;
- exact final-head Phase 02 workflow `34671402258`: SUCCESS;
- exact final-head Phase 02 artifact `10290394916`, digest `sha256:d396c2213bfa68da0927380b85ea1bee499fd0dac95a10eacc1f90049a1b68d3`.

Do not accept yet:

- `READY_FOR_ARCHITECT_FRAME_PACK` on the final task head;
- the inherited Phase 01 readiness regression gate as deterministic;
- Phase 02.

## Decisive blocker

Final task head `4263ae7...` triggered Phase 01 run `34671402263`, which failed in `foundation_runtime_check.py` with the supervisor resident and all expected roles present but `observed_ready=false` and `care_coverage=degraded`.

The readiness probe waits for the control socket and then samples health once. Socket creation is not equivalent to completed child startup. The health API already exposes explicit readiness state; the check must wait for stable ready/healthy child state and synthetic care coverage.

## R04-C04 required package

1. Replace one-shot startup sampling with monotonic readiness polling.
2. Require all expected roles present, ready and healthy, plus `care_coverage=synthetic`.
3. Require two consecutive complete-ready observations.
4. Retain a bounded sanitized startup trace.
5. Fail on timeout or supervisor early exit.
6. Add delayed-ready, never-ready and early-exit synthetic tests.
7. Run complete local Phase 01 verification.
8. Obtain one exact-head hosted Phase 01 success plus two same-head rerun successes.
9. Keep exact-head Phase 02 green.
10. Return `READY_FOR_ARCHITECT_FRAME_PACK` only after all above pass.

## Authority boundary

Identity-critical sprite pixels and temporal key poses are authored by the AI Architect and approved by the operator. Codex owns contracts, immutable intake, deterministic derivatives, Godot integration, CI, and evidence. No procedural production character art is permitted.

## Protected-work rule

Do not modify, inspect for evidence, commit, reset, stash, overwrite, or reformat the operator-owned primary-worktree `.gitignore` or `AGENTS.md` changes.

## Capability boundary

No production frame pack, accepted construction, approved motion language, production embodiment, visual aliveness, or Phase 03+ capability is established.
