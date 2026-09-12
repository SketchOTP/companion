# Phase 02 embodiment qualification and asset pipeline

This directory contains deterministic, disposable intake and validation tools
for `COMPANION-P02-EMBODIMENT-001`. It is not the Companion organism, memory,
speech, perception, care, or production runtime. R04 generates only obvious
geometric test graphics; all production character pixels belong to the AI
Architect and visual approval belongs to the Operator.

The pipeline uses only Python's standard library and the already available
Pillow runtime for local rasterization.  No package is added to the production
workspace.  The historical `build_assets.py` and `build_core_motion.py`
outputs are retained as rejected/superseded evidence. Historical
`build_motion_proof.py` reads the exact native identity PNG, emits six bounded
temporal proof tracks, and writes generated
frames to a caller-owned artifact directory (never the Git tree).

The active R04 path is `build_r04_synthetic_pack.py` →
`intake_authored_frame_pack.py` → actual Rust pack validation →
`r04_authored_pack_test.gd`. Intake copies source bytes without alteration;
R03 has no path into `MonAvatar`.

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

## R03 rejected negative evidence

`build_r03_motion.py` is retained only to reproduce the rejected R03 output
with `--negative-evidence`. It reads the explicit
`MON_BODY_SOURCE_V2` description and writes the formerly submitted output to a
caller-owned temporary directory. Its metadata checks are retained only to
show what the rejected experiment asserted; they are not identity, rig,
contact, or motion-quality evidence.

Godot's old `r03_temporal_playback_test.gd` is likewise historical negative
evidence. R04 has no code path from these files to `MonAvatar`.
# Phase 02 qualification infrastructure

The R04-C03 Godot diagnostic boundary is implemented by
`scripts/run_godot_qualification.py`. It is the sole Godot qualification
runner for local reproduction, direct workflow gates, and
`run_r04_evidence.py`. Each invocation retains separate `godot.stdout.log`,
`godot.stderr.log`, `godot.engine.log`, `xvfb-wrapper.log`, and `result.json`
files. Godot application `ERROR:` lines fail the gate; Xvfb wrapper warnings
remain separate diagnostics.

This remains synthetic bounded evidence only. It does not generate production
character art, approve visual identity, or establish Phase 02 acceptance.
