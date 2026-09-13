# Architect Review 15 — R06-C02 Partial Accepted; Continuous Stance and Real Travel Required

## Verdict

`CONTINUE — R06-C02 PARTIAL ACCEPTED`

- Reviewed implementation head: `94b59cf76fc046abe28d6dd1b67359a803af8544`
- Reviewed publication head: `70afeddeddbcb56fa0580b336c82e494f0f02f3b`
- Notion authority: https://app.notion.com/p/3da833cb27ff810384e9cddc94c4839b
- PR #9: draft/open/unmerged
- Issue #8: open
- Architecture v1.0: adopted/unchanged
- Phase 01: accepted
- Phase 02: active/not accepted
- Phase 03+: closed

R06-C02 materially corrected the render and compositor evidence boundary and produced useful measured sole candidates. Those results are retained. R06 is not yet accepted because the locomotion support model omits visible stance and the current zero-slip/zero-boundary-jump results do not independently establish meaningful travel.

## Retained C02 boundary

Keep unchanged:

- frozen R05 visual package and 58 immutable 1254x1254 RGB runtime masters;
- 24 runtime tracks / 283 frame slots;
- source-role separation and byte-preserving intake;
- schemas and Rust typed consumption;
- failure/recovery and export/restore plumbing;
- strict `RenderingServer.frame_post_draw` requirement for `first_frame_render_committed`;
- separate viewport readback event;
- transformed in-source black-field compositor sampling;
- exact-head hosted regression evidence on `94b59cf...`;
- lowest-contour sole candidates and their inspectable machine-assisted provenance as measured geometry.

No new character art is authorized.

## Decisive review finding

`ground_r06_c02.py` still derives the support timeline primarily from action labels. `make_contacts()` only keeps frames containing `contact` or `down`. Consequently, passing/up drawings can have a visible grounded foot while the evidence records no support at all.

The validator checks only spans that were declared. It does not reject a gait frame whose image still shows grounded support but whose support state is omitted. Therefore the reported `0.0 px` maximum slip proves only that the selected declared intervals were pinned.

`root_plan()` solves actor-root translation from each declared support point so the chosen world contact remains fixed. Zero slip is expected from that construction. `stitched_sequence()` then adds a constant offset to each next track so the boundary actor-root coordinates match exactly. Zero boundary jump therefore establishes coordinate registration, but not that the walk advances through the habitat.

Independent artifact inspection of the accepted left/right loops shows grounded support during frames currently outside the declared contact/down spans. The current stitched start→loop→stop root plans also yield only very small net displacement, so meaningful lateral travel is not yet established.

External gait terminology is used only as a sanity check: stance is conventionally the period in which a foot remains in ground contact, continuing beyond initial contact/loading and ending at toe-off. COMPANION need not copy human percentages or biomechanics, but it may not call a visibly grounded foot unsupported solely because a frame is labelled passing/up.

## CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C03

### Objective

Preserve all accepted C02 integration and correct only locomotion stance/support semantics and cumulative actor-root travel on the frozen accepted drawings.

### Why this is next

Render commitment, compositor qualification, source identity, intake, Rust, Godot loading, and basic runtime execution are no longer blockers. The remaining R06 blocker is whether the accepted profile gait can be represented as physically coherent screen travel rather than an in-place sequence with selectively pinned contacts.

### Authoritative basis

This Review 15 and the frozen R05 visual package. Review 14 remains historical authority for C02. Do not reopen accepted C01/C02 areas unless C03 evidence directly proves a defect.

### Known evidence

- C02 measured sole candidates from actual non-black contours and retained overlays/provenance.
- Current loop contact spans omit passing/up frames.
- Current `0.0 px` planted slip is computed only over those declared spans.
- Current sequence stitching guarantees boundary coordinate equality through a constant offset.
- Exact-head R06, Phase 01, and inherited Phase 02 workflows passed on `94b59cf...`.

### Scope

1. Merge current `origin/main` normally into the existing task branch. No rebase, force-push, reset, history rewrite, new PR, or protected-work mutation.
2. Preserve every accepted source PNG byte, runtime selection, presentation profile, strict render/compositor work, Rust/intake plumbing, and failure/recovery behavior.
3. Reclassify each frame of the six locomotion tracks from the actual rendered/accepted drawing, not label substrings alone. Record independently:
   - gait pose/phase label;
   - visible grounded sole(s);
   - anatomical/support identity;
   - swing identity;
   - support state: `single`, `double`, or `none`;
   - touchdown/toe-off evidence;
   - source contact coordinate and source hash.
4. Do not infer `none` merely from `passing` or `up`. If a sole is visibly on the floor, either classify it as support with evidence or return the ambiguity as a blocker.
5. Construct stance spans across the full evidence-supported interval from touchdown/contact through release/toe-off. No one-tick or contact/down-only shortening.
6. Rebuild left and right 24 Hz actor-root plans from actual support handoffs. At a new touchdown, compute the new foot's world location from the continuous actor-root state and frozen source geometry; do not assign an arbitrary stride distance just to make the walk move.
7. For intended left travel, successive new support touchdowns must progress screen-left; for intended right travel they must progress screen-right. If frozen frame geometry/support identity produces the opposite ordering, stop and return the exact frames/coordinates rather than swapping identity to force a pass.
8. Qualify `start → loop → loop → stop`, not only one loop. The second loop must accumulate travel rather than recentering or resetting to the first loop's coordinates.
9. Require:
   - every declared planted interval: composed world-contact slip `<= 2 px`;
   - no unexplained unsupported interval while at least one visible sole is grounded;
   - no hidden actor-root reset at support handoff, loop seam, start→loop, loop→loop, or loop→stop;
   - nonzero net displacement in the intended screen direction across each repeated loop and the complete stitched sequence;
   - report net displacement, step/stride contact spacing, maximum actor-root step, and all boundary deltas without inventing a minimum stride length.
10. Add an explicit negative matrix that fails: omitted passing/up support, reversed touchdown ordering, zero-net loop travel, loop recenter/reset, >2 px planted slip, and hidden boundary teleport.
11. Produce normal-speed and quarter-speed diagnostic playback of the composed actor-root translation for left and right. This is engineering evidence only; no renewed visual approval request is required unless the evidence exposes a genuine contradiction.
12. Retain strict `RenderingServer.frame_post_draw`, compositor, source-role, Rust, failure/recovery, export/restore, and exact-source checks as regression gates.
13. Choose one final implementation SHA and require R06 + Phase 01 + inherited Phase 02 hosted workflows green on that SHA. A later documentation-only reconciliation commit need not repeat expensive CI if independently proven non-executable.
14. Return to Architect. Do not begin transition qualification or target endurance.

### Required investigation

Determine whether the frozen accepted gait geometry actually supports a coherent alternating stance model. Prefer evidence from source pixels, frame order, visible sole contact, and continuity. Do not assume the names `near`, `far`, `contact`, `down`, `passing`, or `up` are sufficient semantic truth.

### External discovery

Use normal walking gait references only for the basic concept that stance continues while a foot remains in contact with the ground and ends at toe-off. Do not import human gait percentages, anatomy, speeds, or stride dimensions as product requirements.

### Authority boundaries

- Operator-approved R05 visual pixels remain final visual authority.
- C03 may alter metadata, evidence, root translation, and validation only.
- Godot remains presentation/runtime adapter, not identity authority.
- No model-generated semantics may override contradictory visible evidence.

### Acceptance criteria

C03 is accepted only if both left and right locomotion provide an evidence-complete support timeline and a cumulative travel plan satisfying all of the following:

- support/swing state exists for every locomotion frame;
- visible grounded support is not silently omitted;
- stance spans cover the full visible support interval;
- touchdown ordering progresses in the intended direction;
- two consecutive loops accumulate nonzero displacement in that direction;
- every planted interval has `<=2 px` composed world slip;
- start→loop→loop→stop has no hidden reset/teleport;
- exact frozen PNG hashes remain unchanged;
- strict render/compositor/Rust/failure/recovery regressions remain green;
- R06, Phase 01, and inherited Phase 02 pass on one implementation SHA.

### Required validation

Publish per-frame support tables, per-tick root/contact records, touchdown-order tables, two-loop cumulative translation evidence, normal/quarter composed playback, negative matrix, immutable-source hashes, and hosted logs/artifact identity.

### Prohibited claims

Do not claim Phase 02 acceptance, complete embodiment, production reliability, full animation library, organism behavior, memory, perception, speech, learning, caregiving efficacy, transition qualification, or Openbox endurance.

### Stop and return to Architect if

Stop if the frozen accepted drawings cannot yield a consistent alternating support model with forward touchdown ordering and cumulative travel without changing pixels, inventing a stride distance, or falsifying support identity. Return the exact conflicting frame IDs, source hashes, visible sole coordinates, proposed support identities, and why every truthful assignment fails.

### Required project updates

Update the active task packet, evidence/learning/outcome records, Notion Phase 02 directive/report, PR #9, and Issue #8 with the bounded C03 result. Preserve negative evidence.

### Required handoff

Return `# CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C03` with: Verdict; Retrieval confidence; Protected-work verification; Baseline/merge/branch state; Frozen-source identity; Retained C02 boundary; Per-frame gait/support table; Touchdown ordering; Left root plan; Right root plan; Two-loop cumulative travel; Planted-slip result; Root/loop continuity; Normal/quarter composed playback; Negative matrix; Render/compositor regression; Rust result; Failure/recovery; Export/restore; exact-head R06/Phase01/Phase02 CI; artifact identity; files changed; blockers; Notion/GitHub publication; commits/remote equality; recommendation.

## Capability boundary

R06-C02 is accepted only at the strict-render/compositor/integration and measured-geometry boundary. World-grounded locomotion remains unaccepted until C03 proves complete stance semantics and cumulative directional travel. Transition qualification and dedicated Openbox endurance remain later Phase 02 gates.