# Phase 02 embodiment qualification and asset pipeline

This directory contains deterministic, disposable authoring and validation
tools for `COMPANION-P02-EMBODIMENT-001`.  It is not the Companion organism,
memory, speech, perception, care, or production runtime.  Generated drawings
are identity-faithful candidates and remain pending operator visual approval.

The pipeline uses only Python's standard library and the already available
Pillow runtime for local rasterization.  No package is added to the production
workspace.  The historical `build_assets.py` and `build_core_motion.py`
outputs are retained as rejected/superseded evidence. The active
reference-grounded gate is `build_motion_proof.py`, which reads the exact native
identity PNG, emits six bounded temporal proof tracks, and writes generated
frames to a caller-owned artifact directory (never the Git tree).

Run from the repository root:

```text
PROOF_OUT="$(mktemp -d /tmp/companion-p02-proof.XXXXXX)"
python3 experiments/p02-embodiment/scripts/build_motion_proof.py --out "$PROOF_OUT" --clean
python3 experiments/p02-embodiment/scripts/validate_motion_proof.py --out "$PROOF_OUT"
python3 experiments/p02-embodiment/scripts/compare_authoring_candidates.py \
  --proof "$PROOF_OUT" --out "$PROOF_OUT/authoring-comparison.json"
```

The proof output includes `temporal_tracks.json`, `manifest.json`, 26
full-canvas candidate frames, and selected review strips. All generated output
is deterministic for the pinned script and is safe to rebuild in a clean
checkout. Runtime state and temporary exports belong in a private XDG
directory, never in the checkout or an SSHFS mount. Review PNGs under
`assets/source/p02/review/r02/` are selected derivatives only; library-scale
corpus and packs remain deferred until operator approval.
## R02 canon and motion-proof scope

Architect Review 02 supersedes the prior full-library run. The active
qualification surface is now the exact-reference and minimal motion-proof
gate. `build_motion_proof.py` emits one `front_left` facing with six temporal
tracks (26 drawings total) into a private output directory. It must be run in
two clean processes and compared byte-for-byte. `validate_motion_proof.py`
fails closed on reference hashes, track shape, timing, root, safety bounds and
within-track duplicates. The resulting candidate remains pending operator
approval; no eight-direction or 32-family production is authorized.

The vector/path and layered-raster sources are both retained as candidates in
`assets/source/p02/canon/`. `compare_authoring_candidates.py` records that the
raster proof was rendered while the `resvg` vector rasterizer was unavailable on
the current host; this is an explicit comparison limitation, not a dependency
adoption.

## R03 articulated-body correction

`build_r03_motion.py` is the active R03 proof baker. It reads the explicit
`MON_BODY_SOURCE_V2` hierarchy, emits a deterministic `MON_TEMPORAL_TRACKS_V2`
manifest, and writes generated frames and review derivatives to a caller-owned
temporary directory. `validate_r03_motion.py` derives root, contacts, safety
bounds, temporal change, source-part coverage, checksums, and Draft 2020-12
schema results from those outputs and includes tamper-negative mutations.

Godot's `r03_temporal_playback_test.gd` loads every actual generated PNG into
`AnimatedSprite2D`, sets 24 FPS, uses integer duration ticks as relative
weights, and observes frame progression and completion. The headless dummy
renderer cannot expose a readable SubViewport texture, so the Python baker is
explicitly a qualification-only raster mirror of the editable Godot source;
this does not claim a production authoring method or operator approval.
