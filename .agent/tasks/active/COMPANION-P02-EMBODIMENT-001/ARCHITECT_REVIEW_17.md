# Architect Review 17 — C04 Block Accepted; Controller-Driven Locomotion Supersedes Raster Root Extraction

## Verdict

`REPLAN / CONTINUE — C04 STOP ACCEPTED; NO NEW ART AUTHORIZED`

- Reviewed task head: `340afd893f96013e3fdc8480514bf0bbb1d087f0`
- C04 implementation head: `368876873d5fab5cbcd4de9f7f3b3d7dd30d379e`
- PR #9: draft/open/unmerged
- Issue #8: open
- Architecture v1.0: adopted/unchanged
- Phase 01: accepted
- Phase 02: active/not accepted
- Phase 03+: closed
- Notion Review 17: https://app.notion.com/p/3da833cb27ff812e96c5d76a0d8af37e

C04 correctly stopped without modifying approved source pixels. Preserve its blocked result and all C02/C03/C04 evidence.

## Architect finding

The frozen R05 walk frames are in-place full-body raster drawings. They contain no authored root-motion channel, skeleton, persistent material foot marker, or canonical world-displacement curve. Canonical screen movement therefore must not be inferred from raster pixels and made authoritative.

Independent review also found one remaining C04 harness confound: during double support, `root_plan()` records a newly entering support anchor before correcting the actor root for the continuing support, then measures the new foot against that pre-correction anchor. Some reported slip/touchdown values are therefore analysis-order dependent.

Architecture v1.0 requires presentation to remain downstream of canonical state. For the R05 opaque seed, screen-space translation is controller-owned; Godot applies a typed locomotion intent while the sprite gait is presentation synchronized to that movement.

## Adopted correction

For the frozen R05 opaque in-place library:

- canonical `MonRoot` position/velocity is controller-owned;
- Godot is the presentation adapter;
- left intent selects true left-profile locomotion and right intent selects true right-profile locomotion;
- playback rate/phase may be calibrated to commanded velocity;
- foot contours/contact timing remain diagnostic presentation evidence;
- the prior `<=2 px` single-point planted-contact rule is superseded as a Phase-02 gate for this exact in-place raster seed, while remaining valid for future assets that actually provide authored root/contact semantics.

This does not permit wrong-direction movement, loop recentering, teleports, source mutation, or false physical-grounding claims.

Prior-art sanity check: movement-component/controller-driven locomotion with in-place animation is a standard alternative to animation-driven root motion. No external dependency is adopted.

References:
- https://dev.epicgames.com/documentation/unreal-engine/root-motion-in-unreal-engine
- https://dev.epicgames.com/documentation/en-us/unreal-engine/movement-components-in-unreal-engine
- https://docs.unity3d.com/kr/2018.3/Manual/ScriptingRootMotion.html

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C05

## Objective

Implement a typed controller-driven locomotion presentation adapter over the exact frozen R05 frames and prove direction, continuity, phase synchronization, interruption, and recovery without changing art.

## Required work

1. Fetch and normally merge current `origin/main` into the existing Phase 02 branch.
2. Preserve every approved source byte and all C02/C03/C04 evidence.
3. Add a versioned Phase-02 locomotion-intent contract with intent identity, direction/facing, commanded screen velocity, start/cruise/stop state, and cancellation/interruption identity.
4. Treat that contract as synthetic qualification input only; do not claim organism autonomy.
5. Canonical `MonRoot` translation follows the typed intent at 24 Hz. Sprite pixels/contacts may not overwrite canonical position.
6. Left movement selects left-profile start/loop/stop tracks; right movement selects right-profile tracks. No silent front-left fallback.
7. Calibrate animation playback rate/phase to commanded velocity as presentation metadata. Calibration may minimize visible foot skate but may not redefine commanded displacement.
8. Qualify `start -> loop -> loop -> stop` for both directions at a measured nominal calibration plus bounded slower/faster synthetic velocities.
9. Repeated loops must accumulate position without recentering or phase reset. Mid-loop stop/interruption must remain continuous.
10. Preserve strict `RenderingServer.frame_post_draw`, compositor, Rust/intake, failure/recovery and export/restore regressions.
11. Publish normal-speed and quarter-speed translated playback plus commanded velocity, actor-position, frame-phase, event and diagnostic contact/foot-skate traces.
12. Fail wrong direction, velocity-sign mismatch, loop recenter, actor-position discontinuity, phase reset, dropped/duplicated movement ticks, stale intent replay, wrong-profile selection, invalid/missing track and ineligible pack.
13. Pass R06 + Phase 01 + inherited Phase 02 on one implementation SHA and return to Architect.

## Acceptance boundary

C05 passes when controller-owned translation is directionally correct and continuous; repeated loops accumulate world position; animation selection and phase follow that movement; interruption/stop preserve continuity; accepted pixels remain unchanged; and the retained C02 runtime boundaries stay green.

Foot-contact residuals must be reported honestly as diagnostic presentation evidence, not exact physical grounding.

## Prohibited work

No image generation, sprite editing, cutout, recolor, resampling, new art selection, dependency adoption, transition campaign, Openbox endurance, Phase 03 work, PR merge, or Issue #8 closure.

## Stop and return if

Stop if translated playback is visibly unacceptable and cannot be corrected by playback-rate/phase calibration alone, if pixel changes would be required, or if canonical movement would have to be stored in render-only state.

## Capability boundary

This qualifies a controller-driven presentation locomotion primitive only. It does not establish organism autonomy, navigation intelligence, memory, learning, perception, speech, caregiving, transition qualification, target endurance, or Phase 02 acceptance.
