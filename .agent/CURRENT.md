# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 17 accepts the R06-C04 stop but replans locomotion authority. The frozen R05 opaque walk sprites remain operator-approved and unchanged. C03/C04 prove that extracting canonical world travel from independent raster foot contours is not a sound authority model for this in-place seed; canonical movement is now controller-owned and sprite locomotion is presentation synchronized to typed movement intent.

Current authority:

- Architect Review 17: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_17.md`
- Notion Review 17: https://app.notion.com/p/3da833cb27ff812e96c5d76a0d8af37e
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C05`
- Reviewed C04 publication head: `340afd893f96013e3fdc8480514bf0bbb1d087f0`
- C04 implementation/evidence head: `368876873d5fab5cbcd4de9f7f3b3d7dd30d379e`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

## Frozen visual authority

- Review ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- Review HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`

No new character artwork is authorized.

## Retained R06 engineering boundary

Retain:

- 58 immutable native 1254x1254 RGB runtime masters;
- 24 tracks / 283 frame slots;
- source-role separation and byte-preserving intake;
- schema/Rust typed consumption;
- atomic publication/failure cleanup;
- real-art Godot loading and 24 Hz timing;
- missing/corrupt/ineligible failure and recovery;
- export/restore;
- strict `RenderingServer.frame_post_draw` render commitment;
- separately named viewport readback evidence;
- transformed-source black-field compositor sampling;
- C03/C04 support/contact investigations as preserved negative evidence.

## Locomotion authority correction

For this exact frozen R05 opaque in-place raster seed:

- canonical `MonRoot` position/velocity is owned by a typed movement/controller path, not derived from sprite pixels;
- Godot applies movement as a presentation adapter;
- left/right intent selects the corresponding true-profile locomotion tracks;
- animation playback rate/phase may be calibrated to commanded velocity;
- foot-contact and foot-skate measurements are diagnostic presentation evidence;
- the earlier `<=2 px` single-point foot-lock rule is superseded as a Phase-02 acceptance gate for this R05 seed, but remains applicable to future assets that explicitly author root/contact semantics.

This does not permit wrong-direction motion, loop recentering, actor-position discontinuities, source mutation, or false physical-grounding claims.

## Active objective

Codex executes `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C05` only:

1. fetch and normally merge current main;
2. preserve all approved pixels and C02/C03/C04 evidence;
3. add a versioned synthetic locomotion-intent contract with intent identity, direction/facing, commanded velocity, movement state, and cancellation/interruption identity;
4. make canonical `MonRoot` translation follow that typed intent at 24 Hz;
5. select true left/right profile start/loop/stop tracks with no front-left fallback;
6. calibrate gait playback phase/rate to commanded velocity without allowing sprite geometry to redefine commanded travel;
7. qualify start -> loop -> loop -> stop at nominal/slower/faster synthetic velocities and mid-loop interruption;
8. prove cumulative actor position with no loop recenter or phase reset;
9. retain render/compositor/Rust/intake/failure/export regressions;
10. publish normal/quarter translated playback plus movement/phase/event and diagnostic contact traces;
11. pass R06 + Phase 01 + inherited Phase 02 on one implementation SHA;
12. return to Architect before transition or Openbox qualification.

## Remaining Phase 02 gates

Not yet accepted:

- controller-driven locomotion presentation qualification under C05;
- real legal-transition campaign;
- dedicated 1366x768 Openbox two-hour endurance;
- Phase 02 completion;
- organism, autobiographical memory, perception, speech, learning, dreaming, caregiving efficacy, production reliability, or Phase 03+ capability.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Do not inspect them for evidence, commit, reset, stash, overwrite, copy, or reformat them.
