# Architect Deep Dive 01 — Phase 02 Root Blocker and Recovery Plan

## Verdict

`CONTINUE — PRODUCTION BODY AUTHORITY GATE REQUIRED`

- Active directive: `COMPANION-P02-EMBODIMENT-001`
- Reviewed task head: `9a65b8db032c97e13fce5d6a305989d32f2cc879`
- PR: `#9 — OPEN / DRAFT / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Canonical Notion deep dive:
  https://app.notion.com/p/3d8833cb27ff8108a680ef19d8b1cdb5

## Primary conclusion

The main blocker is not Godot, Linux capacity, or the unavailable Openbox
window. The main blocker is the absence of one operator-approved, editable
**production body authority** that turns the two approved raster references
into stable directional construction, real temporal motion, and rendered
acceptance evidence.

The project scaled generated output before that authority existed. Numerical
targets were therefore satisfied by proxies:

- family count instead of animation quality;
- direction count instead of temporal drawings;
- metadata landmarks instead of rendered root/contact evidence;
- declared atlas gutter instead of reserved and extruded pixels;
- generated transition labels instead of visible motion;
- local file paths instead of operator-accessible review artifacts.

## Exact approved sources recovered

The Architect recovered and independently verified the exact operator-approved
native files from project conversation storage:

| Asset | SHA-256 | Dimensions / mode |
|---|---|---|
| `confident_purple_ghost_mascot.png` | `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56` | 1254x1254 RGBA PNG |
| `purple_monster_turnaround_sheet.png` | `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4` | 1448x1086 RGB PNG |

The exact bytes are not yet in a Codex-readable Notion/GitHub source. The
operator transfer requirement is recorded in `APPROVED_REFERENCE_TRANSFER.md`.

## Causal evidence

### Direction is currently used as time

The current clip manifest stores N, NE, E, SE, S, SW, W and NW images in one
`frames` array per family. `MonAvatar` appends that array to one
`SpriteFrames` animation. The mon therefore rotates through directions instead
of performing a motion over time.

The `32 x 8 = 256` result is primarily a directional pose catalog, not 256
temporal animation drawings.

### Timing is not modeled as Godot expects

The current loader passes `duration_ticks / 24.0` as the `add_frame` duration.
Godot defines that argument as relative duration. Absolute frame time depends
on animation FPS and playback speed. Phase 02 needs explicit FPS plus integer
relative tick weights.

### The source model is invented rather than production-authored

The current Pillow generator creates a simplified creature from ellipses,
polygons and lines. It does not use the exact identity image as an editable
construction source. It also moves visible geometry using sway, bob, lean and
gait while leaving declared root/contact landmarks fixed.

### Packaging and publication are proxy claims

The atlas uses flush 1024x1024 cells while declaring a four-pixel gutter.
Generated frames, duplicate Godot copies, atlases and a ZIP are committed to
ordinary Git despite the adopted artifact policy. The operator review package
is referenced through local paths. No dedicated Phase 02 workflow exists, and
the inherited Phase 01 workflow is failing on the generated MonAnimationClip
fixture.

## Systemic diagnosis

This is the same failure class previously seen in the project:

- identifier presence was mistaken for semantic traceability;
- a function call was mistaken for IPC;
- sorted JSON was mistaken for canonical JSON;
- serial reads were mistaken for concurrency;
- control acknowledgments were mistaken for recovery;
- generated category counts were mistaken for exercised behavior.

Phase 02 repeats the pattern visually. The project is measuring what is easy to
count instead of what the end goal requires the user to perceive.

## Required production-body authority

### Source precedence

1. Hard anatomy invariants override all images:
   - exactly two fingers plus one thumb per hand;
   - exactly three toes per foot;
   - no added anatomy.
2. The identity master governs species identity, face, silhouette character,
   palette family, edge treatment, highlight/shadow language and expressive
   presence.
3. The turnaround governs neutral orthographic proportions, limb attachment,
   front/back/profile correspondence and top/bottom construction.
4. Diagonal views and all motion work remain candidates until operator approval.
5. A material conflict in silhouette, face, digit readability or proportion
   stops for one targeted operator ruling.

### Separate semantic axes

Replace ambiguous direction/time use with distinct fields:

```text
facing:
  front | front_right | right | back_right |
  back | back_left | left | front_left

travel_direction:
  independent screen/world movement vector

posture:
  neutral | sit | lie | sleep | ...

variant:
  authored visual variant

frame_index:
  temporal order inside one track

duration_ticks:
  integer 1/24-second timing units
```

Top and bottom approved views are construction references, not normal runtime
facings.

### Authoring architecture

Primary candidate:

- per-facing layered vector/cutout masters using SVG and/or `Polygon2D`;
- bounded `Skeleton2D`/`Bone2D` deformation only where identity remains stable;
- `AnimationPlayer` for authored timing, events and export control;
- discrete authored swaps or complete key poses for silhouette-changing actions;
- deterministic raster export to `MON_FRAME_V1`;
- raster sprite-frame runtime remains unchanged.

Godot is preferred because it is already the approved engine and provides
integrated 2D skeletal deformation, animation timing and SVG import. Blender
Grease Pencil is a fallback only after a bounded comparison proves Godot cannot
preserve the required silhouette. Generative image/video tools may propose
motion ideas but may not become canonical frame authority; current research
still reports identity leakage and temporal drift.

## Recovery gates

### P02-A — exact source and editable body authority

- transfer and verify both exact PNGs;
- build `MON_BODY_SOURCE_V1`;
- author per-facing layered masters, pivots, palette, landmarks and contacts;
- produce approved-view correspondence plus four diagonal candidates;
- obtain operator approval before scaling.

### P02-B — core temporal motion language

Produce only the approval pack:

- three idle/breath variants across eight facings;
- walk and run across eight facings;
- authored turn/orient connectors;
- sit/stand, lie, sleep, wake, listen, think, acknowledge, surprise and
  sensor-degraded proof tracks.

Each track contains real temporal drawings. Publish normal-speed, quarter-speed,
looped, silhouette-only and root/contact-overlay review artifacts.

### P02-C — library scale and runtime

Only after P02-A/P02-B operator approval:

- expand to 32 families and at least 256 real temporal drawings;
- complete correct Godot timing, events, interruption, continuation, transitions
  and BodyA/BodyB handoff;
- implement rendered identity/root/contact QA;
- implement lossless trim, extrusion, real gutters and source reconstruction;
- publish bulk outputs as workflow artifacts;
- pass dedicated Phase 02 CI and evidence validation.

### P02-D — Openbox qualification

The accepted host inventory reports two logical X screens under one X server,
with the 1366x768 Openbox habitat on logical screen 1. Xlib supports an explicit
screen suffix such as `:0.1`.

Before declaring the target absent, perform a bounded read-only probe of the
existing screen 1 with the existing Xauthority. Do not reconfigure the display
or compositor. If access fails, retain the exact XOpenDisplay/Xauthority error
as the real target blocker.

## Operating-model correction for all later phases

Every capability phase must follow:

```text
authority
→ minimum real causal loop
→ strongest disproof tests
→ Architect/operator acceptance
→ scale
→ endurance
```

Every claim must identify:

- canonical owner;
- real input and output path;
- direct observed outcome;
- strongest negative test;
- retained artifact;
- evidence ceiling;
- acceptance authority.

Examples:

- organism: a real need change causes a self-selected action, and observed
  outcome changes organism state;
- memory: a lived event persists across restart and changes a later decision;
- learning: teaching improves held-out behavior rather than setting a flag;
- dream consolidation: memory strength changes without inventing lived facts;
- perception: sensor evidence retains provenance and is checked against ground
  truth;
- care: independent evidence drives deterministic verification and shadow
  escalation.

## Immediate Codex continuation

1. Merge current `origin/main` normally into
   `codex/p02-embodiment-001`.
2. Read Architect Review 01, its source correction, this deep dive and
   `APPROVED_REFERENCE_TRANSFER.md`.
3. Do not generate more bulk body frames.
4. Obtain the two exact native PNGs at the recorded hashes. If they are still
   unavailable through a Codex-readable source, stop with the single transfer
   request in `APPROVED_REFERENCE_TRANSFER.md`.
5. Once present, complete P02-A and P02-B only.
6. Probe the existing X screen 1 through explicit read-only display selection.
7. Remove superseded bulk outputs from the final tree and publish generated
   material as workflow artifacts.
8. Publish operator-accessible construction and core-motion review assets.
9. Return for Architect/operator approval before P02-C.

## Acceptance boundary

This continuation passes only when:

- exact native hashes match;
- one editable production body source exists;
- source precedence is explicit;
- facing, travel, posture and temporal order are separate;
- real temporal core tracks exist;
- rendered identity/root/contact QA passes;
- review assets are directly accessible;
- inherited and dedicated Phase 02 CI are green;
- explicit screen-1 access is tested;
- no full-library or Phase 03 claim is made before approval.

## Capability boundary

Phase 01 remains accepted. Phase 02 remains active and unaccepted. The current
Phase 02 branch contains useful scaffolding and negative evidence, but it does
not yet establish a production body, temporal animation library or visible
aliveness.
