# Architect Review 16 — C03 Stop Accepted; Travel Contradiction Not Yet Proven

## Verdict

`INVESTIGATE / CONTINUE — C03 STOP ACCEPTED; ART-CONTRADICTION CLAIM NOT YET ACCEPTED`

- Reviewed task publication head: `955a540e0e076d06821efa4318bcd99c80b4bfd9`
- C03 implementation/evidence head: `143439a8f3d4b9b4c579921254f2310bc4ed4863`
- Frozen visual head: `5f538a0c86783b7c5d00b140dcc91c7f76c30450`
- PR #9: draft/open/unmerged
- Issue #8: open
- Architecture v1.0: adopted/unchanged
- Phase 01: accepted
- Phase 02: active/not accepted
- Phase 03+: closed
- Notion Review 16: https://app.notion.com/p/3da833cb27ff8190bc08fcb33cb5a3bf

C03 correctly stopped and preserved all accepted art. Its reported opposite-direction geometry is valid diagnostic evidence for the implemented model. It is not yet accepted as proof that the frozen operator-approved drawings are inherently incapable of intended-direction locomotion.

## Decisive review findings

### 1. Runtime coordinate drift

Review 11 separated source/root coordinates from actor/world translation. The later opaque-black profile preserved native 1254x1254 image bytes and allowed metadata placement, but C03 introduces a per-frame `source_root` computed as torso-median X plus a ground baseline Y measured from foot/sole pixels.

That analysis root changes per frame and is not the coordinate transform used by current Godot playback. The C02 Godot qualification creates a centered `AnimatedSprite2D`, positions the node, applies scale 0.5 and no per-frame sprite offset. Therefore a travel-direction conclusion may not substitute a separate per-frame body/ground root unless the same transform is explicitly applied in runtime.

The torso/body anchor remains useful registration evidence, but it must be separately named from the runtime root/contact transform.

### 2. Screen-X order is not anatomical leg identity

C03 assigns two simultaneously visible grounded candidates as:

- leftmost source-X -> `ground_contact_left`
- rightmost source-X -> `ground_contact_right`

This violates Review 11's explicit rule that gait/support identity is anatomical correspondence, not whichever foot happens to appear on the left of the image. During crossing, screen-X order can reverse while the leg remains the same leg.

Profile qualification must therefore maintain a stable `near`/`far` or A/B leg identity through the track and only map that identity to anatomical left/right when separately evidenced. Source coordinate and leg identity are distinct fields.

### 3. The C03 negative matrix is not independent

The real C03 payload already fails the positive direction predicate. The validator mutates that already-failing payload and treats `not positive_predicate(mutated)` as proof that each injected defect was rejected. A pre-existing direction failure is sufficient to make every mutation look rejected.

The omitted-support mutation is also not faithful: it removes the observed grounded sole from `visible_grounded_soles` and changes the state to `none`, rather than keeping the observation and removing only the support declaration.

The seven reported negative passes therefore do not independently prove the seven protections.

## C03 evidence retained

Retain as negative evidence:

- all accepted PNG hashes unchanged;
- full per-frame contour investigation;
- current C03 support tables;
- current reported left/right opposite-direction touchdown values;
- no pixel mutation;
- no transition/endurance execution;
- the fact that the C03 implementation stops fail-closed under its own model.

Do not erase or relabel those results.

## Runtime-coordinate ruling

For the opaque-black runtime, qualification must use the transform actually executed by Godot.

Keep these concepts distinct:

- `source_pixel`: immutable 1254x1254 PNG pixel coordinate;
- `sprite_local`: source coordinate after the actual AnimatedSprite2D centered/offset mapping;
- `frame_registration_offset`: optional metadata translation only if actually applied by runtime and derived independently of foot/support state;
- `actor_root_world`: MonRoot/Node2D world position;
- `world_contact`: source contact transformed through sprite-local and actor-root transforms.

A support foot or sole baseline may not define or move the actor root.

If per-frame registration is required to reproduce the already-approved review alignment, derive it from non-foot body registration before evaluating foot-contact direction, record the evidence, and apply the exact same offset in Godot. Do not create a support-dependent offset.

Godot supports a drawing offset on Sprite2D/AnimatedSprite2D separately from Node2D position, so runtime placement can remain metadata-driven without changing source bytes.

## Leg-correspondence ruling

For profile locomotion, maintain one stable leg identity through occlusion and crossing.

Use `near`/`far` or another stable A/B identity where anatomical left/right is not visually certain. Do not infer identity from current screen-X position. Double support must preserve both contact coordinates.

A filename/action label may support correspondence but cannot overrule contradictory visual evidence.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C04

## Objective

Re-run only locomotion qualification using the actual runtime transform and stable leg correspondence, then determine whether C03's opposite-direction result survives those corrections. Generate or edit no character pixels.

## Why this is next

C02's immutable selection, intake/Rust/Godot integration, strict render commitment, compositor qualification, failure/recovery and export/restore are retained. C03 reached a genuine stop, but its causal conclusion is confounded by root/coordinate and leg-identity semantics. Resolving those semantics is the minimum decisive action before reopening art or moving to transitions.

## Scope

1. Fetch current `origin/main` and normally merge it into the existing Phase 02 branch.
2. Preserve all C02 accepted engineering evidence and all C03 negative evidence.
3. Document the exact source-pixel -> sprite-local -> world transform used by current Godot playback, including texture dimensions, `centered`, sprite/node position, scale, and any offset.
4. Remove the C03 torso-centroid/ground-baseline value from the meaning of runtime `source_root` unless that exact transform is actually applied in Godot. Keep body-registration observations separately named.
5. Establish stable `near`/`far` or A/B leg correspondence through each left/right start/loop/stop sequence. Never derive identity from source-X order alone.
6. Reclassify support/swing/double-support from actual frame evidence; preserve ambiguity instead of forcing a pass.
7. Recompute `start -> loop -> loop -> stop` world contacts and actor travel using the exact runtime transform. No invented stride distance, hidden recenter, or support-dependent registration.
8. Publish old-C03 versus corrected-C04 touchdown/world-travel results side by side and explain any sign change.
9. Replace the C03 negative-test methodology with isolated predicates: start from a known-positive minimal gait fixture or otherwise ensure each mutation is evaluated from a passing baseline. The omitted-support test must retain the observed grounded sole and delete only the support declaration.
10. Add a leg-identity/screen-X swap negative and a support-dependent-root/registration negative.
11. If corrected real-art qualification passes, publish normal/quarter composed playback and run exact-head R06 + Phase 01 + inherited Phase 02 CI.
12. If corrected qualification still fails, stop and return exact stable leg identities, runtime-local contacts, registration offsets, touchdown world coordinates and contradiction.

## Acceptance criteria

C04 passes only when:

- coordinate semantics match the transform actually executed by Godot;
- source PNG bytes remain unchanged;
- leg identity is stable through crossing and is not screen-X identity;
- every evidence-supported stance interval is represented;
- left/right cumulative travel has the intended sign without arbitrary stride injection;
- two loops accumulate rather than recenter;
- planted world slip remains <=2 px;
- no hidden root/reset/teleport is used;
- negative protections are independently demonstrated from a passing baseline;
- exact-head R06 + Phase 01 + Phase 02 are green if the real-art path passes.

If the corrected runtime-transform model still proves opposite-direction travel, return `BLOCKED`. That result will be accepted as a real visual-source contradiction and routed to an explicit Architect/operator decision. Do not alter art automatically.

## Prohibited work

No image generation, pixel editing, cutout/background removal, recolor, resampling, arbitrary stride injection, screen-X leg relabeling, transition campaign, Openbox endurance, PR merge, Issue closure, dependency adoption, or Phase 03 work.

## Required handoff

Return:

```text
# CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C04

## Verdict
## Retrieval confidence
## Protected-work verification
## Baseline / merge / branch state
## Frozen-source identity
## Retained C02/C03 evidence
## Actual Godot coordinate transform
## Root / registration semantics
## Stable leg-correspondence method
## Per-frame support table
## Old C03 vs corrected C04 comparison
## Left two-loop travel
## Right two-loop travel
## World-contact slip
## Root / seam continuity
## Independent negative-test matrix
## Normal-speed composed playback
## Quarter-speed composed playback
## Render / compositor regression
## Rust / intake result
## Failure / recovery
## Export / restore
## Exact-head R06 CI
## Exact-head Phase 01 CI
## Exact-head Phase 02 CI
## Artifact identity
## Files changed
## Failures / blockers
## Notion / GitHub publication
## Commits and remote equality
## Recommendation to Architect
```

## Capability boundary

C03 does not reduce the accepted C02 boundary. Phase 02 remains unaccepted. Transition qualification and dedicated 1366x768 Openbox endurance remain closed pending C04. No organism, memory, perception, speech, learning, development, dreaming, caregiving or Phase 03+ capability is accepted.