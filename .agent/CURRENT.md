# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 15 partially accepts R06-C02. Retain the frozen R05 production selection, immutable intake/Rust/Godot plumbing, strict `RenderingServer.frame_post_draw` render commitment, transformed-source compositor QA, and measured sole-candidate geometry. World-grounded locomotion is not yet accepted.

Current authority:

- Architect Review 15: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_15.md`
- Notion Review 15: https://app.notion.com/p/3da833cb27ff810384e9cddc94c4839b
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C03`
- Reviewed implementation head: `94b59cf76fc046abe28d6dd1b67359a803af8544`
- Reviewed publication head: `70afeddeddbcb56fa0580b336c82e494f0f02f3b`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

## Frozen visual authority

- Review ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- Review HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`

No new character artwork is authorized.

## Retained C02 engineering boundary

Retain:

- 58 immutable native 1254x1254 RGB runtime masters;
- 24 tracks / 283 frame slots;
- source-role separation and byte-preserving intake;
- schema/Rust typed consumption;
- atomic publication/failure cleanup;
- real-art Godot loading and 24 Hz timing;
- missing/corrupt/ineligible failure and recovery;
- export/restore;
- strict `RenderingServer.frame_post_draw` for `first_frame_render_committed`;
- separately named viewport readback evidence;
- black-field compositor sampling inside the transformed source rectangle;
- measured sole candidates and overlay provenance.

## Remaining R06 defect

Current support spans are label-driven and include only `contact`/`down` frames. Passing/up drawings can still show a grounded sole while the evidence declares no support. The validator checks only declared spans, so the `0.0 px` planted-slip result does not test omitted stance. `root_plan()` mathematically pins the chosen contact, and `stitched_sequence()` offsets each next track to force zero boundary jump; those values therefore do not independently establish meaningful lateral travel. Current stitched plans show only very small net displacement.

## Active objective

Codex executes `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C03` only:

1. merge current main normally into the existing task branch;
2. preserve all accepted C02 source/render/compositor/intake/Rust/Godot work;
3. classify support/swing state for every locomotion frame from visible evidence, not labels alone;
4. include full evidence-supported stance from touchdown/contact through release/toe-off, including passing/up when a sole remains grounded;
5. derive left/right actor-root travel from real support handoffs without an invented stride distance;
6. prove successive touchdown ordering progresses in the intended screen direction;
7. qualify start → loop → loop → stop and prove the second loop accumulates travel rather than recentering;
8. retain <=2 px composed planted-contact slip and no hidden root reset/teleport;
9. add negatives for omitted support, reversed touchdown ordering, zero-net loop travel, loop recenter/reset, excess slip, and hidden teleport;
10. publish normal/quarter composed translation playback and exact-head R06 + Phase 01 + inherited Phase 02 CI;
11. return to Architect before transition/endurance work.

If the frozen accepted drawings cannot support a truthful alternating support model and cumulative directional travel, stop and return the exact contradictory frame/coordinate evidence. Do not change pixels or weaken evidence.

## Remaining Phase 02 gates

Not yet accepted:

- complete world-grounded locomotion semantics;
- real legal-transition campaign;
- dedicated 1366x768 Openbox two-hour endurance;
- Phase 02 completion;
- organism, autobiographical memory, perception, speech, learning, dreaming, caregiving efficacy, production reliability, or Phase 03+ capability.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Do not inspect them for evidence, commit, reset, stash, overwrite, copy, or reformat them.

## R06-C02 hosted closeout (2026-09-13)

Implementation head `94b59cf76fc046abe28d6dd1b67359a803af8544` passed the R06
workflow `34767677664`, inherited Phase 02 workflow `34767677668`, and Phase 01
workflow `34767677707` on the same exact SHA. The strict Godot result observed
`RenderingServer.frame_post_draw` with 624 transformed source-field samples,
168 semantic events, zero Godot ERROR lines, and one retained V-Sync warning.
R06-C02 is submitted for Architect review. Phase 02 remains active and
unaccepted; transition and Openbox qualification remain unrun.
