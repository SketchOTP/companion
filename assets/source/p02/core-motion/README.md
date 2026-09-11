# Phase 02 core-motion candidate

This directory contains committed, authored temporal-track specifications and
their deterministic manifest.  The source reference gate is bound to the
native identity SHA-256 `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`
and the turnaround SHA-256 `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`.

Run `python3 experiments/p02-embodiment/scripts/build_core_motion.py --out
<private-output> --clean` to generate full-canvas drawings and trim/extrude
atlases.  Run `validate_core_motion.py` against that output.  The complete
generated corpus is intentionally not committed: CI uploads it as a named
workflow artifact and local export/restore may keep it in an XDG cache.

The package is a visual candidate pending operator approval. It does not
implement organism state, memory, speech, perception, or care policy.
