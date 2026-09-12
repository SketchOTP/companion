# Architect Review 06 — C01 Partial; Executable Bounded-Pack Proof Required

## Verdict

`CONTINUE — R04-C01 PARTIAL; NOT READY FOR ARCHITECT FRAME PACK`

- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed head: `925073601b039bc66e83de272b5378997cd8ec70`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACCEPTED`
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Canonical Notion review:
  https://app.notion.com/p/3d9833cb27ff81089f25cd955f5efb23

R04-C01 established useful contract and intake machinery, but the submitted
`READY_FOR_ARCHITECT_FRAME_PACK` state is not accepted. The executable bounded
request still contradicts the published Architect frame request, the positive
bounded profile is never exercised, and several evidence claims remain broader
than the behavior actually observed.

## Retained evidence

Do not repeat unless inputs change:

- exact approved identity and turnaround hashes;
- source/ingested/receipt contract split;
- per-frame facing and visible/occluded/not-applicable landmark representation;
- bounded synthetic byte-preserving intake and content-addressed copies;
- approval-state enforcement;
- required-path Rust validation;
- explicit 24 Hz timing direction;
- synthetic missing/corrupt/restored-track behavior;
- Phase 01 workflow `34663729219` and Phase 02 workflow `34663729216`, both
  successful at the reviewed head.

These establish bounded synthetic engineering evidence only.

## Material findings

### 1. The executable bounded profile contradicts the published request

`ARCHITECT_FRAME_REQUEST_V1.md` requests three tracks in family
`neutral_construction`: `front`, `right` profile, and `front_left`.

`validate_request_profile()` instead expects families `neutral_front`,
`neutral_profile`, and `neutral_front_left`, and it expects the profile facing
as `left`. It also indexes tracks by `family`, so three correct
`neutral_construction` tracks collapse to one record.

A source pack that follows the human Architect request therefore cannot pass the
current executable validator. This alone blocks frame-pack readiness.

### 2. There is no positive bounded-profile pack

The positive synthetic pack uses `synthetic_r04_test_v1`. The real
`phase02_bounded_motion_proof_v1` path is only tested negatively by switching an
incomplete synthetic pack to that profile and checking that missing families are
rejected, plus one direct endpoint-negative helper.

CI therefore proves that an incomplete bounded pack fails. It does not prove
that any complete bounded pack can pass.

### 3. Required events and endpoints are under-enforced

The published request requires:

- walk: `footfall_left`, `footfall_right`;
- both orientation tracks: `facing_changed` on the final drawing;
- listen/acknowledge: `attention_acquired`, `acknowledge`, `settled`.

The validator only requires any event for orientation and listen tracks. It does
not require walk footfalls, exact event names/order, first-frame entry facing,
last-frame exit facing, or final-drawing placement of `facing_changed`.

### 4. Reuse semantics are incomplete

A repeated source hash inside a track is accepted when `reuse_of` names any
previously seen frame ID. The validator does not prove that the target is in the
same track or uses the same source asset/hash. Reuse must bind to the actual
reused source occurrence.

### 5. PNG color-profile validation overclaims

The Architect request explicitly requires an `sRGB` PNG chunk. The intake also
accepts any `iCCP` chunk whose raw payload happens to contain the byte substring
`srgb`. That is not ICC-profile validation.

For V1, require exactly one valid `sRGB` chunk and reject iCCP-only or
conflicting color declarations unless a real ICC validator is later adopted.
Direct IHDR bit-depth validation remains required because PNG color type 6
permits both 8-bit and 16-bit samples.

### 6. Atomic visibility is useful; crash durability is not yet proven

The staging directory is created under the destination parent and published by
`os.replace`, which gives an atomic same-filesystem namespace switch. The
implementation does not fsync the staged authority files/directories or parent
directory and does not inject a mid-intake failure.

For the production intake boundary, complete Linux durability using standard
library `fsync` around the staged files/directories and parent rename. No new
dependency is needed.

### 7. Headless render observation can be mislabeled

`_await_render_commit()` awaits `RenderingServer.frame_post_draw`, but if that
signal is not observed under headless mode the function returns success after a
process frame and still emits `first_frame_render_committed`.

A scene-tree fallback is not a render-commit observation. Record the observation
source and emit `first_frame_render_committed` only when the render signal is
actually observed. Otherwise use a narrower scene-state event which does not
satisfy the render-commit gate.

### 8. Runtime event/timing evidence is incomplete

The Godot test verifies a required prefix and then checks that event names occur
somewhere. It does not require the entire sequence with no extra events, record
monotonic timestamps, or verify observed progression against the configured
24 Hz tick schedule.

## Architect disposition

Do not create production frames yet. Preserve the accepted C01 work and execute
one final contract-proof correction. No new art-authoring work is authorized.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R04-C02

## Objective

Prove that the exact bounded Architect frame request is internally consistent
and executable end to end. Return `READY_FOR_ARCHITECT_FRAME_PACK` only after a
complete synthetic `phase02_bounded_motion_proof_v1` source pack passes source
schema, profile semantics, durable intake, Rust, and Godot.

## Why this is next

The source/ingested/receipt split is now useful, but the requested real pack
cannot currently pass its own executable contract. Fixing that mismatch is the
last justified engineering gate before identity-critical art is authored.

## Authoritative basis

Read and reconcile:

- canonical project and end goal;
- Architecture v1.0;
- R04 and R10;
- exact approved references;
- Architect Reviews 01–06;
- adopted visual-authorship boundary;
- adopted source/ingested-pack separation ruling;
- accepted Phase 01 boundary;
- current PR #9, Issue #8, and active task packet.

## Scope

### A. Make human and executable request identical

Use the published request exactly:

- `neutral_construction`, front, exactly 1;
- `neutral_construction`, right, exactly 1;
- `neutral_construction`, front_left, exactly 1;
- `idle_breathe`, front_left, 6–8;
- `walk`, front_left, exactly 8;
- `orient_front_to_front_left`, front → front_left, at least 4;
- `orient_front_left_to_front`, front_left → front, at least 4;
- `listen_acknowledge`, front_left, exactly 6.

Do not key profile completeness by family alone. Match each required track by an
explicit role tuple or typed request-role identifier that can distinguish the
three neutral-construction facings.

Rewrite `ARCHITECT_FRAME_REQUEST_V1.md` to contain one canonical, nonconflicting
specification rather than appended contradictory sections.

### B. Add one positive bounded synthetic pack

Build an unmistakably synthetic geometric
`phase02_bounded_motion_proof_v1` fixture containing every required track and
count. It must include:

- truthful per-frame facing changes in both orientation tracks;
- one occluded landmark state and one not-applicable landmark state;
- walk contact spans and both footfall events;
- the complete listen/acknowledge event sequence;
- valid interruption ranges;
- unique IDs/assets/files.

This fixture is test geometry only and never candidate character art.

The complete positive pack must pass source schema, bounded-profile semantics,
intake, ingested schema, receipt schema, Rust round trip, and Godot load.

### C. Enforce exact bounded semantics

Require:

- exact required track multiplicity;
- no missing required track;
- no duplicate role satisfying one requirement twice;
- first frame facing == `entry_facing`;
- last frame facing == `exit_facing`;
- orientation `facing_changed` on the final frame;
- walk events `footfall_left` and `footfall_right` at valid tick/frame pairs;
- listen/acknowledge events in exact chronological order:
  `attention_acquired`, `acknowledge`, `settled`;
- required postures and completion modes;
- exact frame-count ranges;
- reject unexpected extra tracks unless explicitly allowed by the request
  profile.

### D. Correct source reuse

If an occurrence uses `reuse_of`:

- target must be an earlier frame in the same track;
- target and current occurrence must use the same source asset/hash;
- no duplicate file may be introduced under a new asset ID/name merely to pad a
  track;
- ordinary held drawings use increased `duration_ticks` instead of duplicate
  occurrences.

Add positive and negative reuse fixtures.

### E. Make PNG V1 exact

Require:

- valid PNG signature;
- exactly one IHDR as first chunk;
- 1024x1024;
- bit depth 8;
- color type 6;
- compression method 0;
- filter method 0;
- declared interlace policy;
- exactly one valid `sRGB` chunk;
- no iCCP-only substitute or conflicting color declaration;
- exactly one IEND with no trailing bytes;
- nonblank visible content;
- required transparent perimeter/background;
- no safety-region violation.

Do not claim ICC validation unless an actual ICC parser/validator is introduced
under separate authority.

### F. Complete atomic and durable publication

Keep stage and final output on the same filesystem. Before rename:

- fsync staged authority files;
- fsync required staged directories;
- fsync ingested pack and receipt;
- atomically rename stage to the absent destination;
- fsync the destination parent after rename.

Add an injected mid-intake failure test proving no final output is published and
a stale prior output cannot mask failure.

### G. Make render observation truthful

Record an explicit render-observation source.

- `first_frame_render_committed` may be emitted only after actual
  `RenderingServer.frame_post_draw` observation for the qualification render
  path.
- A headless scene-state fallback must use a different event name and does not
  satisfy the render-commit gate.
- Attach the avatar to the viewport/render path being observed.

Physical display presentation remains a later Openbox claim.

### H. Make event/timing evidence exact

Every observed runtime event must carry a monotonic timestamp.

For the bounded synthetic runtime track:

- assert the complete expected event sequence with no extras;
- validate every event tick against its frame's half-open tick interval;
- measure observed progression against configured 24 Hz timing using a declared
  headless tolerance;
- report configured timing separately from target-display timing.

### I. Expand negatives

Add explicit negatives for:

- right-vs-left neutral profile mismatch;
- repeated neutral-construction multiplicity error;
- first-frame entry-facing mismatch;
- final-frame exit-facing mismatch;
- missing/misplaced `facing_changed`;
- missing walk footfall events;
- wrong listen/acknowledge event order;
- invalid `reuse_of` target/hash;
- iCCP-only false sRGB;
- duplicate sRGB chunk;
- malformed chunk order/trailing bytes;
- injected mid-intake failure;
- render fallback mislabeled as render-commit;
- unexpected extra runtime event.

## Do not change

- approved reference bytes/hashes;
- visual-authorship boundary;
- `MON_FRAME_V1`;
- Architecture v1.0;
- Godot 4.7.2;
- accepted Phase 01 foundation;
- branch, PR #9, Issue #8, or protected-work rules.

## Prohibited work

- no production character pixels;
- no operator visual review request;
- no art/3D dependency;
- no full sprite-library generation;
- no final atlas scale-up;
- no Openbox endurance;
- no Phase 03 work.

## Acceptance criteria

C02 passes only when:

1. Machine request exactly matches the published Architect request.
2. One complete positive bounded synthetic pack passes the entire
   source→intake→Rust→Godot path.
3. Orientation, occlusion, event, count, and reuse semantics pass positive and
   negative tests.
4. PNG V1 validation is exact and does not treat arbitrary ICC text as sRGB.
5. Publication is atomic and crash-durable within the stated Linux fsync
   boundary.
6. Render-commit naming matches the actually observed boundary.
7. Full event order and timing evidence are recorded and validated.
8. Phase 01 and Phase 02 CI remain green.
9. Final status is exactly `READY_FOR_ARCHITECT_FRAME_PACK`.

## Stop and return to Architect if

- exact request semantics cannot be represented without a breaking redesign;
- durability requires a new dependency;
- true render-commit cannot be observed in the approved qualification path;
- current `origin/main` cannot be merged normally;
- protected operator work cannot be preserved.

Do not revert to procedural character generation.

## Required project updates

Update active task records, `.agent/CURRENT.md`, `.agent/INDEX.md`, append-only
ledgers, Phase 02 Notion directive/report, PR #9, and Issue #8. Preserve all C01
evidence and negative results. Leave PR #9 draft/open/unmerged and Issue #8
open.

## Required handoff

Return `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R04-C02` with:

- positive bounded-pack manifest summary;
- exact request-profile equations;
- orientation/occlusion examples;
- source/ingested/receipt hashes;
- durable atomic-publication observations;
- PNG structural/profile results;
- exact Godot render-source/event/timing log;
- expanded negative matrix;
- CI run IDs and artifact hashes;
- final readiness status.

## Capability boundary

A passing C02 establishes only that the Architect can supply the bounded
production-art review pack without lying to the contract. It does not accept any
art, Phase 02, visual aliveness, or product capability.
