# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 19 PARTIAL ACCEPTS R06-C06. Retain the frozen R05/R06 visual source identity, controller-owned `MonRoot`, V2 replay/freshness semantics, active-intent cancellation, fixed-step accumulator, immutable intake/Rust/Godot boundaries, strict render/compositor evidence, failure/recovery/export-restore, and exact-head hosted regression at `941c231d4562177c1db02cd61fc0f0c085e6dae4`.

C06 is not yet accepted as a complete locomotion primitive because independent review found three material defects: the hosted normal/quarter viewport captures are blank pre-playback images; the Godot test both plays AnimatedSprite2D and manually overwrites `sprite.frame`, bypassing the accepted `duration_ticks` and producing a 24-tick phase cycle instead of the accepted 32-tick walk loop; and the V2 wire schema/Rust `u64` range exceeds Godot's signed-64 integer range. The claimed 17 negative cases are also not all exercised through the Godot protected path.

Current authority:

- Architect Review 19: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_19.md`
- Notion Review 19: https://app.notion.com/p/3db833cb27ff81a8a722ccf78da68de0
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C01`
- Reviewed C06 implementation head: `941c231d4562177c1db02cd61fc0f0c085e6dae4`
- Reviewed C06 publication head: `1adadc1206be4371b9baa42aa21153d6eeae74fd`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

## Frozen authority

- Review ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Review manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- Review HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`
- R06 source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`

No new character artwork is authorized.

## Retained engineering boundary

Retain 58 immutable native RGB runtime masters, 24 tracks / 283 frame slots, byte-preserving intake, typed Rust consumption, atomic publication/failure cleanup, real-art Godot loading, strict `RenderingServer.frame_post_draw`, transformed-source black-field compositor QA, missing/corrupt/ineligible failure and recovery, export/restore, controller-owned canonical lateral translation, true left/right profile selection, V2 UUID + monotonic sequence replay rejection, active cancellation targeting, and fixed-step accumulator evidence.

All C03/C04 raster-root/contact failures remain preserved negative evidence. Raster foot/contact diagnostics do not own canonical world movement for this in-place seed.

## Active objective

Execute `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C01` only:

1. merge current `origin/main` normally and preserve all historical evidence;
2. constrain V2 `intent_sequence` to a wire range exactly representable by Godot signed 64-bit integers and add max/max+1 schema/Rust/Godot tests;
3. use one presentation clock only and preserve authored frame duration weights exactly;
4. derive loop phase from the actual authored 32-tick profile loop, including modulo continuity across repeated loops;
5. capture visible non-black mon frames during real translated start/cruise/second-loop/stop playback for both normal and quarter review;
6. prove quarter review is the same semantic path at 4x review wall-time rather than a trace label;
7. reconcile negative evidence so controller, loader/resolver, scheduler, and shared trace-verifier paths are exercised truthfully;
8. keep R06 + Phase 01 + inherited Phase 02 green on one implementation SHA;
9. return to Architect before transition or Openbox qualification.

## Remaining Phase 02 gates

After C06-C01 passes without a new material defect: real legal-transition campaign, then dedicated 1366x768 Openbox two-hour endurance, then final Phase 02 acceptance/PR merge decision. Organism, autobiographical memory, perception, speech, learning, development, dreaming, caregiving efficacy, production reliability, and Phase 03+ remain unaccepted.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Do not inspect, commit, reset, stash, overwrite, copy, or reformat them.
