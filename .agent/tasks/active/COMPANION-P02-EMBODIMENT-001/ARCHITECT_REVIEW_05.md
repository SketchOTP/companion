# Architect Review 05 — R04 Partial; Authored-Pack Contract Correction

## Verdict

`CONTINUE — R04 PARTIAL; NOT READY FOR ARCHITECT FRAME PACK`

- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed head: `ee2e47595271777bfbb253a6639c6ebac7198a1b`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Canonical Notion review:
  https://app.notion.com/p/3d8833cb27ff81588285f477678ad3d3

The bounded synthetic intake/runtime evidence is useful and retained. The
submitted `READY_FOR_ARCHITECT_FRAME_PACK` state is not accepted because the
source contract cannot truthfully represent the requested orientation tracks or
occluded landmarks. The Architect must not author production frames against a
contract that forces false metadata and an immediate breaking revision.

## Retained evidence

Do not repeat unless an input changes:

- Exact approved identity and turnaround hashes remain correct.
- The synthetic intake copies source PNG bytes into content-addressed and
  runtime locations and checks exact byte/hash equality.
- Approval eligibility is read from manifest state rather than filenames.
- The generated synthetic pack is consumed by the Rust validator; missing
  required pack input returns nonzero.
- The Godot synthetic test observes scene-tree frame-zero state before the
  director emits `started`.
- Missing track, ineligible approval, corrupt frame, and restored-pack cases
  were exercised.
- Phase 01 workflow `34657387545` and Phase 02 workflow `34657387598` passed.
- Artifact `10285933356` has digest
  `sha256:071348be8021b5dddb45f4fda068e27effbd9cb3d145a6a505ab2b98b8458516`.

These facts establish bounded synthetic engineering evidence. They do not
establish production-pack readiness, character art, motion quality, target
presentation, or Phase 02 acceptance.

## Material findings

### 1. Orientation tracks cannot be represented truthfully

`ARCHITECT_FRAME_REQUEST_V1.md` requests both `front -> front_left` and the
reverse. `MON_AUTHORED_FRAME_PACK_V1` assigns one facing to a whole track, and
the intake filename rule requires every frame to carry that same facing. Frames
have no facing field and tracks have no `entry_facing` or `exit_facing`.

A conforming authored orientation track therefore cannot describe its changing
facing. This alone blocks `READY_FOR_ARCHITECT_FRAME_PACK`.

### 2. Occluded and inapplicable landmarks cannot be represented

Every frame requires concrete integer coordinates for both eyes, hands, and
feet. A profile or strongly turned pose may hide an eye or hand. Canonical R10
allows landmarks to be hidden or undefined when that state is explicit. The
current schema forces invented coordinates.

### 3. Canonical landmark coverage is incomplete

The source contract lacks canonical R10 fields including mouth center,
attachment back/front, interaction focus, explicit ground contacts, and typed
optional action/object anchors. Accepting this V1 would require a breaking
revision as soon as real artwork arrives.

### 4. Architect input and derived runtime authority are conflated

The source schema requires `source_runtime_relationships`, although only intake
can know content addresses and runtime derivative paths. Intake then replaces
that field. Source authority and derived runtime facts must be separate
immutable documents.

Architect Review 05 adopts three distinct records:

1. `MON_AUTHORED_FRAME_SOURCE_PACK_V1` — immutable Architect input;
2. `MON_INGESTED_FRAME_PACK_V1` — validated runtime/build document; and
3. `MON_FRAME_INTAKE_RECEIPT_V1` — byte equality, digests, validation, and
   publication result.

### 5. Request completeness and reuse rules are not enforced

The generic schema accepts a one-track pack. It does not enforce the bounded
request's three neutral masters, idle, walk, both orientation directions,
reaction, counts, or required events.

The intake also does not reject duplicate track IDs, frame IDs, filenames,
sidecar filenames, or accidental duplicate hashes. The request says held
drawings use `duration_ticks`, but that rule is not implemented. Runtime
relationship lookup by the first matching hash is ambiguous when reuse occurs.

### 6. PNG source-profile validation is incomplete

Pillow mode `RGBA` does not independently prove PNG IHDR bit depth 8 and color
type 6. PNG color type 6 permits 8-bit and 16-bit samples. Accepting any ICC
profile does not prove sRGB. The documented `opaque_background` rejection is
not implemented, and blank or fully opaque content inside the safety region can
pass.

The intake must require the actual PNG signature, IHDR dimensions, bit depth 8,
color type 6, an explicit sRGB chunk or validated sRGB ICC profile, nonempty
alpha content, transparent background policy, and no pixels outside the safety
region.

### 7. Intake publication is not atomic

The intake writes directly into the final output directory and does not require
a new or empty destination. A failed retry can leave stale or mixed output from
a previous successful run. Production intake requires staging, complete
validation, receipt generation, and atomic publication.

### 8. Runtime pack trust remains incomplete

Godot checks frame hashes but does not independently verify approved reference
hashes, pack digest, track checksum, relationship uniqueness, path containment,
or complete manifest semantics before starting a track. A post-intake manifest
mutation can alter track mapping or event behavior without necessarily failing
the current runtime gate.

### 9. `first_frame_presented` overstates the observation

The avatar assigns frame zero, sets the target visible, waits one process frame,
and checks node state. This establishes scene-tree visual state, not a completed
viewport draw or physical target presentation. Godot exposes
`RenderingServer.frame_post_draw` after viewports update.

Use `first_frame_render_committed` only after the render boundary is observed.
Physical-display presentation remains a later Openbox target-host claim.

### 10. Timing and event evidence is not exact yet

The test checks 24 FPS, relative duration weights, an event prefix, and event
presence. It does not prove measured tick progression, event tick-to-frame
consistency, complete sequence equality, or absence of unexpected events. An
event tick can disagree with its declared frame index under the present source
validator.

## External discovery

Current primary sources rechecked:

- W3C PNG Third Edition: https://www.w3.org/TR/png-3/
- Godot 4.7 RenderingServer:
  https://docs.godotengine.org/en/4.7/classes/class_renderingserver.html
- Godot 4.7 SpriteFrames:
  https://docs.godotengine.org/en/4.7/classes/class_spriteframes.html
- Godot 4.7 AnimatedSprite2D:
  https://docs.godotengine.org/en/4.7/classes/class_animatedsprite2d.html

The Notion evidence register now records the PNG profile and render-observation
findings. The Architecture Decision Ledger records the source/ingested contract
split.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R04-C01

## Objective

Correct the authored-frame source, intake, and runtime contracts so the exact
bounded Architect frame request can be represented truthfully and accepted
fail-closed. Return `READY_FOR_ARCHITECT_FRAME_PACK` only after this correction.
Do not create production character art.

## Why this is next

Authoring against the present contract would force false facing and landmark
data and require an immediate breaking migration. Correcting the contract before
art production is the minimum decisive action.

## Authoritative basis

- Canonical project and end goal.
- R04 and R10.
- Architecture v1.0.
- Exact approved references.
- Architect Reviews 01–05.
- Adopted visual-authorship boundary.
- Adopted source/ingested-pack separation ruling.
- Accepted Phase 01 boundary.
- Current PR #9, Issue #8, and active task packet.

## Scope

### A. Split supplied and derived authority

Define:

1. `MON_AUTHORED_FRAME_SOURCE_PACK_V1` — immutable Architect input with no
   content-addressed or runtime-derived fields;
2. `MON_INGESTED_FRAME_PACK_V1` — validated document consumed by build/runtime;
3. `MON_FRAME_INTAKE_RECEIPT_V1` — input/output tree digests, byte-equality rows,
   validation profile, rejection result, and publication state.

Stage intake in a new temporary directory and atomically publish only after all
validation succeeds. The destination must be absent or explicitly empty.

### B. Correct track and frame semantics

- Add typed `entry_facing` and `exit_facing` to tracks.
- Add typed `facing`, `posture`, and optional `action_phase` to every frame.
- Keep selection facing separate from temporal frame facing.
- Add a request profile such as `phase02_bounded_motion_proof_v1`.
- Enforce exact required families, endpoint facings, frame-count ranges, and
  required events for that profile.

### C. Correct landmark semantics

Represent each landmark as:

- `state`: `visible`, `occluded`, or `not_applicable`;
- `point`: required only for `visible`, null otherwise.

Include root, left/right ground contacts, head center, eye midpoint or explicit
eyes, mouth center, hands, feet, attachment back/front, interaction focus, and
typed optional named anchors.

### D. Make identity and reuse unambiguous

- Require unique pack, track, frame, filename, and sidecar identifiers.
- Prefer a top-level immutable source-asset catalog keyed by SHA-256, with track
  frame occurrences referencing source assets.
- Reject accidental duplicate source hashes within a track.
- Allow intentional reuse only through an explicit source-asset reference;
  holds use increased `duration_ticks`, not duplicate files.

### E. Strengthen PNG validation

Require and negatively test:

- valid PNG signature;
- IHDR 1024x1024;
- bit depth 8;
- color type 6 RGBA;
- explicit sRGB chunk or validated sRGB ICC profile;
- nonempty alpha/content;
- transparent background/perimeter policy;
- safety-region compliance.

Implement `opaque_background` and blank-image rejection.

### F. Bind runtime trust

Before eligibility or start acknowledgment, Godot must validate:

- ingested profile/version;
- approved-reference hashes;
- pack digest;
- track checksum;
- relationship uniqueness;
- contained safe relative paths;
- timing profile;
- approval state;
- selected track and source-frame integrity.

Await `RenderingServer.frame_post_draw` before claiming
`first_frame_render_committed`. Physical display presentation remains outside
this gate.

### G. Bind event and timing semantics

- Prove each event tick belongs to its declared frame's half-open tick interval.
- Reject tick/frame mismatch, duplicate event identity, invalid contact spans,
  and invalid interruption spans with specific codes.
- Assert the full expected Godot event sequence and absence of unexpected
  events for the bounded fixture.
- Record monotonic observations and verify configured tick progression within a
  stated headless tolerance, clearly separated from target-display timing.

### H. Make CI decisive

Add negative cases for:

- orientation endpoint/facing mismatch;
- invalid landmark state/point combinations;
- duplicate IDs, filenames, or source-hash ambiguity;
- incomplete request profile;
- event tick/frame mismatch;
- 16-bit RGBA PNG;
- non-sRGB profile;
- blank and opaque images;
- stale/nonempty destination;
- path traversal and relationship duplication;
- pack, track, reference, and relationship tampering after intake.

Generate the synthetic source pack, intake it, validate the actual ingested pack
through Rust, then run the exact Godot path.

## Do not change

- Exact approved reference bytes and hashes.
- Visual-authorship authority.
- `MON_FRAME_V1` canvas, root, baseline, safety, and 24 Hz policy.
- Architecture v1.0.
- Godot 4.7.2.
- Accepted Phase 01 foundation.
- Existing branch, PR #9, Issue #8, and protected-work rule.

## Prohibited work and claims

- Do not create production character pixels.
- Do not adopt an art or 3D dependency.
- Do not request operator visual approval.
- Do not expand the sprite library.
- Do not run Openbox endurance or Phase 03 work.
- Do not retain the incompatible combined V1 contract as a silent fallback.
- Do not claim production-pack readiness before this correction passes.

## Required validation

- Source/ingested/receipt schema validation.
- Atomic byte-preserving intake.
- Request-profile completeness.
- Orientation and occlusion fixtures.
- PNG structure/profile checks.
- Duplicate/reuse checks.
- Actual ingested-pack Rust round trip.
- Runtime pack/track/reference integrity.
- Full event/tick sequence.
- New tamper-negative matrix.
- Clean clone and hosted CI.
- Phase 01 regression.
- `git diff --check` and private-data scan.

## Acceptance criteria

1. Orientation tracks use truthful per-frame facings and endpoint facings.
2. Occluded/inapplicable landmarks require no invented points.
3. Source pack, ingested pack, and intake receipt are separate.
4. Intake is atomic and byte-preserving.
5. The bounded request profile rejects incomplete packs.
6. PNG bit depth, color type, sRGB, alpha, background, and safety are proven.
7. Duplicate/reuse semantics are unambiguous.
8. Rust consumes the actual ingested pack and missing input fails.
9. Godot validates pack/track/reference integrity before start.
10. Start follows the corrected render-commit observation.
11. Full event/tick assertions and all new negative cases pass.
12. Phase 01 and focused Phase 02 CI remain green.
13. Final status is exactly `READY_FOR_ARCHITECT_FRAME_PACK`.

## Stop and return to Architect if

- the split contract cannot preserve source bytes;
- orientation or occlusion cannot be represented without weakening typing;
- atomic publication requires a new dependency;
- physical display presentation is required to pass this engineering gate; or
- the protected-work boundary cannot be maintained.

## Required project updates

Update the active task packet, `.agent/CURRENT.md`, `.agent/INDEX.md`, append-only
records, Phase 02 directive/report, PR #9, and Issue #8. Preserve R04 evidence
and negative results. Leave PR #9 draft/open/unmerged and Issue #8 open.

## Required handoff

Return `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R04-C01` containing the
three contracts, exact crosswalk, atomic-intake evidence, request-profile result,
PNG-profile evidence, runtime integrity/event logs, complete negative matrix,
CI IDs, artifact hashes, and final status.

## Capability boundary

A passing C01 establishes only that the Architect can supply a truthful,
immutable, bounded frame pack for review. It does not accept any character art,
Phase 02, visual aliveness, or product capability.
