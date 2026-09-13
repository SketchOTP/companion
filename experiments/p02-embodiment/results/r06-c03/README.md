# R06-C03 support and cumulative-travel investigation

This evidence is a fail-closed investigation of the frozen R05/C01 runtime
masters. It does not modify or regenerate any source image. The source-pack
SHA is `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.

## Method

`qualify_r06_c03.py` measures the lowest visible contour of each accepted PNG
and records every sole candidate, its source SHA, declared pose label, visible
grounded soles, support/swing identity, support state, and contour evidence.
For a stable body anchor it uses the median visible foreground x-coordinate in
the torso window y=650..900 and the measured sole baseline for y. This is
machine-assisted geometry evidence, not a visual approval claim.

The authored `near`/`far` phase correspondence is retained and checked against
the visible candidate rather than used as the sole source of truth. Passing and
up drawings are therefore included in the support timeline when their contour
shows a grounded sole. Double support is represented when two candidates are
within the measured four-pixel ground band.

Root plans run at 24 Hz using:

```text
world_contact = actor_root + 0.5 * (source_contact - source_root)
```

At each support handoff the current actor root is preserved and the new
touchdown anchor is computed from the actual source contact. No stride distance,
re-centering, pixel edit, or hidden root jump is introduced.

## Result

The positive predicate is **BLOCKED**. The frozen drawings produce the opposite
touchdown ordering for both requested travel directions:

| direction | touchdown anchor deltas (px) | two-loop net (px) | required sign |
|---|---:|---:|---:|
| left | `+135.5, +72.0, +135.5, +72.0` | `+255.0` | negative |
| right | `-118.0, -134.5, -118.0, -134.5` | `-336.0` | positive |

Thus left-facing travel advances screen-right and right-facing travel advances
screen-left under the evidence-supported support assignments. The contradiction
exists before any arbitrary stride policy could be chosen. The complete per-
frame and per-tick records are in `support_investigation.json`.

The complete stitched start → loop → loop → stop plans show the same reversal:
left ends at `+415.0 px` and right at `-505.0 px`. No loop is re-centered; the
second loop begins at the first loop's reached world position.

All seven executable negative tests pass: omitted passing/up support, support
identity swap, reversed touchdown order, zero-net loop, second-loop recenter,
hidden root reset, and planted slip over two pixels are rejected by the semantic
predicate. `validation.json` records the independent validator result.

## Reproduction

```bash
python3 experiments/p02-embodiment/scripts/qualify_r06_c03.py \
  --source assets/source/p02/r06/approved \
  --out experiments/p02-embodiment/results/r06-c03
python3 experiments/p02-embodiment/scripts/validate_r06_c03.py \
  --evidence experiments/p02-embodiment/results/r06-c03
```

Both commands intentionally exit with status `2` for this directive stop:
the evidence is complete and the frozen geometry is contradictory, not a
successful locomotion qualification.
