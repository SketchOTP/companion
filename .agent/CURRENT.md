# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 14 accepts R06-C01 only at a bounded real-art selection/intake/playback-plumbing boundary. The frozen R05 visual package remains operator-approved and no new character art is authorized.

Current authority:

- Architect Review 14: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_14.md`
- Notion Review 14: https://app.notion.com/p/3da833cb27ff81d9b48bd3e2c64e018c
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C02`
- Reviewed task publication head: `b446e7214cd14e530556ab558dae565ceda05f07`
- Accepted tested executable head for C01: `3eb24eb25ee1e33f4c018688b739182b60521132`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

## Frozen visual authority

- Review ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- Review HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`

R05 visual generation remains closed. Diagnostics and rejected studies remain runtime-ineligible.

## Accepted C01 engineering boundary

Retain:

- `R05_PRODUCTION_VISUAL_SELECTION_V1` from final accepted non-diagnostic playback;
- 58 immutable native 1254x1254 RGB runtime masters;
- 24 tracks / 283 frame slots;
- byte-preserving source/runtime intake;
- typed schema/Rust consumption;
- atomic staged publication and failure cleanup;
- missing/corrupt/ineligible failure plumbing;
- real-art Godot loading/playback and 24 Hz duration handling;
- export/restore evidence.

## C01 corrections

C01 is not accepted as grounded spatial behavior.

- `build_r06_c01_selection.py` currently derives many anatomical landmarks from generic foreground bounding-box fractions. These are bootstrap heuristics, not grounded semantic observations.
- Walk contacts are synthetic first-half/second-half declarations rather than observed support-foot intervals.
- Hosted R06 qualified through `SubViewport.texture.get_image` fallback rather than observed `RenderingServer.frame_post_draw`; that fallback cannot emit the authoritative `first_frame_render_committed` event.
- Current black-field runtime QA samples viewport outer corners, which are outside the scaled source rectangle and therefore cannot prove the source field blends into the black habitat.
- CI provenance correction: `a2826a...` had a Phase 01 failure; `3eb24eb...` is the tested executable head where R06, Phase 01, and inherited Phase 02 PR workflows pass. `b446e721...` is documentation/evidence-only reconciliation.

## Active objective

Codex executes `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C02` only:

1. merge current main normally into the existing task branch;
2. preserve accepted image bytes, selection, role separation, and C01 integration;
3. ground runtime-consumed landmarks against the actual accepted drawings with inspectable overlay/provenance evidence;
4. derive real gait phases, support-foot identity, planted intervals, and footfall events from the accepted sequences;
5. create explicit left/right 24 Hz `MonRoot` translation plans;
6. prove composed planted-foot world slip <=2 px without hidden root teleports;
7. require observed `RenderingServer.frame_post_draw` for `first_frame_render_committed` and keep any readback-only fallback separately named;
8. sample inside the transformed source rectangle for black-field compositor QA;
9. keep Rust/Godot/failure-recovery/export-restore green;
10. pass R06 + Phase 01 + inherited Phase 02 on one final implementation SHA;
11. return to Architect before transition or endurance qualification.

No new character artwork, cutout, repaint, recolor, resampling, dependency adoption, transition campaign, Openbox endurance, PR merge, Issue closure, or Phase 03 work is authorized.

## Remaining Phase 02 gates

Not yet accepted:

- grounded real-art semantic geometry and world-contact locomotion;
- real legal-transition campaign;
- dedicated 1366x768 Openbox two-hour endurance;
- Phase 02 completion;
- organism, autobiographical memory, perception, speech, learning, dreaming, caregiving efficacy, production reliability, or Phase 03+ capability.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Do not inspect them for evidence, commit, reset, stash, overwrite, copy, or reformat them.
