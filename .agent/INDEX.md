# Authority Project-State Index

## Canonical project

- Canonical project:
  https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- End goal:
  https://app.notion.com/p/3d5833cb27ff81b09c20e2b52d537e1e
- Roadmap:
  https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Architecture v1.0:
  https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- R04 embodiment research:
  https://app.notion.com/p/3d5833cb27ff81d79680f362491287a7
- R10 sprite contract:
  https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Repository:
  https://github.com/SketchOTP/companion

## Current pointers

- Active roadmap phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase acceptance: `NOT GRANTED`
- Active directive: `COMPANION-P02-EMBODIMENT-001-R04`
- Reviewed task head: `1183795843f26de6b69f0a2a0828ee288f32e415`
- Review 04 merge: `928ba4b8e52b8cadb9c8861ad066d2d8a91366a4`
- R04 implementation head: `7a79ddf9400a0d7cacd781d418fffdc625ec3c57`
- Active directive: `COMPANION-P02-EMBODIMENT-001-R04-C01`
- Reviewed task head: `ee2e47595271777bfbb253a6639c6ebac7198a1b`
- Repository review:
  `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_05.md`
- Notion review:
  https://app.notion.com/p/3d8833cb27ff81588285f477678ad3d3
- Phase 02 directive:
  https://app.notion.com/p/3d8833cb27ff810e858acd029ac0ea05
- Phase 02 report:
  https://app.notion.com/p/3d8833cb27ff817d9d01d754ec852c10
- Pull request: `#9 — DRAFT / OPEN / UNMERGED`
- GitHub issue: `#8 — OPEN`
- Required branch: `codex/p02-embodiment-001`
- Required worktree: local ext4/NVMe secondary worktree
- Phase 03 and later: `CLOSED`

## Completed gates

- Canonical ingest:
  `.agent/tasks/completed/COMPANION-P00-INGEST-001/`
- Linux environment evidence:
  `.agent/tasks/completed/COMPANION-P00-ENV-001/`
- Architecture v1.0:
  `.agent/tasks/completed/COMPANION-P00-ARCH-001/`
- Foundation qualification:
  `.agent/tasks/completed/COMPANION-P00-QUAL-001/`
- Roadmap Phase 01 foundation:
  `.agent/tasks/completed/COMPANION-P01-FOUNDATION-001/`
- Phase 01 merge:
  `fc31717bba8c4833736d1792d7a5fe1c6cca4900`

## Review 05 retained boundary

Retain as bounded evidence:

- exact approved references and hashes;
- synthetic source-byte preservation and content-addressed copies;
- approval-state enforcement;
- generated-pack Rust consumption and missing-path rejection;
- 24 Hz relative-duration configuration;
- synthetic missing/corrupt/restored-track behavior;
- green Phase 01 and Phase 02 workflows;
- R04 artifact `10285933356` and digest
  `sha256:071348be8021b5dddb45f4fda068e27effbd9cb3d145a6a505ab2b98b8458516`.

Do not accept:

- `READY_FOR_ARCHITECT_FRAME_PACK`;
- combined source and ingested pack authority;
- orientation or occluded-landmark support;
- complete R10 landmark support;
- atomic production intake;
- exact PNG profile enforcement;
- complete runtime pack integrity;
- physical first-frame presentation;
- exact event/timing behavior;
- Phase 02.

## Decisive blocker

The current schema assigns one facing to a whole track and forces all filenames
to use that facing, while the requested orientation clips change facing over
time. It also requires concrete coordinates for landmarks that can be occluded.
The Architect cannot supply a truthful conforming pack until R04-C01 corrects
those semantics.

## Adopted contract split

- `MON_AUTHORED_FRAME_SOURCE_PACK_V1` — immutable Architect input.
- `MON_INGESTED_FRAME_PACK_V1` — validated derived runtime/build authority.
- `MON_FRAME_INTAKE_RECEIPT_V1` — validation and atomic-publication evidence.

Runtime relationships and content addresses are never written back into the
Architect source manifest.

## R04-C01 required package

1. Source/ingested/receipt schema split.
2. Track entry/exit facing plus per-frame facing/posture/action phase.
3. Explicit visible/occluded/not-applicable landmark states and complete R10
   landmarks.
4. Bounded request-profile completeness enforcement.
5. Unique IDs/files/assets and explicit reuse/hold semantics.
6. Direct PNG IHDR, bit-depth, color-type, sRGB, alpha, transparency, and safety
   validation.
7. Fresh staged atomic intake.
8. Pack/track/reference/path/relationship integrity in Godot.
9. Render-commit observation rather than physical-presentation overclaim.
10. Exact event tick/frame consistency and expanded tamper cases.
11. Actual ingested-pack Rust validation and green Phase 01/Phase 02 CI.
12. Final status `READY_FOR_ARCHITECT_FRAME_PACK`.

## Authority boundary

Identity-critical sprite pixels and temporal key poses are authored by the AI
Architect and approved by the operator. Codex owns byte-preserving intake,
contracts, build derivatives, packaging, Godot integration, CI, and evidence.
Codex may create only unmistakably synthetic non-product fixtures.

## Protected-work rule

Do not modify, inspect for evidence, commit, reset, stash, overwrite, or reformat
the operator-owned primary-worktree `.gitignore` or `AGENTS.md` changes.

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
