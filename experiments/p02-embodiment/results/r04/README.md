# R04-C01 sanitized evidence

This bundle contains only synthetic calibration evidence; it is not production character art.

## Regeneration

1. Use the pinned qualification Python with `Pillow` and `jsonschema`, the
   Rust 1.98.1 toolchain, and the exact Godot 4.7.2 binary. No system package
   or global toolchain change is required.
2. Set `CARGO` and `GODOT_BIN` to those exact local/CI tool paths. Keep any
   private XDG qualification cache (toolchains, temporary pack trees, and
   exports) outside the checkout; no secret or capability environment variable
   is used by this boundary.
3. Run `python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out
   OUT --cargo "$CARGO" --godot "$GODOT_BIN"`. The command builds the
   synthetic source twice, runs intake and its negative matrix, performs the
   schema/Rust crosswalk, validates the actual generated pack, and executes the
   Godot test before writing sanitized JSON, provenance, and this README.
4. Run `python3 experiments/p02-embodiment/scripts/validate_r04_results.py
   --results OUT --tamper-negative`; it independently checks all hashes and
   expected outcomes, then must report `status: PASSED` and five rejected
   tamper mutations.
5. Keep generated PNGs, content-addressed copies, caches, binaries, export
   archives, restored trees, corruption copies, and any raw host output outside
   Git. Only the sanitized JSON bundle, hashes, and regeneration procedure are
   committed.

`provenance.json` records observed timestamps, checked-out Git commit, fixture/reference hashes, result hashes, runtimes, commands, and the E3 evidence ceiling.
