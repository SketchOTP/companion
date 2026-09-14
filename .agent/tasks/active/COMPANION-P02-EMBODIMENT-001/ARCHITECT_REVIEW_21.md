# Architect Review 21 — C06-C02 Partial Accepted; C06-C03 Final Timing/Continuity Correction

## Verdict

`CONTINUE — C06-C02 PARTIAL ACCEPTED.`

Do **not** start the legal-transition campaign. Retain the valid C06-C02 corrections, but the exact hosted evidence still misses two explicit Review 20 acceptance conditions.

## Authority sync

- Reviewed implementation: `034690cab0f3b7a1bc297fed1bc0b1fa996d3511`.
- Reviewed publication head: `961b95532ab9916aa96d5a2497a11fe9879cb9d2`.
- Pre-review Architect routing head: `f508cb12b8ae5f5a31aa659f7f7eb36ecfbcdc77`.
- Hosted artifact: `10346359655`; downloaded ZIP SHA-256 matches `e97561173a1bc48447fec13e498f21d0b4de49c5b3b5d34de3cba396f2ee6cfe`.
- PR #9 remains draft/open/unmerged. Issue #8 remains open.
- Exact-head R06 `34843867410`, Phase 01 `34843867420`, and Phase 02 `34843867429` are successful on `034690c...`.
- Notion Review 21: https://app.notion.com/p/3db833cb27ff81448f03f04700628fbc

## Accepted C06-C02 boundary

Retain:

- monotonic deadline-based review timing and full-run hosted ratios `3.94813665x` left and `3.94699164x` right;
- loaded-pack-derived authored-loop ticks, frame mapping, and track-derived phase fields;
- source-pack, source-frame, and capture SHA binding;
- all 16 real non-black translated checkpoint captures;
- capture-derived strips/GIFs assembled from the hosted Godot PNGs;
- exact normal/quarter semantic checkpoint equality;
- frozen source identity, common signed-64 wire range, one paused/manual presentation clock, controller ownership, replay/cancellation/fixed-step behavior, and prior intake/Rust/render/compositor/failure/export boundaries.

## Material defect 1 — checkpoint timing requirement is not satisfied

Review 20 required every matched nonzero checkpoint to demonstrate quarter elapsed time consistent with 4x normal elapsed time within a documented bounded tolerance.

The exact artifact records:

- left `first_cruise`: `580665 us` normal vs `1496276 us` quarter = about `2.576x`;
- right `first_cruise`: `574071 us` normal vs `1492479 us` quarter = about `2.600x`;
- left `second_loop_cruise`: `1882717 us` vs `7223632 us` = about `3.837x`;
- right `second_loop_cruise`: `1883637 us` vs `7223447 us` = about `3.835x`.

Only full-run totals approach 4x. The current timing verifier validates the total ratio and semantic equality, but not intermediate checkpoint elapsed ratios.

## Material defect 2 — sequential authored-phase continuity is not independently verified

The current pack-backed verifier correctly binds each individual sample to a real pack track, duration total, frame mapping, and phase. It does not verify that authored presentation position advances by the expected amount from one cruise sample to the next or wraps correctly across the loop seam.

Its negative matrix contains no executed phase-reset/progression mutation, despite the C06-C02 result claiming that phase reset was independently rejected. A trace can remain individually pack-valid while jumping to another valid authored state unless sequential progression is checked.

## Evidence integrity

Correct C06-C02 append-only. Preserve its valid full-run timing, source/capture binding, media evidence, and exact-head CI, but withdraw the unsupported claims that checkpoint 4x pacing and phase-reset rejection are already proven.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C03

## Objective

Close only the remaining two C06 evidence defects: prove actual 4x pacing at matched semantic checkpoints and independently verify sequential pack-derived authored-time/phase continuity, including the loop seam. Correct the C06-C02 overclaim about phase-reset rejection.

## Why this is next

C06-C02 establishes real pack-derived presentation state, source/capture identity, capture-derived review media, and acceptable full-run 4x timing. Legal-transition qualification remains blocked because Review 20's checkpoint timing and sequential phase-continuity criteria are not yet proven.

## Authoritative basis

Architecture v1.0 remains adopted. Roadmap Phase 02 remains active/unaccepted. Review 20 remains historical authority; Review 21 supersedes only the unresolved C06-C02 closeout disposition and routes C06-C03. Preserve frozen R06 pack SHA-256 `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.

## Scope

1. Fetch and normally merge current `origin/main`.
2. Preserve all accepted C06-C02 behavior, capture hashes/media, source bytes, movement/controller semantics, and one-clock presentation ownership.
3. Use a monotonic review epoch and actual observation timestamps so each matched moving checkpoint can be compared independently of startup/capture fixed overhead.
4. Target true `4.0x` pacing. Do not redefine 4x as a `4.05` configured multiplier or rely on configured delay as evidence.
5. For `first_cruise`, `second_loop_cruise`, and `stop`, require observed quarter/normal elapsed ratio in `[3.90, 4.10]` independently for left and right, using a clearly defined common semantic timing origin. Preserve full-run `[3.90,4.10]` as an additional check.
6. Record raw monotonic observation timestamp and elapsed-from-review-epoch for each checkpoint; keep capture/readback completion time separate if needed.
7. Add a floating or exact authored presentation position to the trace if needed so progression is not inferred only from an integer frame/tick snapshot.
8. The shared verifier must independently derive expected presentation advancement from the loaded pack and playback rate for every adjacent cruise sample, verify modulo continuity through the 32-tick seam and into the second loop, and verify frame/phase mapping at each sample.
9. Add at least one negative mutation that changes authored position/tick/phase/frame consistently to another individually pack-valid state but violates expected sequential progression. It must fail specifically for progression/phase discontinuity.
10. Add an explicit unexpected phase-reset mutation and require rejection. Normal modulo wrap at the real loop seam must continue to pass.
11. Correct the C06-C02 result/Notion/GitHub handoff append-only: preserve its valid evidence but mark checkpoint pacing and phase-reset rejection as not established by artifact `10346359655`.
12. Re-run focused R06, Phase 01, and inherited Phase 02 on one exact final implementation SHA.
13. Return to Architect and stop.

## Do not change

No image generation, sprite editing, resampling, source reselection, new dependency, controller ownership change, command-semantics redesign, legal-transition campaign, Openbox endurance, Phase 03 work, PR #9 merge, or Issue #8 closure.

## Required investigation

Explain why the current absolute-deadline implementation produces correct full-run totals but only about `2.58–2.60x` at first cruise and `3.84x` at second-loop cruise. Define one measurement origin/observation point that is semantically comparable across normal and quarter runs and is not dominated by fixed capture overhead.

Confirm whether any current consumer depends on controller `animation_phase`; preserve compatibility, but acceptance remains pack-derived.

## External discovery

No new dependency or architecture research is authorized. Use official Godot 4.7 timing documentation only if needed. `Time.get_ticks_usec()` is suitable for precise monotonic elapsed-time measurement; SceneTree timers are frame-processed and requested delay alone is not acceptance evidence.

## Authority boundaries

- Controller owns canonical movement and command lifecycle.
- Loaded authored track owns presentation timing/frame/phase.
- Review pacing changes observation speed only, never semantic displacement or authored state.
- Render capture is evidence only.
- CI must encode the Architect criterion and may not weaken it.
- Codex may not authorize transition qualification or Phase 02 acceptance.

## Acceptance criteria

C06-C03 passes only if one exact implementation SHA proves:

- frozen source and current capture/source identity regressions remain green;
- normal/quarter semantic checkpoints remain exactly equal;
- left and right full-run quarter/normal observed ratios remain in `[3.90,4.10]`;
- left and right `first_cruise`, `second_loop_cruise`, and `stop` elapsed ratios each independently lie in `[3.90,4.10]` from the documented common review epoch;
- loaded left/right cruise tracks still derive to 32 authored ticks;
- authored presentation position advances by the pack-derived expected amount on every cruise sample;
- modulo wrap at the real loop seam passes and second-loop continuity is proven;
- a pack-valid-but-sequentially-wrong authored-position mutation is rejected;
- an unexpected phase-reset mutation is rejected;
- focused R06, Phase 01, and inherited Phase 02 pass on the same implementation SHA.

## Required validation

- Exact frozen pack hash regression.
- Capture/source SHA regression.
- Per-checkpoint monotonic timing table with explicit normal, quarter, ratio, origin, and observation point.
- Synthetic timing negatives including `3.33x` total and at least one bad intermediate checkpoint ratio.
- Positive pack-derived sequential progression verification.
- Pack-valid sequential-jump negative.
- Unexpected phase-reset negative.
- Exact-head focused R06, Phase 01, and inherited Phase 02 hosted workflows.

## Prohibited claims

Do not claim C06 complete before Architect review; checkpoint 4x pacing from total duration alone; phase continuity from individual sample validity alone; phase-reset rejection without an executed mutation; or legal-transition/Openbox/Phase 02/later organism capability.

## Stop and return to Architect if

Stop if checkpoint-wise 4x observation cannot be made truthful without changing semantic state, if sequential authored progression conflicts with the frozen pack, or if satisfying this gate requires a new dependency or architecture change.

## Required project updates

Update active Phase 02 evidence and C06 result history, dedicated Notion report, PR #9, and Issue #8. Preserve artifacts `10344096459` and `10346359655` as historical evidence, including their negative findings.

## Required handoff

Return `# CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R06-INTEGRATE-001-C06-C03` with authority sync, protected work, baseline/merge/branch state, C06-C02 artifact reconciliation, measurement-origin definition, per-checkpoint timing table, full-run timing, pack-derived sequential progression, seam continuity, progression/phase-reset negatives, retained source/capture/media verification, exact-head R06/Phase 01/Phase 02, artifact identity, files changed, failures/blockers, publication, remote equality, and recommendation.

If C06-C03 passes without another material defect, stop. The Architect will then decide whether to authorize the legal-transition campaign.
