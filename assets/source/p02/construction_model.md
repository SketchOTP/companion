# Mon construction model candidate — `MON_CONSTRUCTION_V1`

This is an authored, identity-locked construction model derived from the two
approved references. It is a candidate for operator review, not a replacement
for the canonical identity master.

## Native source gate (2026-09-11)

The construction basis is the exact native operator-approved identity source,
not the historical SVG derivative:

- `assets/source/p02/references/identity-approved.png` — 1254×1254 RGBA,
  SHA-256 `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`.
- `assets/source/p02/references/turnaround-approved.png` — 1448×1086 RGB,
  SHA-256 `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`.

The deterministic core-motion builder reads and hashes the native identity PNG
before every export.  It normalizes the source into MON_FRAME_V1 with one
fixed, documented transform, then applies only bounded local band deformations
around the fixed source root.  The turnaround remains a six-view
correspondence authority and is never rasterized into a substitute identity.

All diagonals and temporal drawings are candidates pending operator visual
approval.  The native files are preserved byte-for-byte; no recompression or
runtime asset mutation is permitted.

## Grid and silhouette

- Work in a 1024×1024 square with the MON_FRAME_V1 root at `(512,896)`.
- The body is a rounded, unclothed purple form occupying approximately
  `x=260..764`, `y=420..920`; a seven-spike flame head stays inside the source
  safety rectangle `x=64..960,y=32..960`.
- The head silhouette is asymmetric by authored pose and direction; no runtime
  mirror is used as a distinct source.
- Ground contact is represented by two planted foot landmarks and a soft
  purple shadow footprint. Root translation is prohibited.

## Palette roles

| Role | Value | Use |
|---|---|---|
| outline | `#261444` | silhouette and limb separation |
| body | `#8b54d9` | primary purple fill |
| light | `#b879f2` | controlled cel highlight and pupils |
| shadow | `#5b3299` | controlled purple shadow shapes |
| eye | `#090711` | black eye fields |
| pupil | `#fff9ff` | white pupils |
| mouth | `#2b1238` | small simple mouth |

## Anatomy invariants

Every candidate must retain exactly two fingers plus one thumb on each hand and
exactly three toes on each foot. The head has edge spikes but no ears, horns,
muzzle, nose, teeth, clothes, accessories, symbols, or extra limbs. Face layers
may vary gaze, blink, and mouth presentation without changing identity.

## Pose limits

Squash/stretch is bounded to ±4% in source authoring; tilt is bounded to ±12°;
limb overlap may change but may not hide or invent digits; perspective offsets
remain within the turnaround's six-view proportions. Diagonal views are
explicitly candidate `front_left`, `front_right`, `back_left`, and `back_right`
views and are not operator-approved until visual review.

## Landmark set

`root`, `head`, `left_foot`, `right_foot`, `left_hand`, `right_hand`,
`gaze_center`, and `mouth_center` are recorded per drawing. Contacts are spans
over integer 1/24-second ticks; all authored source definitions carry a source
revision and checksum through the pack manifest.

## Core temporal-track package

`core-motion/temporal_tracks.json` defines one track per
`body_revision + stage + family + direction + posture + variant`.  Direction is
therefore a selection key, never a temporal frame index.  Idle A/B/C, walk, and
run have independent ordered drawing sequences; turn connectors and focused
proof tracks are separately identified.  Generated PNGs are written to a
private build directory and are versioned as CI artifacts, while this source
manifest and the review sheets remain in Git.
