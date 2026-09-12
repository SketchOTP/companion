# Architect Review 11 — R05 Rejected; Front-Presence and Profile-Locomotion Motion Model

## Verdict

`REPLAN / CONTINUE — R05-V1 REJECTED`

- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed task head: `e529d8db3d76af6239c7c4856c49553fb4097979`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Notion review: https://app.notion.com/p/3d9833cb27ff818c89ebe1aca70cf28b

R05-v1 is fully rejected as visual evidence. The operator-facing correction in
`R05_FACING_AND_MOTION_CORRECTION.md` is accepted as the new motion-design
basis.

## Decisive finding

The primary defect is the movement model, not merely insufficient frame count.
A front-left three-quarter showcase pose became the default idle, walk,
attention and reaction orientation. For the flat 2D habitat, ordinary presence
must face the viewer; lateral travel must use a true left or right profile;
quarter/back views are explicit turn and orientation states rather than a
universal animation pose.

Retain the engineering corrections from `c64b9743...`: source-tick review
timing, completion-aware looping, quarter-speed preview, and the operator-
authorized Photoroom cutout adapter. Retain all rejected art as negative
evidence.

Reject as candidate visual evidence:

- all R05-v1 art;
- universal `front_left` idle/walk/listen behavior;
- the eight-drawing twitch walk as adequate gait proof;
- head-only or scale-only orientation as body turning;
- quick nod/flick acknowledgement;
- green-screen cutouts with residual fringe;
- frame counts or unique hashes as proof of smooth motion.

## Adopted facing policy

| Behavior | Default facing | Required transition |
|---|---|---|
| Rest, breathing, listening, acknowledgement, social presence | `front` | Gaze/head may lead; torso turns only for a reason |
| Travel screen-left | `left` full profile | `front → front_left → left`; return through `front_left` |
| Travel screen-right | `right` full profile | `front → front_right → right`; return through `front_right` |
| Turn away | `back_left`, `back`, or `back_right` as required | Ordered whole-body progression; no one-frame flip |
| Unsupported facing/action | none | Report unavailable or route through authored connector; never silently fall back to `front_left` |

All eight construction facings are required for identity correspondence:
`front`, `front_right`, `right`, `back_right`, `back`, `back_left`, `left`,
`front_left`. Left/right production artwork must be reviewed independently;
blind horizontal mirroring is not accepted because the approved head silhouette
and lighting are asymmetric.

## Gait basis

The correct sequence is key-pose first, in-betweens second. A profile walk must
visibly exchange anatomical legs and preserve limb correspondence through
overlap.

Each profile walk contains, at minimum:

```text
anatomical-left contact
→ down
→ passing
→ up
→ anatomical-right contact
→ down
→ passing
→ up
→ loop
```

The swing foot clears the ground, support changes visibly, arms counter-swing,
and torso/head motion remains bounded. Start and stop clips connect to specific
gait phases; a stop may not snap a passing foot onto the floor.

Adobe's walk-cycle guidance identifies contact and passing positions plus
essential up/down body motion and calls for arms, torso, head, weight and foot
impact to participate. Toon Boom's walk analysis explicitly uses contact, down,
passing and up positions and describes an in-place walk whose scene/background
translation produces travel. These sources support the operator correction but
do not determine project-facing policy.

References:
- https://www.adobe.com/creativecloud/animation/discover/animation-walk-cycle.html
- https://learn.toonboom.com/modules/walk-cycle-animation2/topic/walk-analysis

## Contact-coordinate ruling

`MON_FRAME_V1` source root remains exactly `(512,896)` and encoded screen
translation remains prohibited in source PNGs.

The previous phrase `planted-contact drift <= 2 px` is interpreted by coordinate
frame:

- stationary clips: source and world contact coincide; planted source landmarks
  remain within 2 px;
- translating locomotion: a support foot is expected to move backward relative
  to the fixed source root while `MonRoot` translates through the habitat.
  Grounding is evaluated after composition in world space.

```text
world_contact(t) = actor_root_world(t)
                 + uniform_scale * (source_contact(t) - source_root)
```

During a declared planted span, the composed world-contact point must remain
within 2 px. A translating foot is not required to remain fixed in both source
space and world space. It is also prohibited to shorten contact spans to one
frame merely to make the test vacuous.

The locomotion review harness must therefore pair each source track with an
explicit 24 Hz actor-translation plan. Source art retains local landmarks and
contacts; clip/Godot metadata owns world translation.

## New request profile

Create a separately versioned request profile:

```text
phase02_presence_lateral_motion_proof_v2
```

Do not mutate or relabel historical `phase02_bounded_motion_proof_v1`.

### Construction

Eight neutral masters: one for every production facing.

### Front presence

- `idle_breathe_front`: 16–24 distinct drawings, 72–96 total ticks, loop; one
  complete inhale/exhale with planted feet and delayed small head/arm follow-
  through.
- `listen_acknowledge_front`: 16–24 distinct drawings, once; attention lead,
  readable listen hold, acknowledge, settle. A repeated nod does not qualify.

### Left travel

- `turn_front_to_left`: 8–12 drawings, once, visibly `front → front_left → left`.
- `walk_start_left`: 6–10 drawings, once, from a declared support state.
- `walk_loop_left`: 16–24 drawings, loop, built from correct two-leg
  contact/down/passing/up keys before in-betweens.
- `walk_stop_left`: 6–10 drawings, once, decelerating into planted profile rest.
- `turn_left_to_front`: 8–12 drawings, once; not merely outbound timing reversed.

### Right travel

Author the corresponding `right` sequence independently using `front_right`.
Do not satisfy it through blind mirroring.

## Authoring order

The generator may produce many studies, but promotion into the candidate pack is
strictly gated:

1. eight-facing construction;
2. left and right gait key poses;
3. start/stop/turn key poses;
4. only then constrained in-betweens based on selected surrounding keys;
5. cutout and normalization;
6. visual self-QA;
7. immutable intake and runtime validation;
8. Architect/operator review.

Unrelated independent text-to-image generations may not be treated as adjacent
in-betweens merely because their filenames or hashes differ.

## Cutout policy

Prefer transparent-background generation. Do not deliberately use green chroma
backgrounds for candidate production art.

If external cutout is required, the already operator-authorized Photoroom Remove
Background API may be used as offline authoring tooling with `format=png`,
`channels=rgba`, `size=full`, `crop=false`, preserving returned bytes and
provenance. Photoroom documents that cutout-subject output receives edge matting,
while alpha-mask-only output does not; alpha-mask reconstruction is therefore
not the preferred production cutout path.

Every promoted cutout is reviewed over white, black, mid-gray and saturated
magenta. Fringe, halo, clipped anatomy, or nontransparent perimeter rejects the
source before intake.

## Required review media

For every complete action publish:

- normal-speed playback honoring authored 24 Hz ticks;
- quarter-speed playback;
- ordered frame strip with anatomical left/right leg and gait-phase labels;
- silhouette-only playback;
- source-contact overlay;
- composed world-contact overlay using actor translation;
- black/white/gray/magenta edge-composite sheet.

One-shot clips must not be exported as infinite loops and review media must not
force uniform frame time.

## Approval units

Publish two continuous action demonstrations:

```text
front rest
→ attention/gaze left
→ anticipation
→ front_left turn
→ left profile
→ walk start
→ at least one complete two-step profile cycle
→ decelerate and plant
→ left profile rest
→ front_left return turn
→ front
→ settle/full breath
```

and the independently authored rightward equivalent through
`front_right`/`right`.

These complete actions are the review units. Per-clip technical PASS results do
not substitute for visual continuity across the full action.

## Acceptance boundary

Do not request visual approval until all of the following hold:

- all eight neutral facings preserve approved identity/anatomy;
- ordinary presence is genuinely front-facing;
- left/right travel is genuinely full profile;
- gait visibly alternates anatomical legs;
- hands remain stable with exactly two fingers plus thumb;
- feet remain stable with exactly three toes;
- turns change the whole silhouette through the correct quarter view;
- starts/stops connect to real gait phases;
- front breathing completes inhale and exhale;
- listen/acknowledge contains a readable hold and settle;
- no green/edge contamination remains;
- source/world contact QA is non-vacuous and passes;
- v2 request/schema/Rust/Godot/review/CI paths pass without weakening v1.

No Phase 02 acceptance follows automatically.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-002

## Objective

Implement the corrected facing/contact contract and produce two identity-faithful
complete lateral travel-and-return actions plus front-facing presence proof.

## Why this is next

The operator identified the true movement-model defect. Generating more
`front_left` frames would scale the wrong behavior. The next decisive evidence
is correct facing plus complete action continuity in both lateral directions.

## Authoritative basis

- canonical project/end goal;
- Architecture v1.0;
- R04 embodiment research;
- R10 sprite contract;
- exact approved identity/turnaround references;
- Architect Reviews 01–11;
- operator R05 rejection and facing correction;
- adopted Codex candidate-art authorization;
- adopted front-presence/profile-locomotion ruling;
- adopted composed world-contact ruling;
- current PR #9 / Issue #8 / active `.agent` packet.

## Scope

1. Merge current `origin/main` normally into the existing task branch.
2. Preserve all R05-v1 and rejected-study evidence.
3. Introduce `phase02_presence_lateral_motion_proof_v2` without weakening v1.
4. Reconcile source-space and world-space contact QA as defined above.
5. Create eight-facing neutral construction candidates.
6. Generate/select gait keys before any in-between pass.
7. Produce front breathe and front listen/acknowledge.
8. Produce complete left and right turn/start/walk/stop/return sequences.
9. Use transparent generation or the approved Photoroom cutout policy.
10. Normalize only promoted frames to `MON_FRAME_V1` after visual self-QA.
11. Pass actual source/ingested/receipt, Rust and Godot validation for v2.
12. Publish complete-action review media and return for operator/Architect review.

## Do not change

Architecture v1.0, exact approved references, Godot 4.7.2, accepted Phase 01,
protected operator work, Phase 03 closure, or rejected historical v1 evidence.

## Prohibited claims

Do not claim approved visual identity, approved motion language, complete
32-family/eight-direction animation library, visual aliveness, Openbox endurance,
or Phase 02 completion.

## Stop and return to Architect if

- the new profile cannot represent source/world contact honestly;
- a new dependency is required;
- image generation cannot maintain anatomical limb correspondence even at the
  key-pose gate;
- right-facing production art cannot be produced without unapproved mirroring;
- cutout contamination cannot be removed without damaging anatomy;
- any correction would require weakening accepted intake/runtime evidence.

## Required project updates

Update the active task packet, `.agent/CURRENT.md`, `.agent/INDEX.md`, append-only
history, Phase 02 Notion directive/report, PR #9 and Issue #8. Keep PR #9 draft,
open and unmerged; keep Issue #8 open.

## Required handoff

Return one `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R05-AUTHOR-002`
containing the v2 profile identity, eight-facing construction review, selected
gait keys, complete left/right action previews, front-presence previews, cutout
diagnostics, source/world contact calculations, pack/Rust/Godot/CI evidence,
all rejected studies, and one explicit operator visual decision request.
