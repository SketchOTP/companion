# R06-C03 — Continuous stance and cumulative travel

## Status

`BLOCKED` — exact geometric contradiction in the frozen accepted drawings.

No source image was generated, edited, recolored, resampled, or otherwise
mutated. The C02 source pack SHA remains
`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40` and all 58
source PNGs remain byte-identical.

## Evidence

`experiments/p02-embodiment/scripts/qualify_r06_c03.py` measures lowest visible
sole contours and a torso-centroid body anchor for every frame in all six
left/right start, loop, and stop tracks. It records source hashes, visible
grounded soles, support/swing identity, support state, touchdown/toe-off
evidence, confidence, and per-tick 24 Hz actor-root/contact records.

The evidence-supported support assignments yield:

| travel | touchdown anchor deltas | two-loop net | full start→loop→loop→stop net |
|---|---|---:|---:|
| left | `+135.5,+72.0,+135.5,+72.0` | `+255.0 px` | `+415.0 px` |
| right | `-118.0,-134.5,-118.0,-134.5` | `-336.0 px` | `-505.0 px` |

The requested signs are left-negative and right-positive. Both frozen tracks
therefore advance in the opposite direction. No truthful stride distance or
identity relabeling is available inside this directive.

All seven executable negative tests pass: omitted passing/up support, support
identity swap, reversed touchdown ordering, zero-net loop, second-loop
recenter, hidden root reset, and planted slip over two pixels.

Run the validator with:

```bash
python3 experiments/p02-embodiment/scripts/qualify_r06_c03.py \
  --source assets/source/p02/r06/approved \
  --out experiments/p02-embodiment/results/r06-c03
python3 experiments/p02-embodiment/scripts/validate_r06_c03.py \
  --evidence experiments/p02-embodiment/results/r06-c03
```

Both commands return exit status `2` to signal the intentional Architect stop.
Transition qualification and Openbox endurance are not run. Await an explicit
Architect decision; do not alter pixels or weaken the locomotion predicate.
