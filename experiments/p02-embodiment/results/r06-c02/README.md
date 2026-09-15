# R06-C02 grounded integration evidence

This directory contains sanitized, reproducible evidence for the grounded
integration correction. It does not contain new art: all PNG bytes under
`assets/source/p02/r06/approved/` are the frozen operator-approved runtime
masters and were only read while deriving metadata.

## Reproduce

From a clean local ext4/NVMe checkout, with Python 3, Pillow, and jsonschema:

```bash
python3 experiments/p02-embodiment/scripts/ground_r06_c02.py \
  --source assets/source/p02/r06/approved \
  --evidence experiments/p02-embodiment/results/r06-c02
python3 experiments/p02-embodiment/scripts/validate_r06_c02.py \
  --source assets/source/p02/r06/approved \
  --evidence experiments/p02-embodiment/results/r06-c02
```

For intake and atomic-publication evidence, run `intake_r06_pack.py` into a
fresh temporary directory, repeat with `--inject-failure`, assert that the
failed output directory is absent, and then run
`record_r06_c02_evidence.py`. Hosted CI additionally runs the pinned Rust,
SQLite, and Godot 4.7.2 gates; those runtimes are not assumed to exist locally.

The grounding command measures the lowest non-black contour of each accepted
source image, records only visible sole/contact geometry as machine-assisted
landmarks, and leaves unused anatomy `not_applicable` or `occluded`. It emits
representative overlays, per-track 24 Hz root plans, and stitched start/loop/
stop continuity plans. No source image is resized, cropped, recolored,
recompressed, or rewritten.

## Evidence boundary

The local result is bounded candidate engineering evidence. It does not prove
visual identity approval, product embodiment, target-host display behavior,
security, reliability, or Phase 02 acceptance. Hosted Godot evidence must use
the strict `RenderingServer.frame_post_draw` observation; a texture readback
alone is intentionally insufficient.
