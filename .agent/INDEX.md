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
- Current disposition: `R05-V1 REJECTED — PROFILE LOCOMOTION REPLAN ACTIVE`
- Current directive: `COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-002`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_11.md`
- Notion Review 11: https://app.notion.com/p/3d9833cb27ff818c89ebe1aca70cf28b
- Reviewed task head: `e529d8db3d76af6239c7c4856c49553fb4097979`
- Pull request: `#9 — DRAFT / OPEN / UNMERGED`
- GitHub issue: `#8 — OPEN`
- Required branch: `codex/p02-embodiment-001`
- Required worktree: clean local ext4/NVMe secondary worktree
- Phase 03 and later: `CLOSED`

## Accepted foundations

- Roadmap Phase 00 governance/environment/architecture/qualification gates
- Roadmap Phase 01 engineering foundation
- Phase 02 pre-art intake/runtime/readiness engineering
- Operator authorization for Codex candidate-art creation under Review 10
- Review-timing and completion-aware preview correction
- Photoroom RGBA cutout adapter as bounded offline authoring tooling

## Visual evidence status

Rejected:

- complete R05-v1 candidate pack;
- universal front-left idle/walk/listen presentation;
- eight-drawing twitch gait;
- head-shake turns;
- rapid bob/flick acknowledgement;
- green-edge-contaminated cutouts;
- all replacement motion studies through task head `e529d8db...`.

No replacement pack is accepted.

## Adopted motion model

- ordinary rest/social presence: `front`;
- travel screen-left: full `left` profile;
- travel screen-right: full `right` profile;
- whole-body turns: explicit quarter/back progressions;
- all eight neutral construction facings required;
- unsupported facing/action combinations fail or route through authored connectors;
- left/right production art reviewed independently; no blind mirror acceptance.

## Locomotion grounding

Source root remains `(512,896)` with no encoded screen translation. Stationary planted contacts use source-space drift. Translating locomotion uses composed world-space grounding:

```text
world_contact = actor_root_world + scale * (source_contact - source_root)
```

Declared planted world-contact drift is limited to 2 px. The new review harness must pair source tracks with a 24 Hz actor translation plan.

## Next bounded profile

`phase02_presence_lateral_motion_proof_v2`

Required proof:

- eight neutral construction facings;
- 16–24 drawing front breathe, complete inhale/exhale;
- 16–24 drawing front listen/acknowledge with hold and settle;
- left profile: turn out, start, 16–24 drawing two-step walk loop, stop, return turn;
- independently authored right profile equivalent;
- normal and quarter-speed complete-action review;
- gait-labeled strips, silhouette, edge-composite, source-contact and world-contact overlays;
- actual source/ingested/receipt, Rust, Godot and CI validation.

Historical `phase02_bounded_motion_proof_v1` remains regression evidence and must not be weakened or relabeled.

## Authority boundary

- Operator: final visual acceptance authority.
- AI Architect: strategic direction, evidence review and Phase 02 acceptance authority.
- Codex/image-generation tooling: authorized to create candidate art, but may not self-approve it.
- Godot: nonauthoritative presentation/runtime adapter.

## Explicit boundary

Phase 02 remains unaccepted. No production embodiment, visual aliveness, autonomous organism, autobiographical memory, perception, speech, learning, dreaming, caregiving efficacy, target endurance, reliability or Phase 03+ capability is established.

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` changes remain protected.
