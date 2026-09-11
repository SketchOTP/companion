# AUTHORING PIPELINE — COMPANION-P02-EMBODIMENT-001

## Alternatives

Compare layered vector/shape authoring and controlled full-frame raster
keypose/in-between authoring. Record evidence, failure modes, rights, exact tool
versions, determinism, identity quality, and rejected alternatives.

## Selected pipeline

Document:

- canonical authored source representation;
- part/body revision ownership;
- frame pose/in-between representation;
- deterministic MON_FRAME_V1 export;
- landmark generation;
- transparent-edge handling;
- clip and event generation;
- trim/extrude/atlas packing;
- pack construction;
- clean-room rebuild;
- local export/restore;
- artifact publication;
- repository binary-budget enforcement.

## Reproducibility

Record exact commands, environment, tool versions/integrity, source hashes,
result hashes, normalized nondeterminism if any, and byte-for-byte or semantic
reproducibility result.

## Executed result

Controlled raster key-pose/in-between authoring was selected for this bounded
candidate because Pillow 10.2.0 is available locally, produces deterministic
RGBA PNG bytes, and keeps runtime animation raster-frame based. Layered vector
shape authoring remains a viable future source format. `build_assets.py` emits
256 unique 1024² frames, landmarks, clip metadata, 16 4096² atlases, and a zip
pack; `validate_assets.py` performs fail-closed canvas, alpha, safety,
uniqueness, timing, direction, and pack checks. Rebuilding reproduced the
manifest and source hashes. Generated binaries are versioned artifacts;
authored sources and manifests are Git-authoritative.
# Architect Review 01 correction — deterministic source path (2026-09-11)

The selected authoring path is reference-grounded raster export from the exact
native identity source with explicit stable family/direction/frame parameters.
`build_core_motion.py` writes all generated frames and trim/extrude atlases to a
private caller-provided output.  Byte-identical clean-process rebuilding is
validated before any artifact publication; no runtime rig or authoring tool is
a production dependency.

## Architect Review 02 correction

Two explicit authoring candidates are retained: the layered vector/path source
(`mon_body_source_v1.svg`) and the layered raster key-pose source
(`raster_key_pose_source_v1.json`). The bounded comparison records raster proof
rendered and vector proof `NOT_RUN_EXTERNAL_RASTERIZER_UNAVAILABLE` because no
`resvg` executable is installed. This is a recorded limitation, not an adopted
dependency or a selection decision.
# R03 authoring correction

The bounded proof uses explicit part poses from `MON_BODY_SOURCE_V2`, a
deterministic MON_FRAME_V1 raster bake, landmark/contact sidecars, and
normal/quarter-speed, silhouette, root/contact, and ordered-strip review
derivatives. The bake contains no reference-pixel copy or whole-image warp.
Godot remains the editable source and raster `SpriteFrames` runtime; the Python
mirror exists only because the pinned dummy renderer cannot expose a readable
SubViewport texture. Full atlas/pack and library scale remain deferred.
# R04 authorship and intake boundary

The AI Architect authors identity-critical full-frame source poses. Codex does
not generate, warp, repair, or interpolate production pixels. The sole active
pipeline is immutable source validation, byte-preserving content-addressed
copy, separate deterministic derivatives, local export/restore, and Godot
runtime integration. R02/R03 procedural authoring paths are superseded
negative evidence and never a fallback.
