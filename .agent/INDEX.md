# Authority Project-State Index

## Canonical project

- Project: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- Roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Repository: https://github.com/SketchOTP/companion

## Current pointers

- Active phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase 02 acceptance: `NOT GRANTED`
- Current disposition: `R06-C05 PARTIAL ACCEPTED — INTENT LIFECYCLE / FIXED-STEP / PHASE COUPLING ACTIVE`
- Current directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_18.md`
- Notion Review 18: https://app.notion.com/p/3db833cb27ff81748624fa3ed8132b8d
- Reviewed implementation head: `24b4919a48eeef49fbcbb9305b9f2ad66639b3bd`
- Reviewed publication head: `3f8846c761ecc46e7cf2f5e3d94a2bbd5c6416e1`
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
- R06 source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`

R05 sprite generation remains visually accepted/frozen. No new art is authorized.

## Retained R06 boundary

- 58 immutable RGB runtime masters;
- 24 tracks / 283 frame slots;
- exact byte preservation and source-role exclusion;
- atomic staged intake and typed Rust consumption;
- real-art Godot loading/source timing;
- strict observed `RenderingServer.frame_post_draw`;
- transformed in-source black-field compositor sampling;
- missing/corrupt/ineligible failure/recovery and export/restore;
- C03/C04 raster root/contact failures retained as negative evidence;
- controller-owned `MonRoot` translation and true left/right profile mapping;
- bounded slow/nominal/fast displacement arithmetic;
- nominal Godot translated playback on actual approved art;
- exact-head hosted R06 + Phase 01 + inherited Phase 02 success on `24b4919a...`.

## C05 limitations requiring C06

C05 does not yet satisfy the accepted runtime-semantics boundary:

- no monotonic intent sequence/replay rejection is implemented in the Godot controller;
- cancellation identity is not enforced;
- Godot semantic tests use non-UUID IDs despite the schema/Rust UUID contract;
- several claimed negative cases are static result records rather than protected-path executions;
- gait frame cadence is the same at slow/nominal/fast movement speeds;
- quarter-speed is only copied trace metadata, not actual rendered playback;
- interruption can resume cruise after one zero-velocity tick;
- controller ticks are invoked from `process_frame` rather than an explicit fixed 24 Hz simulation clock.

## R06-C06 gate

Required:

- preserve all accepted source/runtime/render/intake evidence;
- version the locomotion wire contract instead of rewriting historical V1;
- use UUID intent identity plus an explicit monotonic sequence/freshness field;
- reject duplicate, stale and replayed commands in the actual controller path;
- define active-intent cancellation/stop semantics and reject mismatched/replayed cancellation;
- consume schema-valid serialized intent fixtures in Godot;
- run canonical movement on an explicit fixed 24 Hz clock independent of render cadence;
- prove render-FPS variation does not lose or duplicate semantic movement ticks;
- couple loop animation phase/rate to commanded velocity under a declared calibration;
- terminate mid-loop stop/cancel into stop presentation without cruise resumption;
- publish real rendered normal/quarter translated playback;
- execute negative cases through the protected implementation path rather than summary booleans;
- retain R06 + Phase 01 + inherited Phase 02 green on one implementation SHA.

## Remaining after R06

If C06 passes without a new material defect:

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

### C05 hosted exact-head closeout — 2026-09-14

The inherited Phase 01 persistence probe now establishes a known valid candidate
before care restart, removing a test-ordering race without changing production
behavior. Implementation SHA `24b4919a48eeef49fbcbb9305b9f2ad66639b3bd`
passed hosted Phase 01 `34790167116`, same-head reruns `34790169089` (job
`103813789392`) and `103814757741`, focused R06 `34790169083`, and inherited
Phase 02 `34790169074`. C05 remains bounded controller-owned locomotion
evidence; Phase 02 remains unaccepted.
