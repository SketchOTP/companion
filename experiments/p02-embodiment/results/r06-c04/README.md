# R06-C04 runtime-transform locomotion requalification

Status: **BLOCKED** (investigation evidence; not Phase 02 acceptance).

This result preserves all accepted C02 evidence and re-runs only locomotion
qualification against the transform executed by `godot/r06_black_pack_test.gd`:

* native source: 1254x1254;
* `AnimatedSprite2D.centered = true`, so the source anchor is `(627,627)`;
* sprite offset `(0,0)`;
* uniform scale `0.5`;
* `MonRoot`/container position `(320,320)`;
* `sprite_local = source_pixel - (627,627) + offset`;
* `world = MonRoot + scale * sprite_local`.

The torso/registration anchor is kept separate from support-foot metadata.  Sole
candidates are assigned persistent `near`/`far` identities by temporal
correspondence; screen-X ordering is used only for an explicitly marked initial
ambiguity and never for a handoff.  Both contacts are retained during double
support.  Source PNG bytes remain unchanged (pack SHA
`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`).

## Corrected result

The repeated loop still fails the complete support qualification. Left touchdown
anchors alternate `+140.0, -174.5, +85.0, -159.5, ...` world px and right
anchors alternate `-115.0, +184.5, -143.0, +168.0, ...`; the first handoff is
rightward for requested left travel and leftward for requested right travel.
The actor-root net over two loops is `-218.0 px` left and `+189.0 px` right, but
alternating touchdown progression and double-support disagreement produce
maximum planted slips of `27.0 px` and `18.0 px` respectively (required ≤2 px).
Several passing/up drawings also conflict with the phase hint, so those frames
remain explicitly ambiguous rather than being silently relabeled.

The JSON records every frame/source hash, visible sole candidate, stable leg,
support state, source and sprite-local contacts, runtime offset, actor root,
world contact and slip.  `c03_vs_c04` retains the prior heuristic anchors and
the corrected anchors side-by-side.

## Independent negatives

All negatives start from a separately constructed passing baseline that first
passes the semantic predicate.  Each mutation rejects for exactly its intended
reason: omitted support, stable-leg swap, screen-X substitution,
support-dependent offset, reversed touchdown, zero-net loop, loop recenter,
hidden actor-root reset, and planted slip greater than 2 px.

Run:

```bash
python3 experiments/p02-embodiment/scripts/qualify_r06_c04.py \
  --source assets/source/p02/r06/approved \
  --out experiments/p02-embodiment/results/r06-c04
python3 experiments/p02-embodiment/scripts/validate_r06_c04.py \
  experiments/p02-embodiment/results/r06-c04/locomotion_requalification.json
```

The qualifier intentionally exits `2` for the real-art contradiction; the
structural validator exits `0` when that blocked evidence and its independent
negative matrix are complete.  Hosted C04, transition qualification and
Openbox endurance are **NOT RUN** because the directive requires stopping on
this result.
