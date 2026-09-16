# Architect Review 28 — C02 Partial Accepted; Persistent-Individual Proof Still Open

## Verdict

**CONTINUE — `COMPANION-ALPHA50-003-LIVE-001-C02` PARTIAL ACCEPTED.**

Alpha50 and Roadmap Phase 02 remain unaccepted. The next active directive is `COMPANION-ALPHA50-003-LIVE-001-C03`.

## Reviewed authority

- Architect main before review: `ac572d5f87863430de3b4fc325a73d6626961ead`
- Reviewed C02 task head: `9c83199a9beaf2fbb9ace037875035975fc8b12c`
- PR #9: draft/open/unmerged
- Issue #8: open
- Frozen R06 pack SHA-256: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`
- Phase 01, R05 and R06 PR workflows are green for the reviewed branch head.
- Alpha50 PR run `35055274200` completed **FAILURE** at the retained restart/failure step. The run produced `0/500`, `identity=null`, and zero organism snapshots in every case.
- Failed-run artifact `10430534095` is retained; ZIP SHA-256 `0d650aa6d47c4b984d2f11ab6308a9e69b3ed599032ba607fb5f8091fa307ed4`.

## Retained bounded capability

Retain as bounded implementation evidence:

- C01 producer authentication, durable replay reservation, signed-sequence exhaustion refusal and real Godot 4.7.2 render participation;
- one shared transition-authority data file and `MonTransitionResolver` used by the live director and the Godot campaign;
- bridge track selection from frozen-pack metadata instead of hard-coded track IDs;
- explicit version-neutral aliases for Goal, Commitment, EvidenceRef, MemoryRecord and BodyNeutralIntent, with V2 using those aliases;
- Alpha-life negative showing the legacy ordinary file is ignored in that explicit mode;
- corrected artifact-manifest temp-file placement outside the scanned evidence directory.

## Material findings

### 1 — Shared legality data is not one production execution path

The live director and qualification campaign call the same `MonTransitionResolver`, but the campaign invokes the resolver directly. It does not traverse the normal director/avatar/controller/render/result chain. The resident Rust bridge separately maps organism actions to pack families, selects one track from frozen metadata, and launches the R06 render-test path. Therefore legality data is shared, but live intent execution, transition qualification and result handling are still separate execution paths.

### 2 — Transition authority is not grounded against frozen track semantics

`transition_authority.json` is newly authored project graph data. Its validator checks internal consistency only. It does not reconstruct or prove the graph from the frozen pack's role/facing/posture/entry/exit/interruption semantics. The authority can therefore drift from the frozen pack without the current validator detecting semantic disagreement.

### 3 — Legacy file isolation remains mode-dependent

The hosted live trace sets `COMPANION_ALPHA_LIFE=1`, which suppresses the legacy file path and proves zero legacy events in that mode. In the ordinary-listener branch, however, the legacy reader is still gated by absence of `COMPANION_ALPHA_LIFE`, not exclusively by `COMPANION_PHASE01_COMPAT=1`. C02's explicit compatibility-only isolation requirement is not satisfied yet.

### 4 — Canonical alias promotion is acceptable direction, not complete lifecycle qualification

Promoting the shared Rust contracts to version-neutral aliases is acceptable. Their current fields remain shallow/stringly typed for several lifecycle concepts, and C02 does not establish richer V2 goal, commitment, evidence-validity, or result-causality semantics.

### 5 — Product-defining causality is still absent

The four resident paired controls, post-restart remembered-action proof and Godot-loss continuity were not run.

### 6 — Autonomy/development/memory qualification is still absent

Operative goals, evidence-gated development, consolidation, contradiction handling, rich prospective lifecycle, and a non-degenerate 30-day V2 life campaign remain unproven.

### 7 — Resilience/care/restore/model gates remain absent

The genuine multi-class failure campaign, care process-loss independence, resident clean-root restore and model-worker topology qualification remain unrun.

### 8 — Target sensor evidence remains local and ungoverned

The handoff reports `/dev/video0` and ALSA device `1`, but governed sanitized target-host evidence is not part of the reviewed exact-head artifact.

### 9 — C02 regressed the retained restart campaign

The completed Alpha50 PR run failed the old restart campaign with no snapshots and no identity in all 500 cases. The current standalone harness no longer drives `companion-core` through a supported state-producing path before restart. This negative result is preserved. C03 must repair the harness/production precondition without masking the failure, re-establish the retained restart invariant, and then replace the restart-dominated campaign with the required multi-class failure campaign.

## Evidence disposition

`CONTINUE — C02 PARTIAL ACCEPTED.`

Do not merge PR #9, close Issue #8, accept Phase 02, or accept Alpha50.

## Completion position

Evidence-grounded overall completion is **46%**, superseding Review 27's 44%.

The increment reflects shared transition authority/resolver plumbing, frozen-pack metadata track selection, canonical contract promotion direction, explicit Alpha-life legacy-file negative, and the corrected artifact-manifest construction. The failed Alpha run prevents a stronger disposition and the project remains below 50% because remembered experience has not yet been proven to alter later resident behavior through the real body across restart, while resilience/care/restore gates remain open.

## Next action

Execute only `COMPANION-ALPHA50-003-LIVE-001-C03`. C03 is the final software acceptance campaign for this Alpha milestone. It must first repair the exact-head restart regression, then collapse live embodiment and transition testing onto one production Godot execution path; prove the four resident causal comparisons plus remembered behavior after restart; complete bounded autonomy/development/consolidation; run genuine multi-class failures, care independence and resident restore; and publish governed host sensor evidence. Missing implementation or an ordinary failed test is not an authorized stop condition.