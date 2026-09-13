# R03 superseded result bundle

Status: `REJECTED_AS_PRODUCTION_ART` / `NEGATIVE_EVIDENCE_ONLY`. These files
preserve the failed R03 claims and must not be used as a candidate pack or
runtime fallback.

This committed bundle is a compact, sanitized candidate record. It contains
the generated temporal-track/pose/manifest/event metadata and validator output;
the 28 full-canvas frame PNGs remain caller-owned temporary output and are not
ordinary Git history. Selected review derivatives are under
`assets/source/p02/r03/review/`.

## Rebuild and verify

From a clean checkout with Python 3 and the already available Pillow and
jsonschema runtimes:

```bash
OUT="$(mktemp -d /tmp/companion-p02-r03.XXXXXX)"
python3 experiments/p02-embodiment/scripts/build_r03_motion.py --out "$OUT" --clean --negative-evidence
python3 experiments/p02-embodiment/scripts/validate_r03_motion.py --out "$OUT" --tamper-negative > /tmp/r03-validation.json
R03_TRACKS_PATH="$OUT/temporal_tracks_v2.json" cargo test --workspace --locked
GODOT=/path/to/Godot_v4.7.2-stable_linux.x86_64
"$GODOT" --headless --path godot --script res://r03_temporal_playback_test.gd -- --out="$OUT" > /tmp/r03-godot.log
! grep -q 'ERROR:' /tmp/r03-godot.log
```

The private output directory, generated frame corpus, Godot cache/UID files,
and logs stay outside Git. The Godot binary must be the exact verified
`4.7.2.stable.official.ed1daf0bf`; no project or host configuration is changed.
The review package is candidate-only and capped at bounded engineering/visual
evidence (`E3_TARGET_TESTED`), not identity approval or product capability.
