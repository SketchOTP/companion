# Phase 02 minimal motion proof

This is the bounded P02-A/P02-B approval pack, not the complete Phase 02
library. It contains one `front_left` facing so that direction is a selection
axis rather than a temporal frame index:

- idle/breathe: 6 drawings;
- walk: 8 drawings;
- front → front-left and reverse orient connectors: 3 drawings each; and
- listen and acknowledge reaction proofs: 3 drawings each.

The 26 full-canvas PNG drawings are generated into a private build directory by
`experiments/p02-embodiment/scripts/build_motion_proof.py`. They are not
ordinary-Git payload. The committed manifest and temporal track metadata bind
the generated output to the two exact native references. Selected strips under
`assets/source/p02/review/r02/` are review derivatives only.

`event_expectations.json` describes the events the Godot proof must observe; it
does not self-attest runtime behavior. Operator visual approval is required
before any eight-direction or full-family expansion.

`godot_headless_observation.json` records one local Godot 4.7.2 headless
execution in a temporary project copy. It is bounded `E3_TARGET_TESTED`
evidence of frame-marker and completion signal behavior only.
