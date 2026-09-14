# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

## Latest Architect disposition

Architect Review 20 `CONTINUE — C06-C01 PARTIAL ACCEPTED`.

Retain the C06-C01 wire-range correction, one paused/manual presentation clock, authored-duration frame selection, real non-black translated Godot captures, replay/cancellation/fixed-step controller behavior, negative-evidence categorization, frozen source identity, and prior intake/Rust/render/compositor/failure/export boundaries.

Do not authorize legal-transition qualification yet.

Independent review of hosted artifact `10344096459` identified four remaining evidence defects:

1. Review 19 required quarter review at 4x review wall-time, but CI was weakened to accept `>=3.0x`; the exact artifact measures only about `3.17–3.18x`.
2. The submitted timing values do not match the exact hosted artifact even though the downloaded ZIP SHA-256 matches the submitted digest.
3. The shared phase verifier validates controller `animation_phase` based on hard-coded `AUTHORED_PROFILE_LOOP_TICKS := 32.0`, not phase independently derived from the loaded track's `duration_ticks`.
4. Capture records omit required source/timing identity fields, and the required actual-capture strip/GIF is absent.

Current authority:

- Architect Review 20: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_20.md`
- Notion Review 20: https://app.notion.com/p/3db833cb27ff81b4a078f4ab04a54b90
- Current Codex directive: `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C02`
- Reviewed C06-C01 implementation: `de9d7c041cad3c28ecb2779e5afc11f1f2a0f3a4`
- Reviewed C06-C01 publication head: `84b1fcb12a89538a20f52efc1cc594173ab513e7`
- Hosted C06-C01 artifact: `10344096459`, digest `sha256:961f32864633d5ab45f121430d294bae538dc626c1abcac97488f333403b438f`
- Frozen visual task head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- Frozen R06 source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`
- PR #9: draft/open/unmerged
- Issue #8: open
- Branch: `codex/p02-embodiment-001`

No new character artwork is authorized.

## Active objective

Execute `COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C02` only:

1. normally merge current `origin/main` and preserve all accepted work/history;
2. restore real 4.0x review pacing using monotonic, deadline-based timing; hosted quarter/normal ratio must be `3.90..4.10` for left and right;
3. derive presentation loop ticks and phase from the loaded selected track's actual `duration_ticks`, with independent pack-backed verification rather than a duplicated controller constant;
4. bind every required capture to semantic tick, actor position, selected track/frame, authored tick, track-derived phase, monotonic review elapsed time, source pack/frame hashes, and capture hash;
5. preserve exact semantic equality between normal and quarter review checkpoints;
6. assemble strip/GIF only from actual Godot checkpoint PNGs;
7. add regression proving a 3.33x timing ratio fails validation;
8. reconcile the inaccurate C06-C01 reported timing values to the preserved hosted artifact;
9. keep focused R06 + Phase 01 + inherited Phase 02 green on one implementation SHA;
10. return to Architect before transition/Openbox qualification.

## Remaining Phase 02 gates

After C06-C02 passes without a new material defect: Architect decision on legal-transition campaign; then dedicated 1366x768 Openbox two-hour endurance; then final Phase 02 acceptance/PR merge decision.

Organism state, autobiographical memory, perception, speech, learning, development, dreaming, caregiving efficacy, production reliability, and Phase 03+ remain unaccepted.

## R06-C06-C01 hosted closeout — 2026-09-14

Implementation SHA `de9d7c041cad3c28ecb2779e5afc11f1f2a0f3a4` passed focused
R06 `34835566609`, Phase 01 `34835566661`, and inherited Phase 02
`34835566591`; PR-triggered equivalents `34835572145`, `34835572191`, and
`34835572178` also passed. Artifact `10344096459` digest is
`sha256:961f32864633d5ab45f121430d294bae538dc626c1abcac97488f333403b438f`.
The workflow-only capture-path defect from `34835193580` was fixed in
`de9d7c0`; publication reconciliation `657c11e` is documentation-only.

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

### C06-C02 evidence correction — 2026-09-14

The active C06-C02 correction uses monotonic deadline pacing, pack-derived
track timing/phase, source/capture hash enrichment, and capture-only review
media. Local Godot 4.7.2 ratios are left `3.95565x` and right `3.95612x`;
the prior C06-C01 timing values remain preserved as superseded history. No
source PNG changed. Focused R06, Phase 01, and inherited Phase 02 hosted
regressions remain required on the final implementation SHA.
