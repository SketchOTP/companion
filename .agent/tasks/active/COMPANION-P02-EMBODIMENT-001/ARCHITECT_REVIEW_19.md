# Architect Review 19 — C06 Partial Accepted; Render Proof and Presentation Clock Correction Required

## Verdict

`CONTINUE — R06-C06 PARTIAL ACCEPTED.`

Retain C06 replay/freshness semantics, active-intent cancellation, controller-owned `MonRoot`, fixed-step accumulator, frozen source identity, and exact-head hosted regression. Do **not** start transition qualification yet.

## Reviewed evidence

- Tested implementation: `941c231d4562177c1db02cd61fc0f0c085e6dae4`
- Publication head: `1adadc1206be4371b9baa42aa21153d6eeae74fd`
- Frozen R06 pack: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`
- R06 CI: `34800729601` PASS
- Phase 01 CI: `34800729655` PASS
- Inherited Phase 02 CI: `34800729662` PASS
- R06 artifact: `10330902923`, digest `sha256:3952de98c7f96aa8b9a7ddafbd9d5b848b8539862e85549386605f98f4375cf1`

No approved sprite pixel changed.

## Accepted C06 boundary

- V2 intent carries UUID identity and monotonic `intent_sequence`.
- Reused/equal/lower commands are rejected by the reusable Godot controller.
- Stop/cancellation targets the active movement intent and latches terminal stop.
- Canonical actor translation remains controller-owned; sprite presentation is downstream.
- The accumulator path demonstrates equivalent 24 semantic ticks under 30 FPS and 60 FPS supplied render deltas.
- Frozen source/intake/Rust/render/compositor/failure/export evidence remains retained.

## Material defect 1 — claimed normal/quarter rendered playback is not actually captured

Architect downloaded hosted artifact `10330902923` and inspected the four C06 viewport captures. All four left/right normal/quarter `movement.json.viewport.png` files are byte-identical SHA-256:

`6e6426a0da7adb0ddb171ec69433d23542149a366891d201b026cc7545364c12`

All contain only black RGB pixels with opaque alpha. In `r06_c06_locomotion_test.gd`, `_capture_viewport()` runs after the initial `frame_post_draw` but **before** any `SpriteFrames` resource is assigned or start/cruise/stop playback begins. The hosted workflow therefore proves a render signal and a black viewport image, not translated character playback.

## Material defect 2 — presentation timing has two competing authorities and bypasses accepted duration ticks

`_load_frames()` installs source `duration_ticks` into `SpriteFrames` and calls `sprite.play()`, but `_play_track()` also overwrites `sprite.frame` every semantic tick via `frame_cursor += rate`.

For the accepted left/right loop tracks, eight frames each have `duration_ticks = 4`, so one authored loop is 32 source ticks at nominal 1.0x. The manual path advances one frame every semantic tick, and the controller phase increments by `rate / 24`, producing a 24-tick phase cycle instead of the accepted 32-tick loop. Setting `sprite.frame` also resets `frame_progress` while the node remains playing.

C06 therefore does not yet prove velocity/gait coupling against the actual accepted temporal contract.

## Material defect 3 — V2 wire range is not equivalent across Rust and Godot

The V2 JSON Schema accepts `intent_sequence` through unsigned 64-bit maximum `18446744073709551615`; Rust stores it as `u64`. GDScript `int` is signed 64-bit, maximum `9223372036854775807`, and the controller converts the wire value with `int()`.

The current schema therefore accepts values the Godot consumer cannot faithfully represent. Wire equivalence is not yet proven.

## Evidence-strength defect — not all 17 negatives execute the protected Godot path

The Python model contains 17 negative cases. Godot `_negative_probe()` directly exercises only a subset of replay/cancellation/profile/sign cases; missing-track/corrupt-pack checks are local assertions and fixed-step/trace reset cases remain Python-model evidence. Preserve those results, but do not label all 17 as protected-path Godot negatives.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C01

## Objective

Close only the three material C06 defects: truthful rendered playback capture, one authored-duration-aware presentation clock, and an exactly representable intent-sequence wire range. Reconcile negative-path evidence labels/execution. No new art and no transition work.

## Scope

1. Fetch and normally merge current `origin/main`; preserve governance history and all accepted source bytes.
2. Keep controller-owned canonical movement, V2 replay/cancellation semantics, and the fixed 24 Hz accumulator.
3. Tighten the V2 wire schema so every accepted `intent_sequence` is exactly representable by the Godot signed-64 consumer. Rust may remain `u64` only if schema validation constrains the wire to the common range. Add schema/Rust/Godot boundary tests at the maximum accepted value and max+1 rejection.
4. Replace dual animation authority with one deterministic presentation clock. Either let `AnimatedSprite2D`/`SpriteFrames` own frame progression or drive frame/progress manually while the node is paused; do not both play and overwrite frame state.
5. Preserve source `duration_ticks` exactly. The current eight-drawing profile loop must take 32 authored ticks at nominal 1.0x. Slow/nominal/fast calibration scales presentation timing as 0.5x/1.0x/1.5x without changing canonical displacement.
6. Derive loop phase from the actual authored loop duration and prove modulo continuity across two repeated loops. Do not hard-code `phase_resets = 0` as proof.
7. Move viewport capture into actual playback. For left/right normal and quarter review, capture `frame_post_draw`-bounded images during start, translated cruise, second-loop cruise, and stop. Every capture set must contain visible non-black mon pixels and moving checkpoints must show different actor positions.
8. Normal and quarter review must represent the same semantic checkpoints while quarter review takes 4x review wall-time. Publish a review strip or GIF assembled only from actual Godot viewport captures.
9. Rebuild negative evidence so command/replay/cancellation negatives run through the actual Godot controller, pack-selection negatives exercise the actual loader/resolver, and scheduler/trace negatives use one shared verifier also applied to the positive trace. Label any Python-model-only cases explicitly.
10. Retain strict `RenderingServer.frame_post_draw`, black-field compositor QA, immutable intake, Rust round-trip, failure/recovery, export/restore, and historical C03/C04 evidence.
11. Select one final implementation SHA and pass focused R06 + Phase 01 + inherited Phase 02 on that exact SHA.
12. Return to Architect and stop. If C06-C01 passes without a new material defect, the next directive is the legal-transition campaign.

## Do not change

No image generation, sprite editing, cutout, resampling, visual reselection, dependency adoption, Openbox endurance, Phase 03, PR merge, or Issue closure.

## Stop and return if

Stop if preserving authored timing makes the accepted animation visually unusable without pixel changes, truthful rendered captures cannot show the mon under Xvfb, common wire-range enforcement requires an architecture change, or controller/presentation ownership must be weakened.
