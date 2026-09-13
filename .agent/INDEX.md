# Authority Project-State Index

## Canonical project

- Project: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- Roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Repository: https://github.com/SketchOTP/companion

## Current pointers

- Active phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase 02 acceptance: `NOT GRANTED`
- Current disposition: `C04 STOP ACCEPTED — CONTROLLER-DRIVEN LOCOMOTION REPLAN ACTIVE`
- Current directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C05`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_17.md`
- Notion Review 17: https://app.notion.com/p/3da833cb27ff812e96c5d76a0d8af37e
- Reviewed C04 publication head: `340afd893f96013e3fdc8480514bf0bbb1d087f0`
- C04 implementation/evidence head: `368876873d5fab5cbcd4de9f7f3b3d7dd30d379e`
- Frozen visual head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`
- Phase 03+: closed

## R06-C02 hosted closeout

Implementation head `94b59cf76fc046abe28d6dd1b67359a803af8544` passed R06
workflow `34767677664`, inherited Phase 02 workflow `34767677668`, and Phase 01
workflow `34767677707` on the same exact SHA. Strict Godot evidence recorded
`RenderingServer.frame_post_draw`, 624 compositor samples, and 168 events with
zero Godot ERROR lines. Phase 02 remains unaccepted pending Architect review.

## Frozen visual package

- ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`

R05 sprite generation remains visually accepted/frozen. No new art is authorized.

## Retained R06 boundary

- 58 immutable RGB runtime masters;
- 24 tracks / 283 frame slots;
- exact byte preservation and source-role exclusion;
- atomic staged intake and typed Rust consumption;
- real-art Godot loading/playback and 24 Hz duration handling;
- strict observed `RenderingServer.frame_post_draw`;
- transformed in-source black-field compositor sampling;
- failure/recovery and export/restore;
- C03/C04 root/contact investigations retained as negative evidence.

## Architect Review 17 ruling

The R05 opaque walk assets are in-place raster presentation, not an authored root-motion source. Canonical `MonRoot` position/velocity therefore belongs to a typed controller/movement path. Godot applies that state and synchronizes animation presentation to it. Sprite foot contours may inform gait calibration and diagnostic foot-skate evidence but may not own canonical world movement.

The previous `<=2 px` single-point planted-foot gate is superseded for this exact R05 opaque in-place seed. It remains valid for future assets with explicit authored root/contact semantics. Wrong-direction movement, loop recentering, actor-position discontinuity and source mutation remain prohibited.

## R06-C05 gate

Required:

- preserve all accepted pixels and C02/C03/C04 evidence;
- add a typed synthetic locomotion-intent contract;
- drive canonical `MonRoot` translation at 24 Hz from that intent;
- select full-profile left/right locomotion from requested direction;
- calibrate animation phase/playback rate to movement speed without letting art redefine commanded displacement;
- qualify nominal/slower/faster left/right travel plus mid-loop stop/interruption;
- prove cumulative repeated-loop translation with no recenter or phase reset;
- retain strict render/compositor/Rust/intake/failure/export behavior;
- fail wrong direction, sign mismatch, recenter/reset, phase reset, movement-tick loss/duplication, stale intent and wrong/missing track;
- publish translated normal/quarter playback and diagnostic contact/foot-skate traces;
- pass R06 + Phase 01 + inherited Phase 02 on one implementation SHA.

## Remaining after R06

- legal transition campaign over the accepted embodiment graph;
- dedicated 1366x768 Openbox two-hour endurance;
- final Phase 02 acceptance and PR merge decision.

## R06-C03 disposition

C03 support investigation is BLOCKED on the frozen drawings: contour-derived
touchdown anchors reverse the requested travel (left `+135.5,+72.0` repeating;
right `-118.0,-134.5` repeating). Per-frame support evidence and seven
executable negatives are committed under `experiments/p02-embodiment/results/r06-c03/`.
No image bytes changed. Await Architect decision; do not proceed to transition
qualification or endurance.

## R06-C04 runtime-transform result — 2026-09-13

`COMPANION_P02_R06_C04_RUNTIME_TRANSFORM_LOCOMOTION_V1` is BLOCKED. Actual
Godot centered-sprite transform and persistent near/far correspondence produce
alternating opposite-direction touchdown anchors and zero two-loop net travel
for both left and right. Full per-frame/world-contact evidence, side-by-side
C03 comparison, and nine independent passing-baseline negatives are stored in
`experiments/p02-embodiment/results/r06-c04/`. No source PNGs changed.

## R06-C05 controller-driven locomotion — 2026-09-13

The C05 controller-owned movement correction is implemented on
`codex/p02-embodiment-001`. The exact frozen pack remains byte-identical
(`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`). Six
left/right start→loop→loop→stop runs at -48/-96/-144 and +48/+96/+144 px/s
pass with cumulative travel, no actor reset, and no phase reset. The typed
intent contract, actual Godot test, and 13 independent negative cases are
documented in `experiments/p02-embodiment/results/r06-c05/R06_C05_RESULT.md`.
Local schema/contract and Godot checks pass; hosted exact-head regressions are
required before Architect review. Phase 02 remains unaccepted.
