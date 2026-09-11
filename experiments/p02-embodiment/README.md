# Phase 02 embodiment qualification and asset pipeline

This directory contains deterministic, disposable authoring and validation
tools for `COMPANION-P02-EMBODIMENT-001`.  It is not the Companion organism,
memory, speech, perception, care, or production runtime.  Generated drawings
are identity-faithful candidates and remain pending operator visual approval.

The pipeline uses only Python's standard library and the already available
Pillow runtime for local rasterization.  No package is added to the production
workspace.  `build_assets.py` creates the authored pose sources, MON_FRAME_V1
PNG frames, overlay library, atlases, packs, manifests, and review sheets.

Run from the repository root:

```text
python3 experiments/p02-embodiment/scripts/build_assets.py
python3 experiments/p02-embodiment/scripts/validate_assets.py
python3 experiments/p02-embodiment/scripts/transition_matrix.py --cases 10000
```

All generated outputs are deterministic for the pinned script and are safe to
rebuild in a clean checkout.  Runtime state and temporary exports belong in a
private XDG directory, never in the checkout or an SSHFS mount.
