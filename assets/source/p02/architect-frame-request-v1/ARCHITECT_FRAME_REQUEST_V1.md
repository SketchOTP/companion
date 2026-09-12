# ARCHITECT_FRAME_REQUEST_V1

Status: `READY_FOR_ARCHITECT_INPUT`
Production-art authority: AI Architect
Visual approval authority: Operator
Intake/integration authority: Codex

This landing contract requests immutable, full-frame source drawings. Codex
must not redraw, repair, interpolate, warp, crop, resize, recolor, recompress,
or infer missing information. A rejected delivery is returned to its art
authority unchanged.

## Canonical frame profile

Every source frame must be a 1024 x 1024, 8-bit RGBA PNG with an sRGB chunk,
transparent background, root `(512, 896)`, baseline `y = 896`, and all drawable
pixels inside `x = 64..960, y = 32..960`. Source cropping and encoded
translation are prohibited. Timing is an integer number of 1/24-second ticks.

The pack must cite these immutable approved references:

- Identity: `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`
- Turnaround: `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`

## Requested bounded landing pack

| Family | Facing / transition | Source frames | Required event intent |
|---|---|---:|---|
| `neutral_construction` | `front` | 1 | none |
| `neutral_construction` | `right` profile | 1 | none |
| `neutral_construction` | `front_left` | 1 | none |
| `idle_breathe` | `front_left` | 6-8 | optional `breath_apex` |
| `walk` | `front_left` | 8 | `footfall_left`, `footfall_right` |
| `orient_front_to_front_left` | `front` to `front_left` | at least 4 | `facing_changed` on final drawing |
| `orient_front_left_to_front` | `front_left` to `front` | at least 4 | `facing_changed` on final drawing |
| `listen_acknowledge` | `front_left` | 6 | `attention_acquired`, `acknowledge`, `settled` |

This is an intake request, not approval. Initial art must use
`approval_state: candidate`. Only the Operator may change that state to
`operator_approved` through durable authority.

## Exact names and layout

```
architect-frame-pack-v1/
├── pack.json
├── frames/
│   └── <family>__<facing>__<posture>__v<variant-02>__f<frame-03>.png
└── sidecars/
    └── <same-stem>.frame.json
```

Examples:

```
frames/walk__front_left__walking__v01__f000.png
sidecars/walk__front_left__walking__v01__f000.frame.json
```

Names are lowercase ASCII. The manifest lists filenames relative to the pack
root. A source hash is the SHA-256 of the exact PNG bytes. Each sidecar repeats
the frame identity, source hash, duration, root, landmarks, and provenance;
the intake command requires exact semantic agreement with `pack.json`.

## Required landmarks

Each drawing supplies integer source-space points for:

- `root` (must be exactly `512,896`)
- `head`
- `eye_left`, `eye_right`
- `hand_left`, `hand_right`
- `foot_left`, `foot_right`

Landmarks are authored facts. Intake never infers them.

## Contacts, timing, holds, and events

Contacts are half-open tick spans `[start_tick, end_tick)` and identify one of
`foot_left`, `foot_right`, `hand_left`, or `hand_right` with state `planted`,
`swing`, or `clear`. An authored `planted` span means the named contact is
intended to remain within two source pixels; later rendered QA verifies it.

`duration_ticks` is an integer from 1 through 240. At explicit 24 FPS, a value
of 1 is 1/24 second and 2 is 2/24 second. Identical held drawings are allowed
only by increasing `duration_ticks`; duplicate files must not be used to pad a
track. Events use a stable lowercase name, absolute track tick, and frame
index. Events must be in nondecreasing tick order and point to an existing
frame.

## Approval and rejection

Allowed states are exactly:

- `candidate`
- `operator_approved`
- `rejected`
- `synthetic_test_only`

Production packaging accepts only `operator_approved`. Review intake accepts
`candidate` or `operator_approved`. Test intake accepts only
`synthetic_test_only`. Approval is read from validated manifest content and is
never inferred from a file or directory name.

Stable intake rejection codes include:

`manifest_invalid`, `manifest_incomplete`, `filename_invalid`,
`sidecar_missing`, `sidecar_mismatch`, `source_missing`, `source_hash_mismatch`,
`wrong_dimensions`, `wrong_mode`, `missing_srgb`, `opaque_background`,
`safety_region_violation`, `root_mismatch`, `landmark_missing`,
`contact_invalid`, `duration_invalid`, `event_order_invalid`,
`approval_ineligible`, and `track_checksum_mismatch`.

## What Codex returns after landing

Intake copies each PNG byte-for-byte to content-addressed local storage,
recomputes its hash, and produces a separate runtime derivative manifest. It
records input and stored hashes plus byte equality. Generated import metadata,
review sheets, atlases, and runtime resources remain derivatives; the source
files are immutable and remain independently exportable/restorable by hash.

## R04-C01 machine-checkable landing profile

The source manifest is `MON_AUTHORED_FRAME_SOURCE_PACK_V1` and contains only
Architect-authored facts. Runtime paths, content addresses, atlas locations,
and generated hashes are never written into this source document. Codex emits a
separate `MON_INGESTED_FRAME_PACK_V1` and a `MON_FRAME_INTAKE_RECEIPT_V1` after
validation.

The bounded proof request requires neutral front, right profile, and front-left
masters (one frame each), `idle_breathe` (6–8), `walk` (8), both orientation
directions (at least 4 each), and `listen_acknowledge` (6). Every track has
typed `selection_facing`, `entry_facing`, and `exit_facing`; every frame has
typed `facing`, `posture`, optional `action_phase`, integer `duration_ticks`,
source-asset ID/hash, and a matching sidecar.

Each frame supplies the complete canonical landmark map: `root`,
`ground_contact_left`, `ground_contact_right`, `head_center`, `eye_midpoint`,
`eye_left`, `eye_right`, `mouth_center`, `hand_left`, `hand_right`, `foot_left`,
`foot_right`, `attachment_back`, `attachment_front`, `interaction_focus`,
`action_anchor`, and `object_anchor`. A landmark is `{state, point}`; `point`
is present only for `visible`, and is null for `occluded` or `not_applicable`.
Orientation endpoints and required events (`facing_changed`,
`attention_acquired`, `acknowledge`, `settled`) are checked before intake.

Exact filenames are
`<family>__<facing>__<posture>__v<NN>__f<NNN>.png` with a matching
`.frame.json` sidecar. Holds use increased duration ticks and explicit
`reuse_of`; accidental duplicate hashes, missing files, unsafe PNG profiles,
ineligible approval states, invented landmarks, and source/runtime drift are
rejected. Referenced same-track holds are allowed only through `reuse_of` with
the same source hash and a longer duration; unreferenced duplicate hashes,
missing files, unsafe PNG profiles, ineligible approval states, invented
landmarks, and source/runtime drift are rejected. Production accepts only
`operator_approved`; candidate content is
review-only and synthetic content is test-only.

## R04-C02 executable profile (supersedes the earlier prose profile)

The machine identity of this request is the following set of unique roles;
requirements are keyed by the complete tuple, never by family alone:

```text
neutral_construction/front       entry=front       exit=front       frames=1
neutral_construction/right       entry=right       exit=right       frames=1
neutral_construction/front_left  entry=front_left  exit=front_left  frames=1
idle_breathe/front_left          entry=front_left  exit=front_left  frames=6..8
walk/front_left                  entry=front_left  exit=front_left  frames=8
orient_front_to_front_left       entry=front       exit=front_left   frames=4
orient_front_left_to_front       entry=front_left  exit=front       frames=4
listen_acknowledge/front_left    entry=front_left  exit=front_left  frames=6
```

The first and last frame of each track must equal its declared entry and exit
facing. Completion is `once` for neutral, orientation, and listen tracks, and
`loop` for idle and walk. The walk event sequence is exactly
`footfall_left`, `footfall_right`; each orientation track has exactly one
`facing_changed` event on its final drawing; listen/acknowledge has exactly
`attention_acquired`, `acknowledge`, `settled` in that order. This exact role
table is the `phase02_bounded_motion_proof_v1` profile used by intake and CI.
