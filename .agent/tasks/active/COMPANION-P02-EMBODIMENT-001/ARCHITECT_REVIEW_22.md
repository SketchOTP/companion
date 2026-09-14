# Architect Review 22 — C06 Accepted; Legal Transition Qualification Authorized

## Verdict

`ACCEPTED — C06-C03 closes R06-C06.`

Roadmap Phase 02 remains **ACTIVE / NOT ACCEPTED**. The next and only authorized campaign is `COMPANION-P02-EMBODIMENT-001-R07-TRANSITION-QUALIFY-001`. Openbox endurance, PR merge, Issue closure, Phase 03+, and all organism capability remain closed.

## Authority sync

- Reviewed C06-C03 implementation: `49d9d65e08b9c9410d8013266ed5a5a5194ff8c5`.
- Reviewed publication head: `ff8b6245c8cce9a189c4203302edb0cfd2904ffe`.
- Pre-review Architect `main`: `4853ae92d98b46371cd6c7066ba20653d0e09ecf`.
- PR #9 remains draft/open/unmerged; Issue #8 remains open.
- Hosted C06-C03 artifact: `10352161425`; ZIP SHA-256 independently matches `87765dcfa5b06c1c5be16fcf85a5ba806be29dcfcb4dc224da95b84d59dc183a`.
- Frozen R06 source-pack SHA-256 remains `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.
- Exact implementation SHA independently resolves to successful R06 run `34853256541`, Phase 01 run `34853256563`, and inherited Phase 02 run `34853256770`.
- Notion Review 22: https://app.notion.com/p/3db833cb27ff8149b3c9e1e4404a525a

## C06 acceptance

Independent artifact replay and code inspection confirm:

- true `4.0x` deadline scheduling from a common post-preload monotonic review epoch;
- left checkpoint ratios `3.93891x`, `3.98219x`, `3.99139x` and right ratios `3.95267x`, `3.97978x`, `3.99046x` for first cruise, second-loop cruise, and stop;
- full-run ratios `3.99139x` left and `3.99046x` right;
- exact normal/quarter semantic equality at matched checkpoints;
- loaded-pack-derived 32-tick authored loops and sequential cursor/phase progression through the real modulo seam and second loop;
- independent rejection of a pack-valid sequential jump as `authored_progression` and an unexpected phase reset as `authored_phase_reset`;
- independent rejection of artificial `3.33x` total timing and bad intermediate-checkpoint timing;
- all 58 runtime frame bytes match their recorded source hashes;
- runtime pack, source/capture identity, real non-black translated captures, and capture-derived review media remain intact.

No new material C06 defect was found. C06 is therefore accepted at its bounded capability boundary; this is not Phase 02 acceptance.

## Transition authority reconstruction

Earlier Phase 02 evidence is explicit that the original all-pairs transition matrix was not runtime proof: it treated known family pairs as allowed and fixed several failure counters at zero. That evidence remains superseded.

Architect Review 12 also superseded arbitrary 32-family/256-frame completion quotas for this exact operator-approved visual set. Future artwork is behavior-driven enrichment. The transition campaign must qualify the frozen accepted runtime set and fail closed for unsupported state changes; it must not generate art or fabricate missing connectors to make the graph complete.

R10 requires concrete temporal tracks with entry/exit facing and posture, interruption ranges, events, authored connectors, and legal transition behavior. Godot remains presentation-only; it cannot become canonical organism state or safety authority.

Official Godot documentation adds a relevant implementation constraint: `AnimationNodeStateMachinePlayback.travel()` may teleport to a destination when no transition path exists. Therefore bare `travel()` cannot serve as proof that a requested transition is legal. If AnimationTree is used, an explicit legal graph/path resolver must authorize the complete path first, and the accepted C06 paused/manual presentation clock must remain the sole presentation-time authority.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R07-TRANSITION-QUALIFY-001

## Objective

Establish and qualify the fail-closed legal presentation-transition graph for the frozen accepted Phase 02 runtime pack, then execute at least 10,000 deterministic semantic-intent/transition cases through the real production resolver/director path in Godot. Prove authored connector execution, interruption/continuation behavior, illegal-path rejection, and transition evidence integrity. Return before Openbox endurance.

## Why this is next

R06-C06 now proves real loaded-pack playback, controller-owned locomotion, one presentation clock, replay/cancellation semantics, fixed-step movement, truthful rendered evidence, and authored timing/phase continuity. Phase 02 still lacks accepted evidence that runtime state changes are constrained to real authored connectors rather than arbitrary family switching or synthetic all-pairs acceptance.

## Authoritative basis

- Architecture v1.0 remains adopted.
- Roadmap Phase 02 remains active/unaccepted; Phase 01 remains accepted; Phase 03+ remains closed.
- Architect Review 12 freezes the exact operator-approved visual set and closes unsolicited art generation.
- R10 governs track metadata, connectors, interruption ranges, events, and embodiment authority boundaries.
- Architect Reviews 20–22 and accepted R06-C06 evidence govern current runtime playback semantics.
- Frozen source-pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.

## Known evidence

The frozen pack has 24 tracks and 283 frame slots. It includes explicit front/left/right turn and locomotion start/loop/stop tracks sufficient to express at least these authored presentation paths:

- front neutral → authored turn to left → left neutral → authored walk start → left walking loop → authored walk stop → left neutral → authored turn to front → front neutral;
- the corresponding right-side path.

Other tracks, including construction/reference or standalone facing material, must not become transition-eligible merely because metadata fields can be made to match. Eligibility must be reconstructed from frozen source role and accepted runtime selection.

## Scope

1. Fetch and normally merge current `origin/main`. Preserve public history.
2. Preserve every accepted R06 source byte, runtime frame byte, hash, controller semantic, one-clock presentation rule, and C06 evidence result.
3. Inventory every frozen runtime track and assign an explicit role such as `state_loop`, `entry_connector`, `exit_connector`, `action_once`, `orientation_connector`, or `reference/non_transition`. Derive roles from accepted source provenance and actual track semantics; do not infer runtime eligibility from family name alone.
4. Define a deterministic legal transition graph over concrete presentation states. State identity must use the frozen metadata needed to prevent ambiguity, including facing/posture and the concrete track/role context where relevant.
5. A legal edge/path must be backed by existing frozen authored track data. Entry/exit facing and posture must compose exactly across every adjacent track in the path. Unsupported requests must reject with a typed reason; never fabricate a connector, crossfade incompatible silhouettes, or silently substitute a nearby state.
6. The legal resolver must be fail closed. It must distinguish at minimum: unknown state/track, ineligible track role, no legal path, connector mismatch, non-interruptible point, stale/replayed intent, wrong cancellation target, corrupt/missing transition data, and source/pack identity mismatch.
7. Preserve controller authority: `MonLocomotionController` remains canonical for movement command lifecycle and actor-root translation. The transition graph owns presentation routing only. It may not invent movement, identity, organism state, consent, or safety decisions.
8. Preserve the accepted paused/manual presentation clock. Do not reintroduce concurrent `AnimatedSprite2D.play()`/forced-frame timing, AnimationTree time ownership, or another clock. If AnimationTree is used for graph organization, explicitly pre-resolve and validate the path before any `travel()` call and prove that it cannot teleport past a missing edge or own presentation time.
9. Execute legal orientation and locomotion paths using the real loaded frozen pack and real production resolver/director code. Verify actual ordered track entry, frame progression, connector completion, loop behavior, exit, and destination state rather than only graph reachability.
10. Test interruption and continuation from actual declared `interruption_ranges`. Exercise the first legal tick, interior legal tick, last legal tick, and immediately outside legal ranges. An interruption may only route through a legal authored exit/connector sequence or fail closed; direct incompatible switching is prohibited.
11. If BodyA/BodyB handoff is used by production transition code, prove controlled ownership and that it does not hide incompatible state changes. If it is not used, state that explicitly rather than adding it solely for the test.
12. Run at least 10,000 deterministic semantic-intent/transition cases through one real Godot process using the production resolver/director and loaded frozen pack. Do not satisfy this with a Python-only graph model, precomputed table, hard-coded counters, or a separate reimplementation of the runtime rules.
13. Reuse the repository's retained deterministic seed authority. Discover and report the exact seed set rather than inventing a replacement. Ensure stratified coverage so randomness cannot omit an edge or negative class.
14. The 10,000-case campaign must cover every legal edge/path class, every declared illegal adjacency class, left/right start-loop-stop, front↔profile orientation, loop seams, legal and illegal interruption points, cancellation/replay lifecycle cases, missing/no-path requests, and recovery after a rejected request.
15. Store raw case-level results in an artifact-friendly machine-readable trace. Each case must bind stimulus, starting state, requested semantic intent, resolver decision, selected path or rejection reason, observed track sequence, terminal state, pack identity, and deterministic case ID/hash. Aggregate counts are secondary evidence and may not replace raw traces.
16. Render-observe at least one positive case for every unique authored connector/edge class and every materially different negative/recovery class after `RenderingServer.frame_post_draw`. The entire 10,000 cases need not each produce a PNG if raw live runtime observations are retained, but no edge class may exist only in a Python/model proof.
17. Add independent verification that recomputes graph legality from frozen track metadata and raw traces without trusting runtime PASS booleans.
18. Add tamper negatives that must fail independently: remove a required legal edge, inject an illegal all-pairs edge, alter one connector's entry/exit facing or posture, mutate an interruption range, mutate selected track/source identity, and make a resolver claim success while its observed track sequence violates the graph.
19. Explicitly detect and reject the historical anti-pattern where all known family-to-family pairs are treated as legal.
20. Keep focused R06, Phase 01, inherited Phase 02, and the new transition-qualification workflow green on the same exact implementation SHA.
21. Return to Architect and stop. Do not begin dedicated Openbox endurance.

## Do not change

No new character artwork, image generation, cutout, recoloring, resampling, source reselection, arbitrary library expansion, new dependency, model-owned routing, organism behavior, memory, perception, speech, care capability, target-host reconfiguration, two-hour endurance, PR #9 merge, Issue #8 closure, or Phase 03 work.

Do not revive the old requirement that Phase 02 needs 32 families or 256 unique frames. Do not broaden the frozen pack merely to make the graph connected.

## Required investigation

- Identify the exact runtime role of all 24 frozen tracks and explain any transition-ineligible entries.
- Identify the retained deterministic transition seed set already present in project evidence/tooling.
- Determine whether current production transition routing is in Godot, Rust, or split across the accepted bridge, and ensure the campaign exercises that exact path rather than a test-only duplicate.
- Determine whether the accepted Phase 01 transport is already part of the transition-intent path. If it can be exercised without architecture change, include it end to end. If satisfying this gate would require changing process authority or transport architecture, stop and return to Architect.
- Confirm whether any production path currently uses AnimationTree or BodyA/BodyB handoff; do not adopt either merely because Godot provides it.

## External discovery

Use official Godot 4.x/4.7 documentation only for engine transition semantics. Relevant constraints:

- state-machine travel is limited to connected transitions, but the official AnimationTree tutorial states that `travel()` teleports to the destination when no transition path exists;
- transition switch modes, priority, reset, and crossfade behavior are engine mechanisms, not project legality authority;
- `AnimatedSprite2D` animation changes reset frame state, and `animation_finished` is not emitted for looping animations.

No new package or dependency research/adoption is authorized by this directive.

## Authority boundaries

- Canonical movement and command lifecycle: controller.
- Presentation route legality: deterministic project transition graph derived from accepted pack authority.
- Presentation frame timing: accepted loaded-track/manual clock.
- Source/track identity: frozen pack/intake hashes.
- Godot render observations: evidence, not canonical state.
- Models: no ownership of transition legality or state.
- CI/verifiers: validate Architect criteria; they may not redefine them.
- Codex: implementation/evidence authority only; cannot accept Phase 02 or authorize endurance.

## Acceptance criteria

This directive passes only if one exact implementation SHA proves all of the following:

- frozen source pack and all accepted source/runtime frame bytes unchanged;
- all frozen tracks have an explicit, evidence-grounded runtime role;
- every legal graph edge is backed by real frozen authored track data;
- connector entry/exit facing and posture compose exactly along accepted paths;
- required left and right front↔profile locomotion routes execute end to end through real Godot production routing;
- unsupported/back/reference-only/ineligible routes fail closed rather than teleport, substitute, or fabricate;
- one paused/manual presentation clock remains the only presentation-time authority;
- legal interruption points route correctly and illegal interruption points reject;
- replay/cancellation and controller movement authority remain intact;
- at least 10,000 deterministic live runtime cases execute through one Godot process with complete case-level traces;
- coverage is stratified and proves every legal edge/edge class plus every required negative class was exercised;
- no all-pairs family shortcut exists;
- independent verifier reconstructs graph legality and rejects all required tamper mutations;
- real rendered observation exists for each unique connector/edge class and materially different negative/recovery class;
- transition campaign introduces no hidden movement, no source mutation, no new dependency, and no authority leakage;
- focused R06 + Phase 01 + inherited Phase 02 + transition qualification all pass on the exact same implementation SHA.

## Required validation

- Frozen pack and source/runtime hash verification.
- Complete transition-role inventory.
- Graph connectivity and exact connector-composition verification.
- Required left/right positive route traces.
- Illegal/no-path/reference-only route negatives.
- Interruption boundary matrix.
- Replay/cancellation regression.
- Single-clock regression.
- 10,000+ deterministic live Godot cases with per-case digest/trace.
- Every-edge and every-negative-class coverage report.
- Independent graph-trace verifier.
- Edge-removal tamper negative.
- Illegal-edge injection/all-pairs negative.
- Connector facing/posture mutation negative.
- Interruption-range mutation negative.
- Pack/source identity mutation negative.
- Runtime-success/observed-path contradiction negative.
- Post-rejection recovery case.
- Exact-head R06, Phase 01, inherited Phase 02, and transition workflow.

## Prohibited claims

Do not claim Phase 02 accepted, complete autonomous behavior, full animation-library completeness, universal transition coverage, legal support for a state not backed by frozen authored tracks, Openbox qualification, production reliability, or any Phase 03+ capability.

A 10,000-case count is not proof by itself. Green CI is not acceptance if the workflow does not exercise the production resolver or if its graph criteria are weaker than this directive.

## Stop and return to Architect if

Stop if:

- the accepted frozen pack lacks an authored connector required for a route that product authority says must already exist;
- track role/eligibility cannot be determined from accepted provenance;
- production routing cannot be exercised without creating a separate test-only transition authority;
- legal routing requires source pixel modification or new artwork;
- satisfying the gate requires a new dependency or process/transport architecture change;
- retaining the single presentation clock conflicts with a proposed transition implementation;
- the real 10,000-case campaign cannot run through the production Godot path without semantic shortcuts.

## Required project updates

Update the active Phase 02 evidence/history, `.agent/CURRENT.md`, `.agent/INDEX.md`, dedicated Notion report/directive, PR #9, and Issue #8. Preserve C06-C01/C02/C03 corrections and all rejected historical transition evidence append-only.

## Required handoff

Return `# CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R07-TRANSITION-QUALIFY-001` with sections:

- Verdict
- Authority sync
- Protected work
- Baseline/merge/branch
- Frozen-source verification
- Track-role inventory
- Transition state model
- Legal graph and graph digest
- Required left positive route
- Required right positive route
- Illegal/no-path routing
- Interruption/continuation matrix
- Controller/replay/cancellation regressions
- Presentation-clock ownership
- AnimationTree/BodyA-BodyB disposition
- Retained seed authority
- 10,000-case live campaign design
- Case/edge/negative coverage
- Raw trace artifact identity
- Rendered edge-class evidence
- Independent verifier
- Tamper negatives
- Exact-head R06
- Exact-head Phase 01
- Exact-head Phase 02
- Exact-head transition qualification
- Artifact identity/digest
- Files changed
- Failures/blockers
- Notion/GitHub publication
- Commits/remote equality
- Recommendation

Then stop. If this campaign passes without a new material defect, the Architect will decide whether to authorize the dedicated 1366×768 Openbox two-hour endurance gate.
