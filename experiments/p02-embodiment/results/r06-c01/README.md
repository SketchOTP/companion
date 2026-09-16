# R06-C01 immutable runtime-selection evidence

This directory records the derived selection from the exact operator-approved
R05 final playback archive. It is a candidate integration package, not Phase 02
acceptance. `runtime_visual_master` entries come only from accepted playback
tracks; retries, sheets, and diagnostics are excluded.

The source pack under `assets/source/p02/r06/approved/` is copied byte-for-byte
from the frozen archive. The two adopted presentation profiles are
`R05_BLACK_FIELD_RGB8_V1` and `R05_TRANSPARENT_RGBA8_V1`; `MON_FRAME_V1` is not
changed. Intake outputs are local export/restore artifacts and are not canonical
source history.

Reproduction:

1. Run `python3 experiments/p02-embodiment/scripts/build_r06_c01_selection.py --out assets/source/p02/r06/approved`.
2. Validate `assets/source/p02/r06/approved/pack.json` against
   `contracts/schemas/mon-opaque-black-frame-source-pack-v1.schema.json`.
3. Run `python3 experiments/p02-embodiment/scripts/intake_r06_pack.py --source assets/source/p02/r06/approved --out <local-export>/intake`.
4. Run `python3 experiments/p02-embodiment/scripts/record_r06_c01_evidence.py --out experiments/p02-embodiment/results/r06-c01 --intake <local-export>/intake`.
5. In a hosted environment with the pinned Rust and Godot artifacts, run the
   canonical runner through `.github/workflows/phase02-embodiment-r06.yml`.
   Run `34761173688` is the retained passing execution; its sanitized logs and
   hashes are committed in `hosted-run-34761173688.json` and the full bundle is
   published as the workflow artifact.

No image generation, conversion, cutout, resampling, recolor, or repainting is
performed. Missing hosted toolchains are recorded as `NOT RUN`, never as pass.
