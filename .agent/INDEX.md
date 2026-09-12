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

No production embodiment, motion-language approval, continuous aliveness, or
Phase 03+ capability is accepted.

## R04 implementation pointer

- Contract: `contracts/schemas/mon-authored-frame-pack-v1.schema.json`
- Architect landing request:
  `assets/source/p02/architect-frame-request-v1/ARCHITECT_FRAME_REQUEST_V1.md`
- Intake/runtime boundary:
  `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/R04_INTAKE_RUNTIME_BOUNDARY.md`
- Evidence bundle: `experiments/p02-embodiment/results/r04/`
- Focused hosted evidence: run `34656090767`, artifact `10285600941`, digest
  `sha256:39c56c9d43968e870005065b6bebf19700791986c017496b1ea5a03e0e14ff1f`
- Bounded result after complete publication: `READY_FOR_ARCHITECT_FRAME_PACK`
No production frame pack, accepted construction, approved motion, production
embodiment, continuous aliveness, or Phase 03+ capability is established.

## R04-C01 active correction

Review 05 is the current authority. The correction implements the immutable
Architect source-pack, validated ingested-pack, and intake-receipt split with
typed track/facing/landmark semantics, request-profile completeness, direct PNG
profile validation, atomic staging/publication, and fail-closed Rust/Godot
runtime checks. Synthetic geometry is test-only; R02/R03 visual paths remain
negative evidence. Final bounded handoff status is
`READY_FOR_ARCHITECT_FRAME_PACK`; Phase 02 is not accepted and no operator
visual approval is requested.

## R04-C01 publication reconciliation — 2026-09-12

Final task head: `5d29b51e48073077abbdffad453226ce7e8cfddc`; implementation:
`04570503c957e34e2ddcf2f1ab1cb1151a352b59`. The result bundle is committed,
hash-bound, and validator-checked. No production art or Phase 02 acceptance is
claimed; Architect frame-pack input remains the next authority-owned step.

## R04-C02 execution note

The complete tuple-keyed synthetic profile is implemented and Python intake,
PNG, atomic-publication, export/restore, and negative gates pass. Required Rust
1.98.1 and exact Godot 4.7.2 render-boundary execution are unavailable in this
worktree and remain `NOT RUN`/`BLOCKED`; no readiness or Phase 02 acceptance is
claimed.

## R04-C02 exact-tool rerun

Private Rust 1.98.1 and transient official Godot 4.7.2 execution now provide
local exact-pack evidence: typed Rust round-trip, missing-path rejection,
Godot frame-post-draw render observation, exact event/timing sequence,
corruption/degradation/recovery, and the 19-case intake matrix pass. The
committed bundle is regenerated and independently validated; hosted CI and
publication remain the final checks before the bounded readiness handoff.

## R04-C03 diagnostic-parity investigation

Review 07 is merged normally into the task branch. One canonical Godot runner
(`experiments/p02-embodiment/scripts/run_godot_qualification.py`) is used by
the direct workflow gate, `run_r04_evidence.py`, and local reproduction. It
captures Godot stdout/stderr/`--log-file` plus separate `xvfb-run -e` output,
hashes each channel, retains exact `ERROR:` lines, records import/cold/warm
cache digests, and fails closed on any application error. Classifier negatives
pass locally and the C02 semantic validator passes against canonical local
results. The superseded hosted run did not retain its exact error; hosted
cold/warm and stability rerun remain required before readiness.

## R04-C03 completion

One canonical Godot runner now defines local, evidence, and direct-CI
diagnostics. It records separate stdout/stderr/engine/Xvfb logs, exact error
lines, hashes, cache state, and semantic output, and explicitly selects
`--audio-driver Dummy` to avoid the hosted ALSA fallback diagnostic. Hosted
Phase 02 run `34670472778`, its stability rerun, and Phase 01 rerun
`34670472829` are green. Artifacts `10290328716` and `10290383849` are
published. Status is `READY_FOR_ARCHITECT_FRAME_PACK` for bounded synthetic
evidence only; Phase 02 remains unaccepted.
