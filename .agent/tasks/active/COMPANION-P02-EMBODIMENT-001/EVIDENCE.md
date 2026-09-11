# EVIDENCE — COMPANION-P02-EMBODIMENT-001

## Source register

For every materially used external source or tool record title, owner, date,
URL, version/commit, integrity, license, maintenance, offline behavior,
transitive dependencies, evidence grade, established fact, limitation, project
inference, recommendation, and recheck trigger.

## Project evidence

Bind:

- reference files and hashes;
- construction source revision;
- authored source hashes;
- frame/landmark/clip manifests;
- rejected-frame records;
- pack/atlas hashes;
- QA reports;
- review-sheet hashes;
- Godot scene/resource hashes;
- contract fixtures/results;
- 10,000-case result;
- two-hour playback result;
- performance/memory result;
- CI runs/artifacts;
- export/restore result;
- final implementation commit and ancestry.

## Evidence ceiling

Separate direct observations, reproduced builds, target tests, operator visual
approval, hypotheses, and deferrals. Never treat generated art, automated QA, or
playback as operator approval or organism/product capability.

## Bound evidence package

- Reference metadata and inspected derivatives: `E1_OBSERVED`.
- Deterministic source/export/atlas/pack and automated QA: `E2_REPRODUCED`.
- Godot headless layered-avatar test and 10,000-case transition runner:
  `E3_TARGET_TESTED` (synthetic presentation only).
- Target-host Openbox habitat and two-hour playback: `NOT RUN` because the
  current session exposes a different display topology; no host settings were
  changed.
- Operator identity/motion approval: `PENDING`.

## Architect Review 01 correction evidence — 2026-09-11

The exact native references supplied through the Codex-accessible project
transfer were verified byte-for-byte before the new build:

- identity: `86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`,
  1254×1254 RGBA;
- turnaround: `3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`,
  1448×1086 RGB.

The previous 256-image directional catalog remains rejected historical
evidence.  The current candidate package is `MON_TEMPORAL_TRACKS_V1`: 66
independent tracks and 334 generated MON_FRAME_V1 drawings (166 byte-distinct
body outputs after duplicate removal), with idle A/B/C, walk, run, turn, and
focused proof tracks.  Direction is a track-selection key, not a temporal
frame index.  Core generation and validation are reproducible in private
outputs; the generated corpus and atlases are not part of ordinary Git.

The trim/extrude validator measured real 4 px reserved gutters and source
trim rectangles.  Automated rendered-pixel checks returned zero errors for
canvas, alpha, safety bounds, landmark root, and frame hashes.  These are
bounded `E2_REPRODUCED` candidate observations, not visual approval.

The dedicated Phase 02 workflow is now present but its hosted run and the
dedicated Openbox two-hour target run remain pending.  Godot headless playback
is not claimed locally because the exact 4.7.2 executable is not installed in
this worktree; the workflow stages it ephemerally after hash verification.
