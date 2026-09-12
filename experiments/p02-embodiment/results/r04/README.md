# R04-C02 sanitized evidence

This bundle is synthetic calibration evidence only; no production character pixels are generated.

## Regeneration

1. Use the pinned qualification Python with Pillow/jsonschema, Rust 1.98.1, and the exact Godot 4.7.2 binary when available. Set `CARGO` and `GODOT_BIN` to private cache paths; keep tools, temporary packs, exports, and raw host output outside Git.
2. Run `python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out OUT --cargo "$CARGO" --godot "$GODOT_BIN"`. It builds the complete `phase02_bounded_motion_proof_v1` pack twice, performs intake and negative tests, validates schemas, round-trips the actual generated pack through Rust, runs local export/restore, and records Godot status.
3. Run `python3 experiments/p02-embodiment/scripts/validate_r04_results.py --results OUT --tamper-negative`. The validator independently checks profile/count/hash equations and tamper mutations; it must exit zero only for a complete valid result set.
4. Generated PNGs, CAS copies, caches, binaries, archives, restored trees, and raw logs remain outside Git. Commit only sanitized JSON, hashes, and this procedure.
