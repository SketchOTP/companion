# Authority Project-State Index

## Canonical project

- Canonical project: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- End goal: https://app.notion.com/p/3d5833cb27ff81b09c20e2b52d537e1e
- Roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Visual bible: https://app.notion.com/p/3d5833cb27ff8108a3acf202fc268b6d
- Sprite contract: https://app.notion.com/p/3d5833cb27ff81989d95f604112e25ba
- Repository: https://github.com/SketchOTP/companion

## Current pointers

- Active roadmap phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase acceptance: `NOT GRANTED`
- Active directive: `COMPANION-P02-EMBODIMENT-001-R03`
- Reviewed task head: `4a111435381ff2d364cd705edbb1d65da46ea886`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_03.md`
- Notion review: https://app.notion.com/p/3d8833cb27ff812f8102dbc79891053e
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
- Foundation technology qualification: `.agent/tasks/completed/COMPANION-P00-QUAL-001/`
- Roadmap Phase 01 engineering foundation: `.agent/tasks/completed/COMPANION-P01-FOUNDATION-001/`
- Phase 01 merge: `fc31717bba8c4833736d1792d7a5fe1c6cca4900`

## Review 03 boundary

Retained:

- exact approved references and verified hashes;
- final-tree removal of prior generated bulk outputs;
- deterministic generation infrastructure;
- focused Phase 02 and inherited Phase 01 workflow success;
- initial facing/time separation design.

Rejected as proof:

- `MON_BODY_SOURCE_V1` production-body status;
- authoring-method comparison;
- 26 articulated temporal drawings;
- gait/contact and orientation behavior;
- rendered root/contact validation;
- schema/Rust/generated-track/Godot equivalence;
- 24 Hz timing correctness;
- current headless playback proof;
- operator-review readiness.

## R03 required package

1. `MON_BODY_SOURCE_V2` as a complete editable Godot-native layered body with explicit anatomy, pivots, source traceability, and neutral front/profile/front-left masters.
2. Genuinely articulated front-left idle, eight-phase walk, front↔front-left orientation pair, and listen→acknowledge reaction.
3. Exact contract alignment across schema, Rust, generated track data, fixtures, and Godot.
4. Explicit 24 FPS and integer 1/24-second relative duration weights.
5. Source- or render-derived root, contact, orientation, and anatomy evidence with tamper negatives.
6. Normal-speed and quarter-speed motion artifacts, frame strips, silhouette playback, root/contact playback, and event logs.
7. Focused CI that exercises the actual tracks, fails on unexpected Godot errors, and keeps inherited Phase 01 CI green.
8. Operator and Architect review before full-library or all-direction expansion.

## Authoring decision

Use existing Godot 4.7.2 layered 2D source nodes, bounded Skeleton2D/Bone2D deformation, AnimationPlayer timing, and discrete replacement drawings where identity-critical deformation requires them. Bake deterministic `MON_FRAME_V1` raster frames. Runtime remains raster sprite-frame based.

## Artifact and environment boundary

Keep source, manifests, validators, hashes, and selected review derivatives in Git. Keep bulk frame and pack output in workflow/local artifacts. The final Openbox endurance gate remains deferred until the editable body and motion proof are approved.

## Capability boundary

The branch is useful source-transfer and CI progress plus negative evidence. No production embodiment, continuous aliveness, or Phase 03+ capability is accepted.
