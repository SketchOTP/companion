# Architect Review 29 — C03 Restart Repair Accepted; Causal Gate Isolated

## Verdict

**CONTINUE — `COMPANION-ALPHA50-003-LIVE-001-C03` PARTIAL ACCEPTED.**

Alpha50 and Roadmap Phase 02 remain unaccepted. The broad unexecuted remainder of C03 is superseded by one bounded active directive: `COMPANION-ALPHA50-004-REMEMBERED-CAUSAL-001`.

## Reviewed authority

- Architect main before Review 29: `999f999e853fc9b8b5cd484a3b21b5f4eab95366`
- Reviewed task head: `ae227c1a273dc50d682a7dfee1972b0b114063cc`
- C03 repair commit: `98e970854f55e263ef78b642110d396633cea833`
- Exact branch-head Alpha push run `35086956393`: PASS
- Exact branch-head Alpha artifact `10442678067`, ZIP SHA-256 `1c30f5d2041677f3658a3b1f4d5aa400ea0362b9423abeceaa02440e9e8b8bab`
- Exact branch-head Phase 01 push `35086956399`: PASS
- Exact branch-head R06 push `35086956415`: PASS
- Exact branch-head R05 push `35086956350`: PASS
- Alpha PR run `35086961004`: PASS, but its checkout is the synthetic PR merge commit rather than the task-head checkout and is not labeled exact-head evidence.
- C02 failed run `35055274200` / artifact `10430534095` remain preserved as negative history.
- Frozen R06 pack SHA-256 remains `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.
- PR #9 remains draft/open/unmerged; Issue #8 remains open.

## Retained C03 result

The C02 restart regression is repaired. C03 adds one explicit supported V2 state step and durable snapshot before the ordinary listener loop in Alpha-life qualification. Exact branch-head Alpha evidence restores the graceful restart invariant at 500/500 with stable identity. This restores previously retained evidence; it is not a new multi-class resilience capability.

## Material findings

1. **C03 did not execute its central objective.** The executable change after authority merge is eleven lines in `foundation-services/src/lib.rs` for initial Alpha snapshot creation. Resident paired preference/correction/commitment/result-learning controls, remembered behavior after restart, Godot-loss continuity, rich goals/development/consolidation, multi-class failures, care independence, resident clean-root restore, model-worker topology qualification and governed sensor publication remain unimplemented or unrun.
2. **Legacy-file isolation claim is not supported by the reviewed source.** In the ordinary-listener loop, `ordinary-observation.json` is still consumed whenever `COMPANION_ALPHA_LIFE` is absent. It is not exclusively gated by `COMPANION_PHASE01_COMPAT=1`. The Alpha negative passes because its harness explicitly enables Alpha-life mode.
3. **Production body unification remains open.** The live director and transition campaign share resolver data, but the campaign calls the resolver directly while the resident bridge still uses a separate frozen-pack render-test path. The complete production intent -> director/resolver -> avatar/controller -> result chain is not yet the acceptance path.
4. **The product-defining causal fact remains unproven.** No resident paired evidence establishes that persistent memory or learned experience changes a later body action after restart.

## Evidence disposition

`CONTINUE — C03 PARTIAL ACCEPTED.`

Do not merge PR #9, close Issue #8, accept Phase 02, or accept Alpha50.

## Completion position

Evidence-grounded overall completion remains **46%**. This iteration restores a previously retained restart invariant and returns Alpha CI to green; it does not establish a new end-goal capability.

## Bottleneck selection

The dominant blocker is one missing causal fact: **does remembered experience in the persistent V2 individual actually change a later resident action through the real body after restart?**

Repeated broad directives have returned after one narrow correction. The next directive therefore isolates this causal gate instead of repeating the full Alpha checklist.

## Next action

Execute only `COMPANION-ALPHA50-004-REMEMBERED-CAUSAL-001`. Prove four paired resident causal effects and one post-restart remembered-action difference through the real production Godot body path. Resilience, care-loss, rich 30-day autonomy, clean-root restore and sensor closeout remain deferred until this decisive causal gate passes.