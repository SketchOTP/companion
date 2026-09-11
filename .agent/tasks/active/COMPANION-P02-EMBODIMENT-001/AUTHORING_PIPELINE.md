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
