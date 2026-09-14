# Authority Project-State Index

## Canonical project

- Project: https://app.notion.com/p/3d5833cb27ff8196814fdbae282f15ad
- Roadmap: https://app.notion.com/p/3d5833cb27ff81dd88faeb0c95b6f44e
- Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Repository: https://github.com/SketchOTP/companion

## Current pointers

- Active phase: `02 — Mon Body, Habitat, and Sprite Pipeline`
- Phase 02 acceptance: `NOT GRANTED`
- Current disposition: `R06-C06 PARTIAL ACCEPTED — C06-C01 RENDER/TIMING/WIRE CLOSEOUT ACTIVE`
- Current directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C01`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_19.md`
- Notion Review 19: https://app.notion.com/p/3db833cb27ff81a8a722ccf78da68de0
- Reviewed implementation head: `941c231d4562177c1db02cd61fc0f0c085e6dae4`
- Reviewed publication head: `1adadc1206be4371b9baa42aa21153d6eeae74fd`
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

## Frozen package

- Review ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Review manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- Review HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`
- R06 source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`

No new character artwork is authorized.

## Retained accepted boundary

- 58 immutable RGB runtime masters; 24 tracks / 283 frame slots;
- exact byte preservation, atomic intake, typed Rust consumption;
- strict `RenderingServer.frame_post_draw` and black-field compositor QA;
- missing/corrupt/ineligible failure/recovery and export/restore;
- controller-owned `MonRoot` and true left/right profile mapping;
- V2 UUID identity, monotonic replay rejection, active-intent cancellation;
- fixed-step accumulator evidence and exact-head C06 hosted regression;
- C03/C04 root/contact failures preserved as negative evidence.

## Why C06-C01 is required

Independent Architect review found:

- all four hosted C06 normal/quarter viewport captures are identical all-black images because capture occurs before sprite playback;
- C06 both plays AnimatedSprite2D and manually overwrites `sprite.frame`, bypassing accepted `duration_ticks`; the accepted profile loop is 32 source ticks but submitted phase logic cycles in 24 ticks;
- V2 schema/Rust accepts unsigned-64 sequence values that Godot signed-64 `int` cannot represent;
- not all 17 claimed negative cases execute the Godot protected path.

## C06-C01 gate

Required:

- common exactly representable sequence wire range with max/max+1 schema/Rust/Godot tests;
- one presentation clock preserving accepted duration weights;
- loop phase derived from actual authored loop duration and verified modulo-continuous across repeats;
- visible non-black Godot captures during translated start/cruise/second-loop/stop for normal and quarter review;
- quarter review proven as same semantic path at 4x review wall-time;
- command negatives through controller, pack negatives through loader/resolver, scheduler/trace negatives through a shared positive-path verifier;
- frozen source bytes unchanged;
- R06 + Phase 01 + inherited Phase 02 green on one implementation SHA.

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

### C06 replay-safe fixed-step controller — 2026-09-14

Review 18 C06 implementation is in progress. The V2 intent contract adds UUID
identity plus monotonic sequence and cancellation targeting; the controller
owns a fixed 24 Hz semantic clock and velocity-linked presentation rate. Godot
consumes serialized V2 intents and captures normal/quarter rendered playback.
No source art changed; hosted validation is pending.

## R06-C06 hosted exact-head closeout — 2026-09-14

Exact SHA `6ca691412b3da7efe9227191f5f34a9175883301` passes focused R06
`34799648248`, Phase 01 `34799648246`, and inherited Phase 02 `34799648257`;
PR-triggered equivalents `34799652134`, `34799652115`, and `34799652259` also
pass. C06 covers replay-safe V2 intent freshness, explicit cancellation, fixed
24 Hz movement, velocity-linked presentation, actual rendered normal/quarter
playback, and 17 executable negatives. No source art changed; Phase 02 remains
unaccepted pending Architect review.

### C06 corrected implementation head — 2026-09-14

Implementation SHA `941c231d4562177c1db02cd61fc0f0c085e6dae4` records only the
modulo-phase seam normalization. Exact-head R06 `34800729601`, Phase 01
`34800729655`, and inherited Phase 02 `34800729662` passed.
