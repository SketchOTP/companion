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

If C06-C01 passes without a new material defect: legal-transition campaign, dedicated 1366x768 Openbox two-hour endurance, then final Phase 02 acceptance/PR merge decision.
