# R04-C01 contract correction record

## Boundary

`MON_AUTHORED_FRAME_SOURCE_PACK_V1` is immutable Architect input. It contains
only source-frame bytes, sidecars, authoring provenance, approval state, and
source relationships. It does not contain content-addressed storage or runtime
paths. `MON_INGESTED_FRAME_PACK_V1` is the validated derived build/runtime
document. `MON_FRAME_INTAKE_RECEIPT_V1` records validation, source/output tree
digests, byte equality, and publication state. Runtime relationships are never
written back into the source manifest.

## Source layout

```text
source-pack/
  pack.json                         # source profile
  frames/<family>__<facing>__<posture>__vNN__fNNN.png
  sidecars/<same-stem>.frame.json
intake-output/                       # fresh, staged, atomically renamed
  source/                            # byte-for-byte source copy
  sources/sha256/<prefix>/<hash>.png # content-addressed copy
  runtime/frames/<filename>.png      # derived/runtime relationship
  pack.json                          # ingested profile
  receipt.json                       # intake receipt
```

## Typed semantics

Tracks carry `selection_facing`, `entry_facing`, and `exit_facing`; each frame
carries `facing`, `posture`, and optional `action_phase`. Canonical landmarks
are explicit `visible`, `occluded`, or `not_applicable` states, with a point
required only for `visible`. IDs, filenames, sidecars, and source hashes are
unique unless a frame explicitly names `reuse_of`; held drawings use larger
integer `duration_ticks`, never duplicate source files.

The request profile `phase02_bounded_motion_proof_v1` enforces the bounded
neutral, idle, walk, orientation, and listen/acknowledge family counts,
endpoint facings, and event presence. The synthetic profile
`synthetic_r04_test_v1` is used only for calibration and CI; it is not
production art.

## Intake and runtime gates

Intake rejects invalid PNG signature/IHDR, non-8-bit or non-RGBA PNGs, missing
sRGB signalling, blank or opaque images, nontransparent perimeter, safety-region
violations, malformed landmarks, duplicate identities, profile incompleteness,
and event/contact/timing mismatches. Validation occurs in a sibling staging
directory; only a complete receipt is published with `os.replace` into an
absent or empty destination. No source bytes are edited.

Godot consumes only the ingested profile, verifies pack/track/reference hashes,
relationship uniqueness and containment, validates approval eligibility and
frame hashes, and observes `RenderingServer.frame_post_draw` (or the explicitly
bounded headless scene-tree fallback) before `first_frame_render_committed`.
Physical display presentation is outside this gate.

## Evidence status

The committed fixtures are synthetic and intentionally obvious. Tests prove the
intake/runtime boundary and failure behavior only. No production body, approved
motion, visual aliveness, or Phase 02 acceptance is claimed. The final handoff
status after exact-head validation is `READY_FOR_ARCHITECT_FRAME_PACK`.
