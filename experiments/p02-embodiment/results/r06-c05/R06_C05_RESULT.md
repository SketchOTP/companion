# R06-C05 controller-driven locomotion result

Status: `PASSED — BOUNDED QUALIFICATION SUBMITTED FOR ARCHITECT REVIEW`

This qualifies only a synthetic controller-driven presentation primitive over
the frozen R05 in-place raster art. It does not claim physical grounding,
organism autonomy, navigation, reliability, or Phase 02 acceptance.

## Identity and ownership

- Frozen pack: `assets/source/p02/r06/approved/pack.json`
- Pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`
- Pack revision: `r06-c02-grounded-v1`
- Source mutation: `false`
- Intent schema: `contracts/schemas/mon-locomotion-intent-v1.schema.json`
- Rust type: `foundation_core::contracts::LocomotionIntentV1`
- Controller owns canonical `MonRoot`; Godot owns sprite presentation.
- Timing is 24 Hz; each tick integrates `velocity / 24`.

Left selects true profile tracks `r06_playback_track_07/08/09`; right selects
`r06_playback_track_12/13/14`. No front-left fallback is legal.

## Qualification observations

| side | velocity (px/s) | net actor travel | loop boundaries |
| --- | ---: | ---: | --- |
| left | -48 | -176 px | -50, -114 px |
| left | -96 | -352 px | -100, -228 px |
| left | -144 | -528 px | -150, -342 px |
| right | 48 | +176 px | +50, +114 px |
| right | 96 | +352 px | +100, +228 px |
| right | 144 | +528 px | +150, +342 px |

All six runs have contiguous 24 Hz ticks, accumulating repeated loops, and
zero actor-position or animation-phase resets. Mid-loop interruption traces are
retained for both directions and stop without a teleport.

## Godot

`godot/r06_c05_locomotion_test.gd` loads the actual approved pack, uses native
1254×1254 centered textures at scale 0.5, and advances the controller at 24 Hz.
Local Godot 4.7.2 left/right runs pass and observe:

```text
first_frame_render_committed(RenderingServer.frame_post_draw)
track_completed(start)
track_completed(loop)
track_completed(loop)
track_completed(stop)
```

Nominal local net displacement is -352 px (left) and +352 px (right), with
canonical owner `controller`, presentation owner `godot`, and no Godot stderr
errors.

## Negative matrix and limits

The 13-case matrix starts from an independently passing baseline and rejects
wrong direction, sign contradiction, wrong profile/front-left fallback, loop
recenter, actor discontinuity/root reset, phase reset, dropped/duplicated tick,
stale intent replay, missing track, and ineligible/corrupt pack.

C03/C04 raster-contact failures remain historical negative evidence. Foot-skate
is a diagnostic presentation residual for this in-place seed, not canonical
movement truth. Transition, Openbox, production-art, Phase 03, and merge work
were not performed.

## Hosted exact-head regression

Implementation SHA `24b4919a48eeef49fbcbb9305b9f2ad66639b3bd` passed focused R06
`34790169083`, inherited Phase 02 `34790169074`, and Phase 01
`34790167116` plus same-head reruns `34790169089` (job `103813789392`) and
`103814757741`. The persistence check now seeds its known candidate before care
restart; this is test ordering only. Frozen pack and result hashes are
unchanged.
