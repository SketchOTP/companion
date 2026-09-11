# Architect Review 03 — R02 Proof Rejected; Production Rig and Articulated Motion Required

## Verdict

`CONTINUE — R02 PROOF NOT ACCEPTED`

- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed head: `4a111435381ff2d364cd705edbb1d65da46ea886`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Canonical Notion review:
  https://app.notion.com/p/3d8833cb27ff812f8102dbc79891053e

Exact reference ingestion, removal of the rejected bulk outputs from the final
tree, deterministic build plumbing, and focused CI infrastructure are retained.
The submitted production-body, authoring-comparison, temporal-motion,
root/contact, contract-alignment, Godot-playback, and operator-review-readiness
claims are rejected.

## Current blocker

The exact references are now available, but there is still no editable,
identity-faithful production body source. The submitted proof deforms a
rectangular upper band of the posed identity PNG while leaving the lower body
and feet unchanged. That cannot establish gait, orientation, planted contacts,
or a reusable motion language.

## Evidence retained

Do not repeat these unless an input changes:

- Both exact approved native PNGs are committed and hash-verified.
- The prior bulk frame/atlas/pack output is absent from the final branch tree.
- Focused Phase 02 and inherited Phase 01 workflows are green at the reviewed
  head.
- Current proof generation is byte-reproducible for its present algorithm.
- A separate track concept has begun to distinguish facing from temporal frame
  order.
- Exact Godot 4.7.2 and the Phase 01 foundation remain intact.

These establish source transfer and useful build infrastructure. They do not
establish a production body or acceptable motion.

## Independent findings

### `MON_BODY_SOURCE_V1` is not a production body source

The JSON file is descriptive metadata. The SVG contains a head/body silhouette,
eyes, pupils, mouth, and shadow, but no articulated arms, hands, fingers, thumb,
legs, feet, toes, facing masters, deformable part graph, production pivots, or
weight information. It cannot generate the approved creature consistently
across neutral front, profile, and front-left views.

The raster candidate is also metadata pointing to the original flattened posed
identity PNG. It is not an editable layered raster source.

### The authoring comparison did not compare two working paths

The raster side is marked `rendered_proof=true` because the approved PNG can be
opened. The vector side was not rasterized. The comparison script records a list
of dimensions as compared without measuring silhouette, face, palette, edge
language, hands, feet, root, or contacts.

The review board juxtaposes the approved creature with a crude egg-shaped
vector. It is not an operator-decision-quality comparison.

### The motion proof is whole-image warping

`build_motion_proof.py` starts from the raised-hand identity master, crops an
upper rectangular band, globally resizes it, and composites it over the
unchanged base image. Walk, idle, orient, listen, and acknowledge all use this
mechanism. Listen and acknowledge add simple arcs.

No limb is separately posed. No foot is lifted or translated. No arm
counter-swing, passing pose, down pose, up pose, weight transfer, or orientation
change is authored.

The Architect independently compared the committed workflow artifact. Rows
`y=820..1023` are byte-identical across every frame within every submitted
track, including all eight walk frames. The manifest nevertheless alternates
left/right planted-contact metadata. The walk/contact claim is contradicted by
the rendered pixels.

The orient tracks never change facing; they scale the same front-left source.
The listen/acknowledge tracks are overlay marks on the same pose rather than an
articulated reaction.

### Root and contact evidence remains self-asserting

Every frame receives hard-coded root and foot coordinates. The validator checks
those declared values rather than deriving positions from the authoring source
or rendered geometry.

The root/contact sheet manually draws a crosshair and circles on a resized
composition. It is not a source-coordinate-faithful reconstruction of
`MON_FRAME_V1` and does not prove planted-contact drift.

### The proof data does not conform to its schema or Rust type

The schema requires `clip_id`, `track_checksum`, stage `candidate|approved`, and
direction values `N|NE|E|SE|S|SW|W|NW`.

The generated proof uses stage `proof`, direction `front_left`, omits required
fields, and uses a different shape. The contract validator validates synthetic
schema samples rather than the actual `temporal_tracks.json`; its wire execution
set is empty.

### Timing remains inconsistent with the 24 Hz contract

The generator and Godot runtime use 12 FPS while integer `duration_ticks` are
passed as relative frame weights. A weight of one therefore lasts 1/12 second,
not the required 1/24 second. The approved timing profile requires explicit 24
FPS when relative weights represent 1/24-second ticks.

### The Godot proof can pass without proving the requested track

The director retains old family names and default direction `N`, while the proof
tracks use different family names and `front_left`. It can report `started`
before proving that the track loaded. The test then directly invokes another
track and only checks that marker/completion arrays are nonempty.

Hosted logs contain repeated Godot UDS connection errors while the job still
passes. The current test does not enforce the requested track, exact event
sequence, or zero unexpected runtime errors.

### Operator review is not ready

The artifact contains static strips but no normal-speed or quarter-speed motion
playback. Static sheets cannot establish rhythm, weight, loop quality, contact
timing, interruption, or transition quality.

## Architect technical decision

Use the already approved Godot 4.7.2 toolchain as the primary Phase 02 authoring
proof:

- explicit layered parts using `Polygon2D`, `Sprite2D`, or an equivalent editable
  Godot-native source;
- `Skeleton2D`/`Bone2D` only for bounded deformation that preserves identity;
- `AnimationPlayer` for authored timing and event tracks;
- discrete authored replacement drawings for hands, feet, face, head silhouette,
  and other changes that cutout deformation cannot preserve;
- deterministic raster bake to `MON_FRAME_V1`;
- raster sprite-frame runtime remains unchanged.

This replaces the unexecuted vector-versus-raster comparison and adds no new
production runtime dependency. A layered raster source may supplement explicit
replacement drawings, but a flattened reference PNG is not a layered-raster
authoring source.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R03

## Objective

Replace the false canon/motion proof with one editable Godot-native production
body proof and one genuinely articulated temporal motion package. Stop for
operator visual approval after this package. Do not expand the full library.

## Why this is next

The exact-source transfer and CI plumbing are solved. Every remaining Phase 02
result depends on an editable body source and a motion grammar that can survive
operator review. Additional metadata, counts, or global image warps cannot
retire that risk.

## Scope

### A. Preserve and reconcile

1. Merge this review from current `origin/main` normally into the existing task
   branch.
2. Retain exact approved references and their hashes.
3. Retain final-tree removal of prior bulk output and the focused workflow
   structure.
4. Mark `MON_BODY_SOURCE_V1`, the authoring comparison, the 26-drawing proof,
   root/contact result, Godot headless result, and operator-review-ready claim as
   superseded evidence.
5. Preserve public history; do not rebase or force-push.

### B. Build the actual editable production source

Create `MON_BODY_SOURCE_V2` with explicit components for:

- shadow;
- torso/pelvis;
- head and stable spike topology;
- left/right upper arm and forearm;
- left/right hand with exactly two fingers plus one thumb;
- left/right thigh/lower leg;
- left/right foot with exactly three toes;
- eye fields and pupils;
- mouth;
- optional face/hand/foot replacement-drawing slots.

Define stable pivots, z-order, rest transforms, root, baseline, foot contacts,
head/eye/mouth landmarks, silhouette bounds, and source-reference traceability.

Create neutral front, neutral profile, and neutral front-left masters from the
same production canon. Do not use the raised-hand hero pose as the neutral rest
pose.

### C. Build real articulated motion

Produce only these operator-review tracks:

1. Front-left idle/breathe: 6-8 temporal poses. Root fixed; torso, head, and arms
   show delayed organic motion; feet remain planted.
2. Front-left walk: eight gait phases covering contact, down, passing, and up for
   both sides. Feet and legs visibly articulate; arms counter-swing; declared
   planted contacts match rendered motion.
3. Front-neutral to front-left and reverse orientation connectors: at least four
   poses in each direction, with a real silhouette/facing change.
4. Listen to acknowledge: head/eyes lead, body settles, acknowledgment follows.
   Decorative arcs alone are not motion evidence.

Use rig/key-pose transforms as authored truth and bake full-canvas raster frames.
Global image-band scaling is prohibited as the sole motion mechanism.

### D. Align contracts and runtime

Version the proof contract so the schema, Rust type, generated JSON, fixtures,
and Godot loader agree exactly.

Separate:

- `family`;
- `facing` using
  `front|front_right|right|back_right|back|back_left|left|front_left`;
- optional `travel_direction`;
- `posture`;
- `variant`;
- temporal `frame_index`;
- integer `duration_ticks`.

Include track checksum, frame hashes, landmarks, contacts, events,
loop/completion behavior, entry/exit posture, and interruption ranges.

Set animation FPS to 24. Pass integer tick values as relative frame-duration
weights. A two-tick hold uses weight `2.0` and lasts 2/24 second.

The director must reject a missing or ineligible track before reporting
`started`. It must select the exact requested facing/family/variant and report
observed frame, event, contact, completion, interruption, and degradation
results.

### E. Derive evidence from actual source and playback

Required positive and negative evidence:

- derive root and foot positions from rig transforms and/or a dedicated landmark
  render pass;
- verify planted-contact drift <=2 px;
- verify swing feet actually move during walk;
- verify orient start/end silhouettes differ and match declared facings;
- verify the lower-foot region is not byte-identical through the whole walk;
- verify idle feet remain fixed while upper-body geometry changes;
- alter one contact/landmark and prove failure;
- remove one digit component and prove source-graph anatomy failure;
- alter one duration tick and prove timing/event failure;
- request a missing track and prove no `started` result is emitted;
- corrupt one proof frame and prove degradation and recovery.

No assertion may be copied from declared metadata without independent observed
support.

### F. Produce reviewable motion

Publish directly accessible artifacts containing:

- production-source hierarchy and pivot sheet;
- neutral front/profile/front-left construction sheet;
- anatomy/palette/silhouette sheet;
- normal-speed animation for every proof track;
- quarter-speed animation for every proof track;
- ordered frame strips;
- silhouette-only playback;
- root/contact-overlay playback;
- exact event logs;
- rejected R02 comparison for audit context.

Use GIF, APNG, or a deterministic frame-sequence player artifact. Static strips
alone do not satisfy motion review.

### G. Make CI semantically fail closed

The focused workflow must:

- validate the actual generated track file against the actual schema;
- deserialize and reserialize every actual track through Rust;
- load and play each requested track in Godot;
- run articulated walk/contact and orientation tests;
- execute all tamper-negative cases;
- run the motion validator rather than only count files;
- fail on unexpected Godot `ERROR:` output;
- use a controlled bridge fixture or disable unrelated bridge retries so the
  proof emits no uncontrolled connection errors;
- build motion-review artifacts and record hashes;
- keep inherited Phase 01 CI green.

## Acceptance criteria

R03 passes only when:

1. `MON_BODY_SOURCE_V2` is a genuine editable complete-anatomy part hierarchy.
2. Neutral front, profile, and front-left renders derive from the same canon and
   remain faithful to approved references.
3. Walk contains real leg/foot articulation and independently verified contacts.
4. Orientation connectors visibly change facing.
5. Listen/acknowledge is a body reaction rather than overlay marks.
6. Schema, Rust type, generated JSON, fixtures, and Godot runtime agree.
7. 24 Hz timing is correct.
8. Exact playback event order is observed without unexpected runtime errors.
9. Positive and tamper-negative QA pass.
10. Normal-speed and quarter-speed artifacts are operator-accessible.
11. Full-library, atlas-scale, transition-campaign, and Openbox-endurance work
    remains closed.
12. PR #9 remains draft/open/unmerged and Issue #8 remains open.

## Stop and return to Architect if

- the references expose a material ambiguity preventing one neutral model;
- Godot-native cutout plus discrete replacements cannot preserve identity;
- a new authoring dependency is required;
- deterministic capture requires host modification; or
- operator-accessible motion publication cannot be produced.

Return the one blocking ambiguity or dependency with concrete evidence. Do not
fall back to whole-image warping or another count-driven proxy.

## Required project updates

Update the active packet, `.agent/CURRENT.md`, `.agent/INDEX.md`, append-only
outcome/learning records, Phase 02 directive/report, PR #9, and Issue #8.
Preserve failed and superseded work. Leave the PR and issue open.

## Required handoff

Return one `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R03` containing exact
source hashes, body-part hierarchy, track/frame counts, contract crosswalk,
observed Godot event logs, rendered contact measurements, negative tests, CI
runs, artifact IDs/hashes, directly accessible motion assets, explicit visual
ambiguities, and one operator approval request.

## Capability boundary

A passing R03 package establishes only an operator-reviewable editable body
source and articulated motion proof. It does not accept Phase 02, establish
continuous aliveness, or authorize Phase 03.
