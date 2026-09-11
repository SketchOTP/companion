# Phase 02 embodiment qualification and asset pipeline

This directory contains deterministic, disposable authoring and validation
tools for `COMPANION-P02-EMBODIMENT-001`.  It is not the Companion organism,
memory, speech, perception, care, or production runtime.  Generated drawings
are identity-faithful candidates and remain pending operator visual approval.

The pipeline uses only Python's standard library and the already available
Pillow runtime for local rasterization.  No package is added to the production
workspace.  The historical `build_assets.py` output is retained as rejected
direction-catalog evidence.  The current reference-grounded core gate is
`build_core_motion.py`, which reads the exact native identity PNG, emits
independent temporal tracks, and writes the generated corpus to a caller-owned
artifact directory (never the Git tree).

Run from the repository root:

```text
CORE_OUT="$(mktemp -d /tmp/companion-p02-core.XXXXXX)"
python3 experiments/p02-embodiment/scripts/build_core_motion.py --out "$CORE_OUT" --clean
python3 experiments/p02-embodiment/scripts/validate_core_motion.py --out "$CORE_OUT"
python3 experiments/p02-embodiment/scripts/build_review_package.py --out "$(mktemp -d /tmp/companion-p02-review.XXXXXX)"
```

The core output includes `temporal_tracks.json`, `atlas_manifest.json`,
`manifest.json`, full-canvas frames, trim/extrude atlases, and review sheets.
All generated outputs are deterministic for the pinned script and are safe to
rebuild in a clean checkout.  Runtime state and temporary exports belong in a
private XDG directory, never in the checkout or an SSHFS mount.  Review PNGs
under `assets/source/p02/review/` are selected derivatives only; the complete
corpus and packs are workflow artifacts/local export bundles.
