# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 18 partially accepts R06-C05. Retain the frozen R05 production selection, controller-owned `MonRoot` authority, true left/right profile selection, immutable source identity, nominal Godot translated playback, and exact-head hosted regression. C05 is not accepted as a complete locomotion primitive because intent replay/cancellation is not implemented end to end, runtime 24 Hz scheduling is simulated by `process_frame`, animation phase/rate is not coupled to commanded velocity, quarter-speed is only trace metadata, and the mid-loop interruption case can resume cruise.

Current authority:

- Architect Review 18: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_18.md`
- Notion Review 18: https://app.notion.com/p/3db833cb27ff81748624fa3ed8132b8d
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06`
- Reviewed C05 implementation head: `24b4919a48eeef49fbcbb9305b9f2ad66639b3bd`
- Reviewed C05 publication head: `3f8846c761ecc46e7cf2f5e3d94a2bbd5c6416e1`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

## Frozen visual authority

- Review ZIP SHA-256: `45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b`
- Manifest SHA-256: `d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595`
- Review HTML SHA-256: `7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2`
- R06 source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`

No new character artwork is authorized.

## Retained R06 engineering boundary

Retain:

- 58 immutable native 1254x1254 RGB runtime masters;
- 24 tracks / 283 frame slots;
- source-role separation and byte-preserving intake;
- schema/Rust typed consumption;
- atomic publication/failure cleanup;
- real-art Godot loading and source timing;
- missing/corrupt/ineligible failure and recovery;
- export/restore;
- strict `RenderingServer.frame_post_draw` render commitment;
- transformed-source black-field compositor sampling;
- C03/C04 raster support/contact investigations as negative evidence;
- controller-owned actor translation rather than raster-derived root motion;
- true left/right profile track mapping;
- bounded slow/nominal/fast displacement arithmetic and nominal left/right Godot translation;
- implementation SHA `24b4919a...` hosted success for R06 + Phase 01 + inherited Phase 02.

## C05 findings retained as limitations

C05 does not yet prove a production-worthy locomotion command path:

- `mon_locomotion_controller.gd` stores no monotonic intent sequence and does not reject replayed IDs;
- `cancellation_id` is not enforced;
- Godot tests submit non-UUID intent strings despite the schema/Rust UUID contract;
- the Python negative matrix hard-codes stale replay, missing track, and corrupt/ineligible results instead of exercising all through the C05 protected path;
- gait frame timing is identical at 48/96/144 px/s, so commanded velocity does not actually control presentation rate/phase;
- `quarter_speed_trace` is a copied trace label, not rendered quarter-speed playback;
- the interruption case injects one stop tick and can continue later cruise phases;
- `tick_once()` is called once per render `process_frame`, so an explicit fixed 24 Hz simulation clock independent of render cadence is not demonstrated.

## Active objective

Codex executes `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06` only:

1. fetch and normally merge current main into the existing Phase 02 branch;
2. preserve all approved pixels and C02-C05 evidence;
3. keep controller-owned `MonRoot` authority unchanged;
4. create a separately versioned locomotion-intent wire profile with UUID `intent_id` plus explicit monotonic `intent_sequence` freshness semantics;
5. reject duplicate/equal/lower replayed intents and implement active-intent cancellation semantics;
6. drive the controller from schema-valid serialized intents rather than ad-hoc invalid IDs;
7. schedule canonical movement on an explicit fixed 24 Hz clock independent of render cadence and prove render-FPS variation does not alter semantic tick count;
8. couple loop animation phase/playback rate to commanded velocity under a declared calibration while preserving commanded world displacement;
9. make mid-loop stop/cancel terminate cruise and enter the stop presentation without later cruise resumption;
10. publish actual rendered normal and quarter-speed translated playback;
11. exercise all C06 negatives through the protected implementation path rather than static result booleans;
12. retain render/compositor/Rust/intake/failure/export regressions and pass R06 + Phase 01 + inherited Phase 02 on one implementation SHA;
13. return to Architect before transition or Openbox qualification.

## Remaining Phase 02 gates

Not yet accepted:

- replay-safe fixed-step velocity-synchronized controller locomotion under C06;
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

## R06-C06 implementation in progress (2026-09-14)

Review 18 requires replay-safe V2 intents, explicit fixed 24 Hz scheduling,
velocity-linked presentation cadence, real stop/cancel semantics, and actual
normal/quarter rendered playback. C06 adds `LocomotionIntentV2`, controller
freshness/cancellation state, Godot C06 playback, semantic cadence probes, and
executable negatives. No art bytes changed; hosted C06 regression remains
pending.

### C06 hosted exact-head closeout — 2026-09-14

Implementation SHA `6ca691412b3da7efe9227191f5f34a9175883301` is green on
focused R06 `34799648248`, Phase 01 `34799648246`, and inherited Phase 02
`34799648257`; matching PR runs `34799652134`, `34799652115`, and
`34799652259` also pass. Final hosted Godot evidence has zero errors, strict
render observation, normal/quarter playback, 30/60 FPS equivalence, six
velocity cases, and 17 executable negatives. C06 is submitted for Architect
review; transition and Openbox gates remain deferred.
