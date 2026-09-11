# R04 authored-frame boundary evidence

This sanitized bundle contains synthetic-only bounded E3 intake and runtime evidence. It does not contain or approve production character art.

Regenerate with the exact Rust 1.98.1 and Godot 4.7.2 qualification artifacts:

```bash
python3 experiments/p02-embodiment/scripts/run_r04_evidence.py --out OUT --godot "$GODOT_BIN"
python3 experiments/p02-embodiment/scripts/validate_r04_results.py --results OUT --tamper-negative
```

Generated PNGs, content-addressed storage, Cargo targets, Godot caches, local export ZIPs, restored trees, and tamper copies remain outside Git.
