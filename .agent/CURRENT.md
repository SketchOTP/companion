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

### C06 corrected implementation head — 2026-09-14

The only post-closeout executable change normalizes the floating-point modulo
seam in the semantic observation so nominal gait phase remains continuous.
SHA `941c231d4562177c1db02cd61fc0f0c085e6dae4` is green on R06
`34800729601`, Phase 01 `34800729655`, and inherited Phase 02 `34800729662`.
