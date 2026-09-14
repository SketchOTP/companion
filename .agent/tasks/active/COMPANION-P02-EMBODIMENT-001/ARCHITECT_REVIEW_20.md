# Architect Review 20 — C06-C01 Partial Accepted; C06-C02 Evidence Correction

## Verdict

`CONTINUE — C06-C01 PARTIAL ACCEPTED.`

Do **not** start the legal-transition campaign. Retain the valid C06-C01 corrections, but the submitted result does not satisfy the complete closeout boundary.

## Authority sync

- Canonical project, Architecture v1.0, Roadmap Phase 02, Review 19, GitHub PR #9, Issue #8, current `main`, publication branch, exact-head workflow records, implementation code, and hosted artifact were re-inspected.
- Current pre-review `main`: `79eada2d6b74479fabda20d4a93eb53f6798b51c`.
- Reviewed implementation: `de9d7c041cad3c28ecb2779e5afc11f1f2a0f3a4`.
- Publication head: `84b1fcb12a89538a20f52efc1cc594173ab513e7`.
- PR #9 remains draft/open/unmerged. Issue #8 remains open.
- Hosted artifact: `10344096459`; downloaded ZIP SHA-256 exactly matches submitted digest `961f32864633d5ab45f121430d294bae538dc626c1abcac97488f333403b438f`.
- Notion Review 20: https://app.notion.com/p/3db833cb27ff81b4a078f4ab04a54b90

## Accepted C06-C01 boundary

Retain:

- common V2 wire range `0..9223372036854775807`, including max/max+1/u64-max boundary handling;
- paused/manual AnimatedSprite2D presentation ownership, with no concurrent `play()` plus forced-frame authority;
- loaded authored duration weights and nominal eight-frame × four-tick = 32-tick profile loop;
- controller-owned canonical `MonRoot`, V2 replay rejection, cancellation semantics, and fixed-step movement;
- real post-`RenderingServer.frame_post_draw` left/right playback captures;
- controller-path and loader/resolver negative categorization, with Python-model evidence separately labeled;
- frozen R06 source identity and prior intake/Rust/compositor/failure/export boundaries.

Independent inspection of the 16 hosted gameplay PNGs confirms visible non-black subject pixels and monotonic translated screen position. Normal and quarter captures are pixel-identical at matched semantic checkpoints, which is valid evidence that review slowdown does not change semantic presentation state.

## Material defect 1 — unauthorized timing-gate weakening

Review 19 required quarter review to represent the same semantic checkpoints at **4× review wall-time**.

The focused workflow instead accepts:

`quarter.review_wall_time_ms >= normal.review_wall_time_ms * 3.0`

That is an unauthorized weakening of the Architect acceptance criterion.

The downloaded artifact itself reports:

- left normal `3937.398 ms`;
- left quarter `12515.9 ms`;
- left ratio `3.1787×`;
- right normal `3942.507 ms`;
- right quarter `12497.416 ms`;
- right ratio `3.1699×`.

These values also do not match the submitted result's `3747.3 / 12388.0` and `3711.6 / 12378.2` figures, despite the artifact digest matching exactly. The closeout report therefore must be reconciled to the hosted artifact before acceptance.

## Material defect 2 — verified phase still comes from a hard-coded controller constant

The presentation path computes `authored_track_tick` from loaded `duration_ticks`, but the shared verifier validates `animation_phase` from `MonLocomotionController`.

The controller owns `AUTHORED_PROFILE_LOOP_TICKS := 32.0` and increments `_animation_phase` from that constant. The verifier then expects `velocity / 96 / 32`.

Review 19 explicitly required phase to derive from the real authored track timing and prohibited satisfying the gate with a constant. The current verifier therefore proves consistency with a duplicated constant, not provenance from the loaded temporal track.

## Material defect 3 — required capture evidence fields are absent

Each gameplay capture records label, file, semantic tick, track, frame, actor X, controller animation phase, review rate, and non-black status.

It does not record the required source-pack identity/hash, source-frame identity/hash, presentation phase derived from the loaded authored track, or monotonic review wall-clock index at capture time.

## Material defect 4 — required actual-capture review media is absent

The hosted C06 evidence contains checkpoint PNGs and JSON/log records, but no C06 strip or GIF assembled from those actual Godot captures. Review 19 required one.

## Evidence-integrity rule

Do not treat green CI as acceptance when the workflow assertion is weaker than the Architect criterion. CI must encode the authority, not redefine it.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C02

## Objective

Close only the remaining C06-C01 evidence defects: restore authoritative 4× review pacing, derive presentation phase from the loaded authored track, bind capture records to source/timing identity, generate actual-capture review media, and reconcile the inaccurate C06-C01 timing report.

## Why this is next

C06-C01 materially corrected the blank capture, dual-clock, wire-range, and negative-label problems. Legal-transition qualification remains blocked because the final evidence gate was weakened and the hosted artifact does not prove the remaining timing/provenance requirements.

## Authoritative basis

- Architecture v1.0 remains adopted.
- Roadmap Phase 02 remains active/unaccepted.
- Architect Review 19 remains historical authority for C06-C01.
- This Review 20 supersedes only the unresolved C06-C01 closeout disposition and routes C06-C02.
- Preserve frozen R06 pack hash `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.

## Known evidence

- Real translated left/right Godot captures now exist and are non-black.
- Matched normal/quarter captures are semantically identical.
- Common sequence range and one paused/manual presentation clock are established.
- Existing hosted timing is only about `3.17–3.18×`, not 4×.
- Current workflow accepts `>=3.0×`.
- Current verified `animation_phase` is controller-derived from hard-coded `32.0`, not independently derived from loaded frame durations.
- Capture records omit source identity and monotonic wall-clock index.
- No capture-derived C06 strip/GIF is present.

## Scope

1. Fetch and normally merge current `origin/main`.
2. Preserve all accepted C06-C01 implementation and frozen source bytes unless a change is strictly required to satisfy this directive.
3. Replace the weakened `>=3.0×` timing assertion. Quarter review must use a true 4.0× wall-time pacing target for the same semantic checkpoint sequence.
4. Use monotonic elapsed time (`Time.get_ticks_usec()` or equivalent already available in Godot 4.7.2) and deadline-based pacing so render/capture overhead does not collapse the intended slowdown.
5. Acceptance tolerance for hosted wall-time measurement is `3.90× <= quarter/normal <= 4.10×` for left and right. This clarifies measurement jitter; it does not retroactively accept the existing ~3.17× artifact.
6. Record a monotonic `review_elapsed_usec` or equivalent for every required capture. For every nonzero matched checkpoint, quarter elapsed time must be consistent with 4× normal elapsed time within a documented bounded tolerance.
7. Derive `authored_loop_ticks = sum(duration_ticks)` from the loaded selected track. Derive `presentation_phase` from `authored_track_tick / authored_loop_ticks` or an equivalent exact representation. Do not use `MonLocomotionController.AUTHORED_PROFILE_LOOP_TICKS` as acceptance evidence.
8. The shared verifier must independently load/recompute the selected track's durations and reject a trace whose loop ticks, frame mapping, or presentation phase disagrees with the pack. Add a negative mutation that would pass a duplicated constant but fails track-derived verification.
9. Each capture record must include at minimum: checkpoint label, semantic tick, actor root position, track ID, frame index, authored track tick, track-derived presentation phase, review elapsed monotonic time, source pack SHA-256, source frame filename/ID, source frame SHA-256, capture filename, capture SHA-256, and non-black status.
10. Prove normal/quarter matched checkpoints have identical semantic tick, actor position, track, frame, authored tick, presentation phase, and source-frame identity; only review wall-time differs.
11. Assemble one strip or GIF per direction, or one combined review artifact, using only the hosted Godot checkpoint PNGs. No regenerated/reconstructed sprite imagery.
12. Reconcile the C06-C01 closeout report to actual hosted artifact `10344096459` and preserve the prior reported timing values as corrected historical evidence rather than silently replacing them.
13. Re-run focused R06, Phase 01, and inherited Phase 02 on one final implementation SHA.
14. Return to Architect and stop.

## Do not change

No image generation, sprite editing, resampling, source reselection, new dependency, controller ownership change, command semantics change, legal-transition campaign, Openbox endurance, Phase 03 work, PR #9 merge, or Issue #8 closure.

## Required investigation

- Explain the fixed overhead that caused the current requested quarter-delay implementation to produce only ~3.17× observed wall-time.
- Confirm the exact loaded duration sum for left/right cruise tracks from the frozen pack.
- Determine whether any current evidence consumer depends on controller `animation_phase`; preserve compatibility if needed, but do not use that field as authored-presentation proof.

## External discovery

No new dependency or architecture research is authorized. If timing API behavior is material, use official Godot 4.7 documentation only. `Time.get_ticks_usec()` is the required class of monotonic measurement; do not infer wall-time from requested timer delays alone.

## Authority boundaries

- Controller remains authority for canonical movement and command lifecycle.
- Loaded temporal track remains authority for presentation frame duration and presentation phase.
- Render capture remains observational evidence only.
- CI validates Architect criteria; CI may not weaken them.
- Codex may not authorize transition qualification or accept Phase 02.

## Acceptance criteria

C06-C02 is acceptable only if one exact implementation SHA demonstrates all of the following:

- frozen source pack hash unchanged;
- V2 common wire-range tests still pass;
- one paused/manual presentation clock remains;
- loaded left/right cruise loops independently recompute to 32 authored ticks;
- track-derived presentation phase is modulo-continuous across the loop seam and second loop;
- all required real Godot captures are non-black and visibly translated;
- capture records contain all required source/timing identity fields;
- normal/quarter checkpoint semantics match exactly;
- left and right quarter/normal observed wall-time ratios each lie in `[3.90, 4.10]`;
- shared verifier rejects track-duration/phase mutations using the frozen pack as authority;
- capture-derived review strip/GIF exists;
- existing controller/loader/scheduler negatives remain green and truthfully labeled;
- focused R06, Phase 01, and inherited Phase 02 pass on the exact same implementation SHA.

## Required validation

- Schema/Rust/Godot wire-boundary regression.
- Exact frozen source hash verification.
- Pack-derived timing/phase verifier positive and negative cases.
- Capture metadata completeness and SHA verification.
- Pixel-content check for all gameplay captures.
- Semantic equality check across normal/quarter capture pairs.
- Actual monotonic wall-time ratio calculation with explicit values in the artifact.
- Regression test that an artificial `3.33×` quarter/normal ratio is rejected by CI validation.
- Exact-head R06 + Phase 01 + inherited Phase 02 hosted workflows.

## Prohibited claims

Do not claim C06 complete before Architect review; 4× review timing from configured delay alone; authored phase from the controller's hard-coded loop constant; source-bound capture evidence when hashes/identity are absent; or Phase 02/legal-transition/endurance/later organism capability.

## Stop and return to Architect if

Stop if true 4× deadline pacing cannot be achieved under hosted Xvfb without changing semantic state, if track-derived phase conflicts with frozen authored timing, if source identity cannot be bound without modifying frozen source bytes, or if satisfying this evidence gate would require a new dependency or architecture change.

## Required project updates

Update the active Phase 02 task evidence, C06 result/history, GitHub PR #9 and Issue #8 handoff, and the dedicated Notion report. Preserve the C06-C01 artifact and incorrect prior timing report as historical evidence with an explicit correction note.

## Required handoff

Return `# CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C02` with sections for authority sync, protected work, baseline/merge/branch, artifact reconciliation, 4× pacing implementation, measured left/right ratios, track-derived phase, verifier provenance, capture metadata, source/capture hashes, review media, negative regressions, exact-head R06/Phase 01/Phase 02, files changed, failures, publication, remote equality, and recommendation.

If C06-C02 passes without another material defect, stop. The Architect will then decide whether to authorize the legal-transition campaign.
