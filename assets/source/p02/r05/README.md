# R05 bounded candidate sprite sources

This directory contains the image-generation source sheets for
`COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-001`.  Architect Review 10 and adopted
ADR-57 authorize Codex and the approved image-generation tool to create these
identity-critical **candidate** pixels from the exact approved identity and
turnaround references.

Nothing here is operator-approved production art.  The generated frames,
runtime pack, and review media remain candidate evidence until explicit visual
approval.

## Deterministic derivative build

```bash
python3 experiments/p02-embodiment/scripts/build_r05_candidate_pack.py \
  --sheets assets/source/p02/r05/imagegen \
  --out "$PRIVATE_XDG_CACHE/companion-p02-r05/source-pack" \
  --clean
```

The builder selects fixed grid cells, converts the deliberately uniform green
background to alpha, applies uniform full-canvas MON_FRAME_V1 normalization,
creates typed sidecars, and emits review derivatives.  It does not invent
additional anatomy or in-between poses.  Full normalized frames and ingested
runtime packs remain outside Git and are published as workflow artifacts.

`candidate-source-pack-manifest.json` records the exact generated frame hashes.
`generation-provenance.json` records source identities, candidate prompts, and
rejected generations.  The committed review directory is a selected derivative
set; CI regenerates the complete artifact bundle from the source sheets.
