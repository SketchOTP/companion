# Architect Review 04 — R03 Rejected; Restore Architect Visual Authorship

## Verdict

`REPLAN — R03 NOT ACCEPTED`

- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed head: `1183795843f26de6b69f0a2a0828ee288f32e415`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Canonical Notion review:
  https://app.notion.com/p/3d8833cb27ff81b0ae0bd8815885e2f6

Exact references, final-tree generated-output cleanup, the track/timing direction,
artifact publication, and CI plumbing are retained. The submitted visual source,
identity fidelity, motion language, source-of-truth claim, contract/runtime proof,
and operator-review readiness are rejected.

## Root correction

The project incorrectly assigned identity-critical artwork to the coding agent.
Canonical R04 and R10 assign the original sprite library to the AI Architect
under operator approval. Codex is the live-codebase authority and implementation
agent; it is not the visual-identity author or acceptance authority.

The fixed boundary is:

- AI Architect: creates or edits identity-critical source art and temporal key
  poses from the approved references, and records provenance.
- Operator: approves identity, construction, diagonal appearance, and motion
  language.
- Codex: performs byte-preserving intake, typed contract validation,
  deterministic derivatives, packaging, runtime integration, CI, and evidence.
  It may create only obviously synthetic non-product fixtures.
- Godot: executes approved sprite tracks; it does not own identity truth.

## Retained evidence

Do not repeat unless an input changes:

- The exact approved identity and turnaround PNGs are committed and verified.
- The prior bulk frame/atlas/pack output is absent from the final branch tree.
- The R03 workflow and inherited Phase 01 workflow are green at the reviewed
  head.
- The separate temporal-track and 24 Hz direction are useful scaffolding.
- The R03 artifact contains changing raster frames and useful review-publishing
  infrastructure.

These facts do not establish accepted production art or motion.

## Independent findings

### The rendered character is not the approved mon

The approved character uses a smooth integrated silhouette, broad rounded limbs
and feet, sweeping curved flame spikes, soft cel-shaded volume, and integrated
hand/foot anatomy. R03 uses a polygon torso, segmented thin limbs, bead-like
digits and toes, angular eye fields, and separate triangular crown spikes. It is
a visibly different construction and rendering language.

This is an Architect rejection. The operator should not be asked to choose among
assets that are already outside the approved identity boundary.

### `MON_BODY_SOURCE_V2` is not a functional production rig

`mon_body_source_v2.tscn` contains a `Node2D` named `Rig` and a hierarchy of
`Bone2D` nodes, but no `Skeleton2D`, `Polygon2D`, `Sprite2D`, textured mesh,
weights, populated replacement drawings, or authored AnimationPlayer library.
The visible body is drawn separately by procedural GDScript.

Godot's official 2D skeletal workflow uses visual Polygon2D pieces with a
Skeleton2D and Bone2D hierarchy. A node-name hierarchy without bound visual
geometry is not a production rig.

### The claimed Godot source of truth is not the frame source of truth

`build_r03_motion.py` says the Godot scene is authoritative, but it does not run
that scene to bake the PNGs. It contains a second hard-coded renderer in Python
using circles, lines, and polygons. The body JSON is loaded, but its geometry is
not used to render the frames.

The branch therefore contains two independently implemented creatures:

1. a GDScript procedural drawing; and
2. a Python procedural drawing.

They can drift and neither is identity-faithful. Production must have one visual
source of truth.

### Motion and facing remain insufficient

The walk now moves feet and arms, but it is a mechanical procedural puppet rather
than an approved motion study. The orientation tracks change head width/position
while the torso, legs, and whole-body facing remain effectively frontal. The
listen/acknowledge sequence has limited body-language differentiation.

Frame uniqueness is not visual acceptance.

### Contract and CI evidence remains partly vacuous

- Rust uses broad `serde_json::Value` fields for landmarks, contacts, events,
  and timing rather than strongly typed structures.
- The generated-track Rust test returns early when `R03_TRACKS_PATH` is absent.
  CI runs Cargo tests before generating the R03 pack and does not provide that
  path, so the actual generated pack is not proven to round-trip through Rust.
- `contract_closeout.py` reports no wire executions.
- The director can form and emit `started` before proving that the requested
  track loaded and became visible.
- The Godot test exercises local selection/playback helpers rather than the
  complete director/avatar/transport path and exact event sequence.

Green CI protects the current assertions, not the full R03 claim.

### The review package is incomplete

The artifact contains motion GIFs and strips, but not the required
source-hierarchy/pivot sheet, neutral front/profile/front-left construction
sheet, or anatomy/palette/silhouette sheet derived from the alleged V2 source.
The required operator decision cannot be made from this package.

## Architect production decision

Identity-critical body motion will use Architect-authored full-frame raster key
poses, with layered eye, mouth, held-object, and accessory overlays where they
preserve quality. Codex may not generate production character pixels with
procedural polygons, whole-image warps, or a coding-agent-authored puppet.

A cutout or hidden 3D rig may later assist in-betweens only after a separate
bounded experiment proves that it preserves the approved identity. It is not
adopted in this directive.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R04

## Objective

Remove coding-agent visual invention from the production path and deliver a
lossless, strongly typed, fail-closed intake/runtime pipeline for an
Architect-authored sprite proof pack. Return
`READY_FOR_ARCHITECT_FRAME_PACK`. Do not generate new character artwork.

## Why this is next

The exact references and CI plumbing are solved. The missing input is approved
art, not another geometry algorithm. The fastest correct path is to lock the
engineering boundary, then ingest the small frame pack created by the Architect
under the operator-approved visual bible.

## Authoritative basis

- Canonical project and end goal.
- R04 Embodiment, Animation, and Social Presence.
- R10 Godot Sprite Embodiment and Asset Production Contract.
- Approved identity master and turnaround.
- Architecture v1.0.
- Architect Reviews 01–03 and this Review 04.
- ADR-54 generated-asset storage policy.
- Adopted visual-authorship boundary recorded with this review.
- Accepted Phase 01 boundary.
- Current PR #9, Issue #8, and active task packet.

## Scope

### A. Preserve and supersede

1. Merge current `origin/main` normally into
   `codex/p02-embodiment-001`.
2. Retain exact references, final-tree bulk-output cleanup, useful 24 Hz/track
   concepts, artifact publication, and green Phase 01 infrastructure.
3. Mark `MON_BODY_SOURCE_V2`, its TSCN/GDScript renderer, the Python duplicate
   renderer, R03 visual outputs, and R03 production-art claims as superseded
   negative evidence.
4. Remove procedural character-art generation from the candidate production
   path. Preserve public history; do not rebase or force-push.

### B. Define `MON_AUTHORED_FRAME_PACK_V1`

The contract must contain:

- immutable 1024x1024 RGBA source frames supplied by the Architect;
- approved-reference hashes and art-generation/edit provenance;
- body revision, stage, family, facing, posture, variant, frame index,
  duration ticks, source-frame hash, landmarks, contacts, events, entry/exit
  posture, interruption ranges, pack revision, and approval state;
- explicit candidate, operator-approved, rejected, and synthetic-test-only
  states;
- no automatic resize, crop, recolor, warp, redraw, in-between, or anatomy
  repair.

Create exact landing paths and `ARCHITECT_FRAME_REQUEST_V1.md` for:

- neutral front, profile, and front-left construction masters;
- 6–8 front-left idle/breathe frames;
- eight front-left walk frames;
- at least four front-to-front-left and four reverse orientation frames;
- six listen-to-acknowledge frames.

Intended holds may reuse a source hash only when explicitly declared. Accidental
duplicates fail.

### C. Preserve source pixels exactly

Implement an intake command that:

- verifies filename, dimensions, RGBA/sRGB, alpha, hash, source authority,
  root, safety region, and sidecar completeness;
- rejects rather than mutates invalid source frames;
- copies source bytes losslessly into content-addressed build storage;
- generates review derivatives, atlases, SpriteFrames, and manifests only in
  separate artifact paths;
- proves each accepted input hash equals the stored source-frame hash.

### D. Strongly type the contract

Replace broad `serde_json::Value` fields with explicit Rust structs/enums for:

- landmarks;
- contacts;
- events;
- timing;
- facing;
- posture;
- approval state;
- provenance.

The schema, Rust types, generated pack, fixtures, and Godot importer must agree
exactly.

The generated-pack Rust test must fail when CI expects a pack but its path is
missing. Generate the test pack before running that test and export the exact
path.

### E. Correct runtime truth

- Resolve and validate the exact track before acknowledging acceptance.
- Emit `started` only after the first requested frame is loaded and visibly
  presented.
- Emit ordered frame, event, contact, interruption, completion, failure, and
  degradation results from observed playback.
- Missing, ineligible, hash-mismatched, or corrupt tracks must never emit
  `started`.
- Use explicit 24 FPS with integer relative-duration weights.
- Exercise the actual director-to-avatar path. Use a controlled Phase 01 bridge
  fixture wherever transport is claimed.

### F. Use only non-product test fixtures

Use:

- the exact approved identity as a clearly labeled one-frame import smoke
  fixture; and
- an obviously synthetic geometric fixture for timing, contact, corruption,
  and event-order tests.

Neither fixture may be presented as candidate character animation.

### G. Make CI non-vacuous

CI must:

- run byte-preserving intake;
- validate actual generated output against the actual schema;
- round-trip generated tracks through Rust after generation;
- import and play exact requested tracks in Godot;
- assert exact event order and timing;
- prove missing/corrupt track failure and restoration;
- run tamper cases for source hash, dimensions, contact, duration, event order,
  and approval status;
- fail on unexpected Godot errors;
- keep Phase 01 green;
- publish the intake template and exact hashes.

## Do not change

- Exact approved reference bytes or hashes.
- MON_FRAME_V1 canvas, root, baseline, safety, and timing policy.
- Architecture v1.0 authority boundaries.
- Exact Godot 4.7.2.
- Accepted Phase 01 foundation.
- Existing branch, PR #9, Issue #8, and protected-work rule.

## Prohibited work and claims

- Do not create, redraw, procedurally generate, warp, or auto-in-between
  production character art.
- Do not adopt Blender, another authoring dependency, or a 3D pipeline.
- Do not request operator visual approval.
- Do not expand the library, create final atlases, run the 10,000-case campaign,
  or perform Openbox endurance.
- Do not claim production embodiment, motion-language approval, visual aliveness,
  organism behavior, or Phase 03+ capability.

## Required validation

- Byte-preserving source intake.
- Fully typed schema/Rust/Godot crosswalk.
- Non-skipping generated-pack Rust test.
- Exact requested-track playback.
- Exact event/timing observation.
- Missing/corrupt pack degradation and recovery.
- Tamper-negative matrix.
- Clean-clone and hosted CI.

## Acceptance criteria

R04 passes only when:

1. no production character pixels are generated by Codex or procedural code;
2. R03 visual/rig outputs are superseded and retained as negative evidence;
3. one complete Architect-frame request and immutable intake contract exists;
4. source-frame bytes remain unchanged through intake;
5. schema, Rust, pack, fixtures, and Godot agree exactly;
6. the generated-pack Rust test demonstrably consumes the generated pack;
7. runtime emits `started` only after first-frame presentation;
8. all missing/corrupt/tamper cases fail closed;
9. Phase 01 and focused Phase 02 CI are green; and
10. the handoff status is `READY_FOR_ARCHITECT_FRAME_PACK`, not operator
    approval.

## Stop and return to Architect if

- any runtime requirement requires modifying source pixels;
- the contract cannot represent externally authored full-frame key poses without
  procedural reconstruction;
- a new dependency is required;
- exact source-byte preservation cannot be proven; or
- the protected-work boundary cannot be maintained.

## Required project updates

Update the active task packet, `.agent/CURRENT.md`, `.agent/INDEX.md`, append-only
outcome/learning records, Phase 02 directive/report, PR #9, and Issue #8.
Preserve all negative evidence. Leave PR #9 draft/open/unmerged and Issue #8
open.

## Required handoff

Return one `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R04` containing:

- exact superseded paths;
- intake schema and directory contract;
- Architect frame request;
- byte-preservation evidence;
- typed contract crosswalk;
- non-vacuous Rust generated-pack evidence;
- Godot event log and degradation/recovery tests;
- CI runs and artifact hashes;
- final `READY_FOR_ARCHITECT_FRAME_PACK` status.

## Capability boundary

A passing R04 establishes only a trustworthy intake/runtime boundary for future
Architect-authored art. It does not accept Phase 02 or establish visual
aliveness.
