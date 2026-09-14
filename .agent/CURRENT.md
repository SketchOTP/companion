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

## R06-C02 hosted closeout (2026-09-13)

Implementation head `94b59cf76fc046abe28d6dd1b67359a803af8544` passed the R06
workflow `34767677664`, inherited Phase 02 workflow `34767677668`, and Phase 01
workflow `34767677707` on the same exact SHA. The strict Godot result observed
`RenderingServer.frame_post_draw` with 624 transformed source-field samples,
168 semantic events, zero Godot ERROR lines, and one retained V-Sync warning.
R06-C02 is submitted for Architect review. Phase 02 remains active and
unaccepted; transition and Openbox qualification remain unrun.

## R06-C03 result (2026-09-13)

Review 15 was merged normally and C03 was investigated without source-pixel
mutation. Every locomotion frame in the six left/right start, loop, and stop
tracks has contour-derived support evidence. The evidence-supported 24 Hz
plans show the frozen geometry advances opposite the requested direction:
left two-loop net `+255.0 px` and right two-loop net `-336.0 px`; complete
start→loop→loop→stop nets are `+415.0 px` and `-505.0 px`. The C03 validator
returns BLOCKED and all seven semantic negative tests pass. This is an exact
geometric contradiction, not a weak or omitted test. Phase 02 remains active
and unaccepted; no art was generated or modified and transition/Openbox gates
remain unrun.

## R06-C04 result (2026-09-13)

Review 16 was merged normally at `c26dcefa8fb455662f3f0b1b749b02be5eb0c9d4`.
The corrected qualifier uses the exact Godot transform (centered native 1254
anchor `(627,627)`, offset `(0,0)`, scale `0.5`, MonRoot `(320,320)`) and
persistent near/far temporal correspondence. Left repeated-loop touchdown
deltas alternate `+140.0,-174.5,+85.0,-159.5`; right alternates
`-115.0,+184.5,-143.0,+168.0`; first handoffs oppose requested travel and
planted slips reach `27.0 px` left / `18.0 px` right. Actor-root nets are
`-218.0 px` / `+189.0 px`, but complete support qualification fails. Nine
negatives reject independently from a passing baseline. Source PNG bytes remain
unchanged; C04 is BLOCKED and no transition or Openbox work followed.

## R06-C05 result (2026-09-13)

Review 17/C05 was merged normally at `eb8a1f3fcaefb4f2e445b19c09481fab9b5792c0`.
The typed synthetic locomotion intent contract and controller-owned 24 Hz
presentation path qualify six complete left/right start→loop→loop→stop runs,
three bounded velocities per side, interruption traces, explicit full-profile
track selection, and a 13-case negative matrix from an independently passing
baseline. Local Godot 4.7.2 left/right runs observe
`RenderingServer.frame_post_draw` before completion and report -352/+352 px
nominal travel with zero actor resets. Frozen source pack SHA remains
`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`; no source
PNG changed. Hosted R06, Phase 01, and inherited Phase 02 runs are pending on
the pushed implementation head. Phase 02 remains active/unaccepted; transition
and Openbox gates remain unrun.

## R06-C05 hosted closeout (2026-09-14)

Implementation SHA `24b4919a48eeef49fbcbb9305b9f2ad66639b3bd` now passes hosted
Phase 01 run `34790167116`, same-head reruns `34790169089` (job
`103813789392`) and `103814757741`, focused R06 `34790169083`, and inherited
Phase 02 `34790169074`. The test-only persistence ordering correction seeds a
known valid candidate before care restart; frozen pack SHA remains
`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40` and no
source PNG changed. Phase 02 remains active and unaccepted.
