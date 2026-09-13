# Architect Review 13 — R06 Block Accepted; Production Selection Must Derive From Final Approved Review Package

## Verdict

`INVESTIGATE / CONTINUE — R06 BLOCK ACCEPTED`

- Repository publication: `04225fb954b197acea86db5f871b4d9a4e3f82f9`
- Live task branch at review: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Architecture v1.0: adopted/unchanged
- Phase 01: accepted
- Phase 02: active/not accepted
- Phase 03+: closed
- Notion Review 13: https://app.notion.com/p/3da833cb27ff813e83b9f5535711b09c

Codex correctly stopped when the source set it treated as authoritative did not
satisfy the Review 12 opaque-black profile. No accepted artwork was mutated.

The stop exposed an Architect authority error: Review 12 conflated an earlier
operator selection record with the final operator-approved review playback.
Those are not the same authority surface.

## Live-state correction

Independent GitHub inspection reports:

```text
main at review publication: 04225fb954b197acea86db5f871b4d9a4e3f82f9
codex/p02-embodiment-001: 5f538a0c86783b7c5d00b140dcc91c7f76c30450
```

The R06 handoff's statement that the remote task branch was
`6bef092cb402270b75cbc6703d4e8d5e9d4cc665` is stale. The next Codex run must
`git fetch origin` and reconcile against the actual live task branch before any
implementation. Do not base integration work on a stale remote-tracking ref.

## Root cause

`R05_AUTHOR_002_OPERATOR_SELECTION.json` approves specific early construction
and static gait-key appearance. Its own `approval_scope` values are
`construction appearance` and `static gait key appearance`, and its
`not_approved_by_this_record` list explicitly includes complete gait continuity,
MON_FRAME_V1 source eligibility, root/world-contact QA, v2 runtime completion,
and Phase 02 acceptance.

The operator later accepted the complete delivered R05 review, including the
assembled left/right movement, front presence, connected Listen -> Acknowledge,
and black-background presentation. That final review package is the later and
broader visual authority.

Therefore the earlier static-selection file is visual provenance/reference
authority. It is not, by itself, the production runtime-selection manifest.

## Asset authority layers

Every visual asset must have one of these roles:

### `visual_reference_master`

Immutable visual/provenance authority. May be light-background RGB, transparent
RGBA, or another exact approved source encoding. Not runtime selectable unless
separately selected into the accepted runtime playback.

### `runtime_visual_master`

Exact source bytes actually referenced by the final operator-approved review
playback. These are the only assets eligible for the real-art runtime pack.

### `diagnostic_only`

Rejected, failed, or historical-study evidence. Never runtime selectable unless
explicitly re-approved later.

Runtime code must fail closed if an asset role is not `runtime_visual_master`.

## Presentation profiles

Do not force every approved source into one destructive encoding.

The R05 black habitat may support at least:

### `R05_BLACK_FIELD_RGB8_V1`

- native 1254x1254 RGB source bytes;
- immutable;
- black/near-black field measured from the accepted source;
- field must be visually indistinguishable from the black habitat under a
  quantitative render-boundary test;
- no cutout, recolor, resampling, repaint, or background replacement.

### `R05_TRANSPARENT_RGBA8_V1`

- native 1254x1254 RGBA source bytes;
- immutable;
- transparent perimeter/field;
- rendered over the same black habitat;
- no destructive conversion to RGB.

A light-background RGB asset remains `visual_reference_master` only unless the
exact final accepted playback demonstrably uses that byte sequence and the
runtime rendering proves no visible field. Do not key, cut out, or repaint it.

`MON_FRAME_V1` remains unchanged and continues to govern transparent normalized
assets where that profile is explicitly used. Review 13 does not weaken it.

## Frozen review authority

The accepted review identity remains:

```text
ZIP SHA-256
45fd9749179419339046af2ab40605c47d825ca4f0ad47c87a8c6fb9ca1b799b

manifest SHA-256
d8a0277272f0ccd6f948a24153b7f954aff138111ab840f22e09204aa359e595

review HTML SHA-256
7bd9e0cd5c64b89259dc2780825457a16144cebe02d259fd73a644591aa38cd2
```

The final package manifest and exact source bytes referenced by its accepted
non-diagnostic sequences define the runtime-production selection candidate.

## CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C01

### Objective

Reconcile the live branch and derive the production runtime selection from the
exact final operator-approved review package, then resume R06 integration using
per-asset immutable presentation profiles.

### Scope

1. `git fetch origin` and verify live `origin/main` and
   `origin/codex/p02-embodiment-001` before touching implementation.
2. Preserve the current clean secondary-worktree safety boundary.
3. Verify the frozen ZIP/manifest/HTML hashes again.
4. Parse the final accepted review manifest and enumerate every exact source
   asset referenced by accepted non-diagnostic sequences.
5. Create `R05_PRODUCTION_VISUAL_SELECTION_V1` with, per asset:
   - stable asset ID;
   - exact SHA-256;
   - exact filename/source path in the frozen package;
   - source role;
   - presentation profile;
   - accepted sequence memberships;
   - dimensions/mode;
   - perimeter/background observations;
   - facing/posture/action/gait phase where known;
   - approval provenance.
6. Compare this manifest against the earlier
   `R05_AUTHOR_002_OPERATOR_SELECTION.json`, preserving lineage but not requiring
   all earlier sources to be runtime eligible.
7. Reject all diagnostics and rejected studies from runtime selection.
8. Render every runtime-selected asset in Godot on the black habitat without
   source mutation. Capture a viewport/readback proof that no visible source
   rectangle/field is distinguishable beyond the declared black-field tolerance.
9. If an accepted runtime sequence references a light-background RGB image that
   cannot render field-free without source mutation, stop and return that exact
   asset/sequence as the blocker. Do not cut it out.
10. Once the runtime selection is clean, continue the existing R06 work:
    typed schema/Rust contracts, landmarks/contacts/events/timing, 24 Hz
    actor-root translation plans, world-contact slip <=2 px, real-art Godot
    playback/failure/recovery, export/restore, and hosted evidence.

### Runtime-placement rule

Native source dimensions are preserved. Per-frame source anchors and landmarks
may vary. Godot may use node transform/offset metadata to place the native image
relative to `MonRoot`; it may not resample or rewrite the master image.

### Required validation

- exact frozen package hashes;
- live-branch identity and ancestry;
- complete accepted-sequence asset inventory;
- role/profile uniqueness;
- runtime-ineligible reference/diagnostic rejection;
- RGB and RGBA byte preservation;
- black-field/perimeter measurement;
- actual black-habitat viewport readback;
- no visible source rectangle beyond declared tolerance;
- schema/Rust/Godot real-art consumption;
- actual accepted-sequence playback;
- source/world landmark and contact validation;
- missing/corrupt/hash-mismatch/ineligible failure and restoration;
- local export/restore;
- hosted Phase 01/Phase 02 regression;
- durable artifact publication.

### Acceptance boundary

C01 passes only when the accepted final-review playback can be represented by a
runtime manifest containing only exact accepted source bytes, every runtime
asset has one valid presentation profile, no source bytes are changed, and the
black habitat renders every selected asset without a visible rectangular field.

If that passes, finish the remaining R06 real-art integration scope in the same
bounded directive and return one complete result.

### Stop conditions

Stop and return to Architect if:

- live branch reconciliation cannot be completed normally;
- frozen package hashes differ;
- the final accepted package is missing;
- accepted runtime playback requires a light-background RGB asset that shows a
  visible field and cannot be used without pixel mutation;
- world-contact grounding cannot pass with metadata/MonRoot translation alone;
- a new dependency is required;
- any visual correction would require new art generation.

Do not reopen art generation automatically.

## Capability boundary

R05 visual acceptance remains valid. This review corrects source-role/runtime
selection authority only. Phase 02, transition qualification, Openbox
endurance, organism behavior, memory, perception, speech, learning, dreaming,
caregiving efficacy, reliability, and Phase 03+ remain unaccepted.
