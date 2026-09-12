# AUTHOR-002 failed key-gate evidence

These sheets document an unsuccessful reference-based authoring study. They are
not candidate production frames, an animation pack, or an approval request.
Construction is provisional; the gait study set was rejected before intake.

Exact prompts: `assets/source/p02/author002/study-requests.json`.
Output hashes/observations: active packet `R05_AUTHOR_002_STUDY_RESULTS.json`.
The result document records the stop condition and all downstream NOT RUN work.

Full raw outputs and exact Photoroom responses remain in private local export
storage, not ordinary Git. To reproduce review derivatives from those retained
inputs (not to regenerate identical AI art):

```sh
python3 experiments/p02-embodiment/scripts/inspect_author002_construction.py --cutouts "$CUTOUT_DIR" --out "$NEW_REVIEW_DIR"
python3 experiments/p02-embodiment/scripts/export_author002_failure.py --requests assets/source/p02/author002/study-requests.json --raw "$RETAINED_GENERATION_DIR" --cutouts "$CUTOUT_DIR" --review "$NEW_REVIEW_DIR" --out "$NEW_EXPORT_DIR"
```

Use new private output directories; both tools refuse existing output roots.
The export checks source byte equality. Its review images are resized/composited
derivatives only. No root/contact coordinates, timing or motion quality are
inferred. Archive timestamps make archives integrity records, not deterministic
byte-for-byte rebuild claims. Existing Pillow is used; no new dependency.
