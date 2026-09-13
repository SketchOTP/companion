# Architect Review 14 — R06-C01 Partial Accepted; Grounded Metadata and Render Commitment Required

## Verdict

`CONTINUE — R06-C01 PARTIAL ACCEPTED`

- Reviewed task head: `b446e7214cd14e530556ab558dae565ceda05f07`
- Tested executable head: `3eb24eb25ee1e33f4c018688b739182b60521132`
- PR #9: draft/open/unmerged
- Issue #8: open
- Architecture v1.0: adopted/unchanged
- Phase 01: accepted
- Phase 02: active/not accepted
- Phase 03+: closed
- Notion Review 14: https://app.notion.com/p/3da833cb27ff81d9b48bd3e2c64e018c

R06-C01 materially advances the real-art integration boundary. Retain the final-review-derived runtime selection, immutable source bytes, typed contracts, staged intake, export/restore, Rust consumption, and Godot playback plumbing. Do not reopen art generation.

R06 is not complete because the semantic metadata and render-commit evidence are not yet truthful enough for world-grounded production qualification.

## Accepted from C01

Retain:

- frozen R05 package hashes and operator visual acceptance;
- `R05_PRODUCTION_VISUAL_SELECTION_V1` derived from non-diagnostic final-review playback;
- 58 immutable 1254x1254 RGB runtime masters;
- 24 non-diagnostic playback tracks / 283 frame slots;
- `R05_BLACK_FIELD_RGB8_V1` source profile for the selected runtime set;
- source/runtime/receipt hashes;
- exact byte preservation;
- schema validation and typed Rust round-trip;
- fsync-backed staged intake and injected failure cleanup;
- missing/ineligible/corrupt failure plumbing;
- 24 Hz duration handling and real-art Godot loading/playback;
- hosted regression on the actual post-fix implementation head described below.

These establish a bounded real-art integration capability, not grounded locomotion or Phase 02 acceptance.

## CI reconciliation

The handoff calls `a2826a546c700897bb049b1ce4defc354374f76a` the executable hosted-test head, but Phase 01 failed on that SHA. The next commit,
`3eb24eb25ee1e33f4c018688b739182b60521132`, changes only `scripts/contract_closeout.py` so the new opaque-pack schema uses the actual R06 pack fixture. On `3eb24eb...`, hosted R06, Phase 01, and inherited Phase 02 PR workflows all pass.

Therefore:

- `3eb24eb25ee1e33f4c018688b739182b60521132` is the accepted tested executable head for C01;
- `b446e7214cd14e530556ab558dae565ceda05f07` is a documentation/evidence reconciliation commit only.

Do not repeat the incorrect claim that Phase 01 passed on `a2826a...`.

## Defect 1 — semantic landmarks are generated heuristics, not observed anatomy

`build_r06_c01_selection.py` currently finds a non-black foreground bounding box and derives semantic landmarks from fixed box fractions. For example, hand, eye, mouth, foot, and ground-contact locations are inferred from generic percentages rather than identified on the accepted creature drawing.

This may be useful bootstrap geometry, but it cannot be labeled an observed anatomical landmark track.

C02 must replace or explicitly demote these values. Runtime semantic landmarks used for contact, attachment, interaction, or later perception/action coordination must be grounded to the actual accepted drawing and carry provenance for how the point was established.

## Defect 2 — planted contacts and footfall events are synthetic placeholders

For every track classified as `walk`, C01 declares the left ground contact planted from tick 0 to roughly half the track and the right contact planted from half to the end. It also places `footfall_left` at tick 0 and `footfall_right` at the midpoint.

Those intervals are not derived from the actual gait phases or visible support-foot behavior. They cannot support the project world-contact claim.

C02 must derive support identity, contact start/end ticks, and footfall markers from the accepted frame sequence and actual gait-phase evidence. Contact spans may not be shortened merely to pass the slip test.

## Defect 3 — render-commit semantics regressed

`r06_black_pack_test.gd` first waits for `RenderingServer.frame_post_draw`, but if that signal is not observed it accepts a non-empty `SubViewport.get_texture().get_image()` readback as success. The subsequent caller then emits `first_frame_render_committed`.

The hosted C01 result records `SubViewport.texture.get_image`, so the fallback path was the one that qualified the run.

A non-empty readback is useful render evidence, but under the accepted C03 boundary it is not allowed to masquerade as the `first_frame_render_committed` event. Godot's own viewport guidance recommends waiting for `RenderingServer.frame_post_draw` before capture because an early viewport texture may be empty.

C02 must restore this distinction:

- `first_frame_render_committed` only after observed `RenderingServer.frame_post_draw`;
- a readback-only fallback, if retained, must have a narrower event/result name and cannot satisfy the render-commit gate.

## Defect 4 — black-field runtime check samples the wrong region

The current Godot test samples the four corners of the 640x640 viewport. The native 1254x1254 image is drawn at 0.5 scale, approximately 627x627, centered in that viewport. The outer viewport corners therefore sit outside the source rectangle and will be black regardless of whether the source field forms a visible rectangle.

C02 must sample pixels inside the transformed source rectangle, including source-corner/edge bands, and compare them against nearby habitat black. Preserve the accepted source bytes. The existing source-perimeter observation (maximum channel value 2/255) may be retained as source evidence, but runtime compositor evidence must actually inspect the rendered source field.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C02

## Objective

Preserve the accepted C01 real-art selection and integration, then make its semantic geometry, world grounding, and render evidence truthful.

## Why this is next

Selection/intake/runtime plumbing is no longer the bottleneck. The remaining R06 blocker is that semantic landmarks/contact spans are synthetic and the hosted render gate qualified through a weaker readback fallback. Transition testing would be premature until the real body is spatially grounded.

## Scope

1. Fetch and normally merge current `origin/main` into the existing `codex/p02-embodiment-001` branch. No rebase, force-push, backward reset, new PR, or protected-work inspection.
2. Preserve the exact frozen R05 review package, 58 runtime masters, 24 tracks, 283 slots, and C01 source/runtime/receipt identities unless a metadata-only revision necessarily changes pack hashes. Never change accepted image bytes.
3. Preserve diagnostics and earlier rejected studies as historical evidence only.
4. Replace synthetic semantic landmark generation with grounded annotations for every landmark that runtime behavior actually consumes in this seed pack.
5. Derive locomotion support-foot identity, contact intervals, gait phases, and footfall events from the accepted frame order/labels plus actual image evidence.
6. Produce explicit 24 Hz actor-root translation plans for left and right locomotion.
7. Validate composed world contacts during every declared planted interval.
8. Restore strict render-commit semantics.
9. Replace viewport-outer-corner black-field QA with transformed source-rectangle compositor QA.
10. Re-run schema/Rust/Godot/export/restore and exact-head hosted R06 + Phase 01 + Phase 02 regression.

## Grounded annotation requirements

Do not claim a generic bounding-box fraction is an eye, hand, mouth, or foot.

For each runtime-consumed landmark, store:

- coordinate in the native 1254x1254 source space;
- state: `visible`, `occluded`, or `not_applicable`;
- annotation method/provenance;
- source asset SHA;
- confidence/review state if machine-assisted;
- the review overlay or other inspectable evidence used to verify it.

Machine-assisted segmentation may propose candidates, but semantic points must be checked against the actual frame. It is acceptable to leave a nonessential landmark `not_applicable` or `occluded`; inventing a plausible coordinate is not acceptable.

At minimum, ground the geometry needed by this seed runtime:

- root/body placement anchor;
- visible left/right foot locations;
- planted ground contact point(s);
- head center where used;
- interaction focus for front listen/acknowledge where used.

Do not spend this directive annotating unused future attachment/object landmarks solely for completeness.

## Locomotion contact qualification

For each left/right gait sequence:

1. Identify actual gait phase per accepted drawing: contact/down/passing/up or explicit connector phase.
2. Track anatomical support identity through overlap/occlusion.
3. Declare a planted span only where the visible sequence supports that claim.
4. A planted span must cover at least two 24 Hz ticks and should cover the full observed stance interval; do not use one-tick spans to evade QA.
5. Build `MonRoot` translation at the 24 Hz master grid from the grounded support-foot track.
6. Evaluate:

```text
world_contact(t)
  = actor_root_world(t)
  + uniform_scale * (source_contact(t) - source_root(t))
```

7. Require maximum drift <= 2 px over every declared planted span.
8. Preserve the actual net locomotion displacement; do not reset accumulated root translation at a walk-loop seam.
9. Record support handoff, root position, source contact, composed world contact, and slip for every qualified tick.

The translation plan may be derived from contact geometry, but the evidence must also show that it is continuous across support changes and loop seams rather than hiding a teleport.

## Render-commit qualification

Use one canonical event definition:

- `first_frame_render_committed` requires an observed `RenderingServer.frame_post_draw` after the intended first frame has been submitted to the qualification viewport.

If the hosted renderer cannot expose that signal while a non-empty readback exists, record a distinct event such as `first_frame_viewport_readback_observed`; do not promote it to render commitment and stop for Architect review.

The test must retain the exact observation source and monotonic timestamp.

## Black-field compositor qualification

For every unique runtime master, transform known source-field sample locations into viewport coordinates using the exact runtime scale/offset.

Measure at minimum:

- transformed source corners or corner-adjacent field pixels inside the source rectangle;
- multiple edge-band points inside the source rectangle;
- nearby viewport background pixels outside the rectangle.

Record the RGB delta to the black habitat. Use the declared R05 black-field tolerance and report the maximum observed delta. Also publish a representative viewport capture. Do not infer field-free rendering from outer viewport corners alone.

If any accepted runtime master produces a visually/materially distinct field beyond the declared tolerance, stop and return that exact asset. Do not edit it.

## Required negative tests

Add targeted tests proving:

- generic bounding-box landmark placeholders cannot satisfy `grounded` annotation status;
- a missing support-foot annotation rejects world-contact qualification;
- a fabricated one-tick planted span does not qualify a multi-frame stance;
- >2 px composed slip fails;
- discontinuous root motion at a support handoff/loop seam fails;
- `SubViewport.texture.get_image` without observed `frame_post_draw` cannot emit `first_frame_render_committed`;
- viewport outer-corner-only sampling cannot satisfy black-field compositor qualification.

## Retain without rework

Do not reopen C01 selection derivation, source role separation, immutable image copying, schema split, Rust typed consumption, atomic intake, missing/corrupt/ineligible failure paths, 24 Hz duration representation, or operator visual approval unless C02 evidence directly proves a defect in one of them.

## Prohibited work

Do not:

- generate or edit character art;
- call background removal;
- repaint/recolor/resample accepted masters;
- add a new dependency;
- expand the full animation library;
- begin the legal transition campaign;
- run the two-hour Openbox endurance gate;
- start Phase 03;
- merge PR #9;
- close Issue #8.

## Hosted acceptance

Choose one final implementation SHA before publication-only reconciliation. That exact SHA must pass:

- R06 real-art workflow;
- Phase 01 workflow;
- inherited Phase 02 workflow.

Record run IDs and artifacts against that SHA. Documentation-only publication may follow without another expensive rerun if the diff is independently shown to contain no executable/workflow/schema/fixture change.

## Acceptance criteria

C02 passes only when:

- C01 runtime source selection remains byte-identical and runtime-ineligible material stays excluded;
- runtime-consumed semantic landmarks are grounded, not bounding-box guesses;
- locomotion contact spans are derived from actual gait evidence;
- left and right actor-root plans exist on the 24 Hz grid;
- every declared planted span has <=2 px composed world slip;
- no hidden root teleport exists at support changes or loop seams;
- `first_frame_render_committed` is produced only from actual `RenderingServer.frame_post_draw`;
- black-field QA samples the source rectangle itself and passes;
- Rust/Godot/failure-recovery/export-restore remain green;
- exact-head R06 + Phase 01 + Phase 02 hosted regression passes.

No Phase 02 acceptance follows automatically.

## Stop and return to Architect if

- grounded annotation reveals the accepted playback cannot support truthful planted-contact spans;
- <=2 px world slip requires source-pixel mutation or an implausible root discontinuity;
- the hosted renderer cannot provide the adopted render-commit signal;
- a runtime master exposes a visible field that cannot be removed without changing accepted pixels;
- a new dependency or architecture change is required.

## Required handoff

Return one `CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C02` containing:

- final implementation SHA and publication SHA;
- frozen-source identity confirmation;
- grounded annotation method and overlay evidence;
- locomotion gait/support/contact table;
- left/right 24 Hz root-translation plans;
- per-span world-slip results;
- render-commit observation source and event sequence;
- source-field compositor measurements and representative capture;
- negative-test matrix;
- Rust/Godot/export-restore results;
- exact-head R06/Phase 01/Phase 02 hosted runs and artifacts;
- remaining blockers;
- recommendation to Architect.

## Capability boundary

R06-C01 establishes a bounded real-art selection/intake/playback plumbing capability. Grounded semantic geometry, world-space locomotion, strict render commitment, transition qualification, Openbox endurance, Phase 02 completion, and all organism/memory/perception/speech/learning/care capabilities remain unaccepted.
