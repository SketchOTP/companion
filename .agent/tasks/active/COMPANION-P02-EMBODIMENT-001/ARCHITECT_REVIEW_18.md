# Architect Review 18 — C05 Partial Accepted; Intent Lifecycle, Fixed-Step Timing, and Real Phase Coupling Required

## Verdict

`CONTINUE — R06-C05 PARTIAL ACCEPTED`

- Reviewed implementation head: `24b4919a48eeef49fbcbb9305b9f2ad66639b3bd`
- Reviewed publication head: `3f8846c761ecc46e7cf2f5e3d94a2bbd5c6416e1`
- Frozen visual head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Architecture v1.0: adopted/unchanged
- Phase 01: accepted
- Phase 02: active/not accepted
- Phase 03+: closed
- Notion review: https://app.notion.com/p/3db833cb27ff81748624fa3ed8132b8d

C05 correctly establishes the controller/presentation authority split and useful bounded movement evidence. Do not reopen sprite generation. Do not begin legal-transition qualification yet because the submitted C05 evidence does not satisfy several explicit Review 17 requirements.

## Accepted C05 boundary

Retain:

- frozen R05 source pack SHA `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40` and byte-identical source art;
- canonical `MonRoot` movement owned by `MonLocomotionController`, not raster contacts;
- true left profile mapping to `r06_playback_track_07/08/09`;
- true right profile mapping to `r06_playback_track_12/13/14`;
- arithmetic left/right cumulative translation for bounded slow/nominal/fast qualification cases;
- nominal Godot use of the actual approved pack and strict `RenderingServer.frame_post_draw` evidence;
- C02 render/compositor/intake/Rust/failure/recovery/export boundaries;
- exact-head hosted success on implementation SHA `24b4919a...` for R06, Phase 01, and inherited Phase 02.

The later `3f8846c...` commit is documentation/evidence reconciliation only.

## Material findings

### 1. Intent replay/freshness is claimed but not implemented

`mon_locomotion_controller.gd::accept_intent()` validates schema major, direction/facing, state, and velocity sign, then simply replaces `intent`. It stores no accepted sequence/freshness state, does not reject a repeated `intent_id`, and does not apply `cancellation_id` semantics.

The Python negative matrix does not exercise a protected stale-intent path. It inserts a static result for `stale_replayed_intent_id`. Therefore the C05 claim that stale intent replay is independently rejected is not accepted.

The contract also calls `intent_id` a UUID while the Godot semantic test submits values such as `c05-left-0`, which are not schema-valid UUIDs. Rust/schema conformance and Godot runtime consumption are therefore not the same end-to-end wire path yet.

### 2. Velocity/animation coupling is absent

Review 17 required gait playback rate/phase to be calibrated to commanded velocity.

C05 does not implement that coupling. The Python qualifier selects frames from authored local ticks identically at `48`, `96`, and `144 px/s`; velocity changes only `actor_root_x`. The Godot test likewise uses the same 24 FPS source timing and frame schedule regardless of commanded velocity.

This proves controller translation at three velocities, but not synchronized presentation at three velocities.

### 3. Quarter-speed evidence is not rendered playback

`quarter_speed_trace` is the normal semantic trace copied with a `playback_rate: 0.25` field. The hosted R06 workflow invokes the C05 Godot script only for nominal left `-96` and right `+96`. No quarter-speed translated Godot playback is executed or captured.

The quarter-speed review claim is therefore not accepted.

### 4. Mid-loop interruption is not a real cancellation/stop transition

The Python interruption case produces one zero-velocity tick, exits the current phase loop, then continues into later outer phases. It can resume cruise rather than terminate locomotion into the stop track.

That is not evidence for the required mid-loop stop/cancellation behavior.

### 5. The runtime 24 Hz clock is not demonstrated

`tick_once()` numerically divides velocity by `24`, but the Godot test calls it once per `process_frame`. The result does not establish that canonical movement is scheduled by an explicit 24 Hz fixed-step simulation independent of render cadence, or that render-rate variation cannot drop/duplicate movement ticks.

### 6. The negative matrix overstates executable coverage

Several negative cases are genuine mutations of a passing trace, but at least stale replay, missing track, and ineligible/corrupt pack are inserted as already-rejected result records rather than all being exercised through the C05 protected path. Earlier R06 evidence for missing/corrupt packs remains useful, but the C05 statement that all thirteen are independent implementation-path mutations is not accepted.

## CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06

### Objective

Preserve the accepted C05 controller-owned movement boundary and close only the runtime semantics that C05 did not actually prove: intent freshness/cancellation, fixed-step 24 Hz scheduling, real velocity/phase coupling, real interruption-to-stop behavior, actual normal/quarter translated review playback, and executable negatives.

### Why this is next

Controller ownership is correct and should not be reopened. Transition qualification would be premature while stale intents can be accepted, interruption is not a real stop path, animation cadence is independent of commanded velocity, and quarter-speed review is synthetic metadata rather than rendered evidence.

### Authoritative basis

- Architecture v1.0 remains unchanged.
- Review 17 controller-owned locomotion ruling remains adopted.
- This Review 18 accepts only the bounded C05 ownership/translation evidence listed above.
- Frozen R05 visual approval remains unchanged.

### Scope

1. Fetch and normally merge current `origin/main` into the existing Phase 02 branch. No rebase/force-push/history rewrite/new PR.
2. Preserve every accepted sprite byte and all C02-C05 positive/negative evidence.
3. Do not change the controller-owned `MonRoot` authority split.
4. Introduce a separately versioned locomotion-intent wire profile rather than silently changing V1 historical evidence.
5. Add explicit monotonic freshness semantics, recommended as `intent_sequence: u64` plus UUID `intent_id`. A UUID alone is not a monotonic ordering mechanism.
6. Controller must retain the latest accepted sequence/ID and reject duplicate, stale, and replayed intents fail-closed.
7. Define cancellation/stop semantics explicitly: a cancellation references the currently active movement intent and cannot cancel an unrelated or already-superseded intent.
8. Use schema-valid serialized intent data in the Godot qualification path. No ad-hoc invalid intent IDs.
9. Run canonical movement from an explicit fixed 24 Hz simulation clock independent of render cadence. Prove render-rate variation does not cause movement tick loss or duplication.
10. Couple loop animation phase rate to commanded speed under one declared calibration. Suggested bounded policy: nominal 96 px/s = `1.0x`; 48 px/s = `0.5x`; 144 px/s = `1.5x`, unless a measured alternative is justified. This is presentation calibration only and must not change commanded world displacement.
11. Start/stop tracks may retain authored timing unless a documented presentation calibration is necessary; do not rewrite art or frame timing files.
12. A mid-loop stop/cancel must stop canonical translation at the accepted command boundary and transition into the stop presentation without resuming a later cruise loop.
13. Preserve actor position continuously through stop/cancel and subsequent idle/rest handoff.
14. Produce actual rendered translated playback at normal review speed and quarter review speed for left/right nominal cases. Quarter-speed review must slow presentation of the same semantic movement path; it may not be a copied trace label.
15. Record command acceptance/rejection, fixed-step ticks, actor position, active intent ID/sequence, selected track/frame, animation phase, playback rate, and stop/cancel events.

### Required negatives

Exercise the actual protected implementation path, not static booleans, for:

- duplicate intent ID;
- equal sequence replay;
- lower/stale sequence;
- cancellation referencing the wrong active intent;
- cancellation replay after completion;
- wrong direction/facing;
- velocity-sign contradiction;
- missing/wrong-profile locomotion track;
- front-left fallback attempt;
- fixed-step tick drop;
- fixed-step tick duplication;
- render-FPS variation with semantic tick count unchanged;
- loop recenter/root reset;
- animation phase reset at loop boundary;
- corrupt/ineligible pack using the retained R06 failure path.

Every negative must identify the specific predicate that rejected it.

### Required validation

- Schema and Rust round-trip for the new versioned intent profile.
- Godot consumes schema-valid serialized intent fixtures with the same field semantics.
- Left/right nominal/slow/fast controller movement remains directionally correct.
- Animation loop rate actually changes with velocity and phase remains continuous through loop boundaries.
- Mid-loop stop/cancel terminates cruise and enters stop without later cruise resumption.
- Fixed-step movement remains 24 Hz under at least two deliberately different render cadences.
- Actual normal and quarter translated playback artifacts are published.
- Strict render/compositor/intake/failure/export regressions remain green.
- One implementation SHA passes R06 + Phase 01 + inherited Phase 02. Do not touch Phase 01 unless required by a real regression; if Phase 01 code is unchanged, one exact-head hosted pass is sufficient.

### Do not change

No image generation, sprite editing, cutout, recolor, resampling, new dependency, transition campaign, Openbox endurance, Phase 03 work, PR merge, or Issue closure.

### Stop and return to Architect if

Stop if truthful controller timing requires canonical movement state to live in render-only Godot state, if velocity/phase calibration cannot produce visually coherent translated playback without changing source pixels, if cancellation semantics conflict with accepted authority boundaries, or if a new dependency/architecture change is required.

### Acceptance boundary

C06 passes when the controller-owned locomotion primitive is a real versioned, replay-safe, fixed-step runtime path with velocity-synchronized presentation and truthful stop/cancel behavior, not merely an offline displacement trace. If C06 passes with no new material defect, the next action is the legal-transition campaign. Do not invent another locomotion metadata gate.

## Capability boundary

Phase 02 remains active and unaccepted. No organism autonomy, navigation, physical foot grounding, memory, perception, speech, learning, caregiving, reliability, or Phase 03 capability follows from C05 or C06.