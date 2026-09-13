# R06-C02 grounded real-art integration result

## Verdict

`SUBMITTED_FOR_ARCHITECT_REVIEW` — no new character pixels were generated.

## Frozen source and retained boundary

The C01 selection remains 58 immutable native 1254×1254 RGB runtime masters,
24 tracks, and 283 frame slots. Grounding regenerated only pack/sidecar
metadata; source bytes remain hash-identical to their manifest entries. The
source-pack SHA after deterministic metadata regeneration is
`1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.

## Grounding and world contact

`ground_r06_c02.py` measures the actual lowest non-black contour and records
visible sole candidates, explicit occlusion/not-applicable states, source
hashes, method, review state, and representative overlay evidence. Walk
support is derived from the labelled near/far sole evidence, not a fixed
bounding-box fraction. The left and right stitched start→loop→stop plans are
continuous; all six walk-track plans report maximum planted-contact slip
`0.0 px` at 24 Hz with no source mutation.

## Validation

`validate_r06_c02.py` passes the source schema, source hashes and dimensions,
grounded provenance, support geometry, 24 Hz plans, and eight executable
negative mutations (heuristic placeholder, missing support, one-tick contact,
slip >2 px, root discontinuity, readback-only render commitment, sequence
boundary discontinuity, and viewport-corner-only compositor evidence).

Local immutable intake, injected mid-intake failure, ingested-schema
validation, and sanitized integration recording pass. Rust and Godot exact-head
execution remain hosted gates; the Godot gate is strict about
`RenderingServer.frame_post_draw` and must not be weakened to a readback
fallback.

## Limits

These are E3 target-tested candidate observations only. The visual package is
not re-approved, Phase 02 is not accepted, and transition/Openbox endurance
work remains deferred to the Architect's next gate.

## Hosted exact-head result — 2026-09-13

Implementation head `94b59cf76fc046abe28d6dd1b67359a803af8544` passed the
canonical R06 workflow `34767677664`, inherited Phase 02 workflow
`34767677668`, and Phase 01 workflow `34767677707` on that exact SHA. R06
artifact `10320777649` is published. Runtime-pack SHA is
`6d20431d72d182a547409df310e2ec69db53639aafacb2878476f8420510474f`.
Godot 4.7.2 on Xvfb/llvmpipe observed `RenderingServer.frame_post_draw`,
168 semantic events, 624 compositor samples, zero Godot ERROR lines, and one
retained V-Sync warning. The runner bounds missing-signal execution with a
300-second timeout and the script fails fast on the first unobserved boundary;
no fallback is relabeled as render commitment. This remains bounded candidate
evidence; transition, Openbox qualification, and Phase 02 acceptance were not
run.
