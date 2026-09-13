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

- Latest joint-sheet diagnostic: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_BLACK_SEQUENCE_SHEET_RESULT.md` — two failed outputs; no completed animation.
- Exact negative source sheets/prompts: `assets/review/p02/author002/black-sequence-sheet/`.

- Latest targeted retry: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_BLACK_MOTION_RETRY_RESULT.md` —7 new trials, controlled temporal progression still fails;12 motion tracks remain incomplete.
- Retry evidence: `assets/review/p02/author002/black-motion-retry/README.md` —prompts, hashes, pixel scan and ordered comparisons; no approval request.

- Latest black-motion continuation: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_BLACK_MOTION_RESULT.md` —52 black-backed drawings /23 diagnostic sequences; conversion and bounded review playback observed, complete motion FAILED/incomplete.
- Current review evidence: `assets/review/p02/author002/black-motion-studies/README.md`; exact hashes/prompts, selected strips/GIFs and Godot result. No new visual approval requested.

- Latest operator workaround: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_BLACK_BACKDROP_RESULT.md` — Godot black backdrop and one front still preview; transparent contracts unchanged.

- Latest continuation: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_CONTINUATION_RESULT.md` — new right-key studies preserved; clean-source stage blocked by Photoroom HTTP402 and RGB-only fallback.
- Continuation hashes/results: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_CONTINUATION_RESULTS.json`.

- Latest operator decision: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_OPERATOR_APPROVAL.md` — construction sheet and latest corrected gait poses visually approved.
- Exact approved selection: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_OPERATOR_SELECTION.json` — eight facings / eleven latest keys; superseded variants excluded.

- Historical pre-approval execution result: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_KEY_GATE_RESULT.md` — coder stopped at Review11 anatomical key gate; 25 studies, zero promoted frames. Selected artwork's visual disposition is superseded by the operator decision above.
- Exact study observations/hashes: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_AUTHOR_002_STUDY_RESULTS.json`.
- Operator approval was supplied directly; complete v2 actions/intake/runtime remain NOT RUN.

- Latest movement correction: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_FACING_AND_MOTION_CORRECTION.md` — front rest, profile travel, deliberate turns; planned, not implemented.
- Latest visual disposition: **all R05-v1 previews operator-rejected**.
- Current correction/evidence: `tasks/active/COMPANION-P02-EMBODIMENT-001/R05_OPERATOR_REJECTION_01.md`.
- Replacement motion: **NOT READY**, no new visual approval request.

- Active roadmap phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase acceptance: `NOT GRANTED`
- Current disposition: `OPERATOR VISUAL SELECTION APPROVED — COMPLETE MOTION AND TECHNICAL QA REMAIN`
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
