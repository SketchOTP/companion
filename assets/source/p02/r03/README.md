# R03 editable embodiment proof

This directory contains the candidate `MON_BODY_SOURCE_V2` hierarchy and
selected review derivatives for Architect and operator review. It is not an
approved production body. The six-view turnaround and identity master under
`assets/source/p02/references/` are the canonical inputs; their hashes are
recorded in `mon_body_source_v2.json`.

The Godot scene is the editable source with explicit pivots, limbs, digits,
feet, replacement-drawing slots, and bounded pose controls. The deterministic
Python baker in `experiments/p02-embodiment/scripts/build_r03_motion.py`
mirrors those named source parts to produce review-only full-canvas PNGs and
ordered motion artifacts. Runtime animation remains raster `SpriteFrames`;
the Godot scene is not a skeletal-runtime substitute.

All diagonals, temporal tracks, anatomy, palette, and motion in this directory
remain `CANDIDATE_PENDING_OPERATOR_APPROVAL`.
