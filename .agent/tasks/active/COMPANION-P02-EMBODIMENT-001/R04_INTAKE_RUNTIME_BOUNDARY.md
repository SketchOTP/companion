# R04 Immutable Authored-Frame Intake and Runtime Boundary

## Status

`READY_FOR_ARCHITECT_FRAME_PACK` is the implementation target. This document
does not accept Phase 02 or any artwork.

## Source preservation

`intake_authored_frame_pack.py` reads a supplied pack without altering it. It
validates each PNG and sidecar, copies the exact PNG bytes into
`sources/sha256/<prefix>/<sha256>.png`, reads the stored bytes back, and checks
both byte equality and SHA-256. Runtime copies live under `runtime/frames/` and
must retain the same bytes and digest. Atlases, imports, and review media are
separate derivatives and may never replace the content-addressed source.

Godot image import creates derived data in its import cache; it need not and
must not modify a source PNG. R04's external-pack loader is stricter: it loads
the validated runtime copy into an `Image`, then creates an `ImageTexture` in
memory. No `.import` metadata is written beside or into the source pack.

## Presentation acknowledgment point

`MonAvatar.present_track()` resolves an exact family/facing/posture/variant,
checks operation-specific approval eligibility, verifies every frame hash,
loads frame zero, assigns it to the inactive `AnimatedSprite2D`, makes that
sprite visible, waits one process frame, then verifies the same visible sprite,
track, frame index, and non-null texture. That observation emits
`first_frame_presented`. `MonAnimationDirector` may emit `started` only after
receiving that successful result; playback begins after `started`.

The observed sequence is:

```text
intent_received
track_resolved
track_validated
first_frame_loaded
first_frame_presented
started
frame_changed
track_event
completed
visible_state
```

## Approval authority

Eligibility is derived from the validated `approval_state` field, never a
filename:

- production: only `operator_approved`;
- review: `candidate` or `operator_approved`;
- test: only `synthetic_test_only`.

`rejected` is ineligible for every operation. An ineligible track cannot emit
`started`.

## Revision, export, and restore

`pack_id` is stable across revisions; `pack_revision` identifies one immutable
manifest release. Each source is addressed by its byte digest, so unchanged
frames may be shared by later revisions without mutable aliasing. The local
export command archives the complete intake tree with deterministic ZIP
metadata. Restore occurs into a fresh directory and requires equality of every
relative path and content digest. Generated archives and restored trees remain
outside Git.

## Evidence ceiling

The committed evidence uses obvious geometric `synthetic_test_only` frames and
the exact approved identity as a one-frame import smoke fixture. It proves a
bounded intake/runtime boundary at `E3_TARGET_TESTED`. It does not prove an
accepted body, animation, motion language, identity fidelity, visual aliveness,
target-host endurance, or Phase 02 completion.
