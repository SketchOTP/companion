# ANIMATION LIBRARY — COMPANION-P02-EMBODIMENT-001

## Coverage summary

Record exact totals for:

- semantic clip families;
- unique authored body-frame sources;
- exact duplicates rejected;
- near duplicates dispositioned;
- frame totals by direction/action/posture;
- eye/gaze/blink overlays;
- mouth overlays;
- boot-critical and on-demand packs;
- transition connectors;
- rejected frames and reasons.

## Required floor

- 32 clip families.
- 256 unique body-frame sources excluding eye/mouth overlays.
- Eight direction identifiers.
- Eight-direction idle/breath, orient/turn, walk, and run.
- 24 eye/gaze/blink overlays.
- 8 mouth overlays.
- 3 materially distinct high-frequency idle variants.

## Clip catalog

For every clip record ID, version, source revision, direction, posture,
behavior tags, affect/energy range, frame count, durations, loop/seam, root
motion, landmarks, contacts, connectors, interrupt ranges, events, overlays,
repeat/cooldown/rarity, pack, validation checksum, and visual-review status.

## Direction policy

Record legal direction fallback and the approval state of all diagonal art. No
unapproved mirror may be counted as production left/right coverage.

## Executed result

The candidate manifest records 32 semantic families, 256 unique body-frame
sources, eight direction identifiers, 24 eye overlays, eight mouth overlays,
and three distinct high-frequency idle families. Every family declares all
eight directions with explicit fallback metadata. Frame hashes are unique; no
metadata-only, translated, scaled, or mirrored duplicate is counted. These
remain visual presentations and do not implement organism, speech, memory,
perception, or care policy.
# Architect Review 01 correction — temporal core candidate (2026-09-11)

The previous one-frame-per-direction catalog is retained as rejected history.
`assets/source/p02/core-motion/temporal_tracks.json` now defines independent
temporal sequences keyed by body revision, stage, family, direction, posture,
and variant.  The core candidate contains idle A/B/C, walk, run, turn, and
focused proof tracks; direction is not a temporal frame.  Full 32-family
completion remains deferred until operator visual approval.

## Architect Review 02 correction

The former 32-family directional catalogue is superseded and must not be
counted as temporal animation. The active proof contains exactly six temporal
tracks at one `front_left` facing: idle/breathe (6), walk (8), two orient
connectors (3 each), listen (3), and acknowledge (3), for 26 drawings. Full
direction and family expansion waits for operator selection of the canon and
motion language.

## R04 superseding boundary

No R02 or R03 frame is candidate production animation. The production library
count is zero until an Architect-authored `MON_AUTHORED_FRAME_PACK_V1` is
accepted through byte-preserving intake and operator visual approval. R04 uses
only one approved-identity import smoke frame and an unmistakably geometric
`synthetic_test_only` timing pack. Full family, facing, and motion-language
coverage is deferred; no procedural character-art fallback remains.
