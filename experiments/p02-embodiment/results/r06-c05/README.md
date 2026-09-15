# R06-C05 controller-driven locomotion

This is a bounded synthetic qualification of controller-owned movement over
the frozen R05 in-place raster pack. No source PNG is edited and no raster
contact writes canonical actor position.

The typed intent contract is `contracts/schemas/mon-locomotion-intent-v1.schema.json`
and `foundation_core::contracts::LocomotionIntentV1`. At 24 Hz, the controller
integrates `actor_root_x += commanded_velocity_px_per_second / 24`. Left
intents select `r06_playback_track_07/08/09` (true left profile); right intents
select `r06_playback_track_12/13/14` (true right profile). The loop track is
selected continuously across both loops; only its authored frame phase wraps.

Qualification command:

```bash
python3 experiments/p02-embodiment/scripts/qualify_r06_c05.py \
  --pack assets/source/p02/r06/approved/pack.json \
  --out experiments/p02-embodiment/results/r06-c05
```

The result contains six full `start → loop → loop → stop` runs (left/right at
slow, nominal, and fast bounded velocities), interruption traces, normal and
quarter-speed presentation traces, exact 24 Hz actor samples, selected
track/frame phase, and a 13-case negative matrix. The Python result is a
controller qualification record; Godot presentation is exercised by
`godot/r06_c05_locomotion_test.gd` with the same track selection and transform.

This does not claim organism autonomy, navigation, physical grounding,
production reliability, or Phase 02 acceptance. Foot contact/skate remains a
diagnostic visual residual for the frozen in-place art.

See `R06_C05_RESULT.md` for the exact bounded result and retained limits.
