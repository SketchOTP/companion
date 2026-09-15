# Architect Review 26 — Alpha50-003 Partial Accepted; Auth + Real Godot Closeout

## Verdict

`CONTINUE — COMPANION-ALPHA50-003-LIVE-001 PARTIAL ACCEPTED`.

Alpha50 and Roadmap Phase 02 remain unaccepted. Execute only `COMPANION-ALPHA50-003-LIVE-001-C01` next.

## Authority sync

- Architect main before this review: `5e13d934bce0c14531763dc1fcdaf9b9e54cb7ad`.
- Reviewed executable head: `d484c0370512ab3bb9fbcebaf99b9e44a718cdba`.
- Reviewed publication head: `299886beb2dac046e9ba5a25055f5f51c34eb9df`.
- PR #9 remains draft/open/unmerged.
- Issue #8 remains open.
- Exact-head Alpha push run `35026682276` succeeded at `d484c037...`.
- Alpha artifact `10419532624` is bound to that SHA. Independent ZIP SHA-256: `6694a8f2cdf022a59f5ca8598487ba7846867e25089e309f5d42118a6c644b2e`.
- Phase 01 `35026685839`, focused R06 `35026686022`, and inherited Phase 02 `35026685797` are green on the same executable SHA.
- Frozen R06 pack remains `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`.

## Retain

Retain as bounded candidate evidence:

- host read-only XDG inspection found no potentially lived V1 organism snapshots in the observed companion authority store;
- Alpha qualification is V2-only and guarded against V1 acceptance regression;
- fixed-point V2 numerical state and signed-64 sequence design;
- V2 preference/correction/commitment/outcome plumbing;
- separate typed ordinary-evidence UDS architecture;
- same-UID peer credential plus digest-integrity prototype;
- resident companion ordinary→V2→body-intent→Rust bridge-result→learning→snapshot plumbing;
- exact-head CI, scanner correction, capability-matrix corrections, and Phase 01/C06 regressions.

## Material findings

### Ordinary evidence is not yet producer-authenticated

The receiver checks effective UID and a self-computable unkeyed SHA-256 digest. It does not bind the peer to the authorized sensor-gateway PID, generation, or capability. The hosted positive trace is sent directly by Python while declaring `source=sensor-gateway`. This is same-UID integrity evidence, not accepted producer authentication.

### Replay/idempotency is process-local

The received-message set is in memory and resets across companion restart. Durable replay rejection must occur before V2 mutation.

### Legacy ordinary file ingress is still available in live service mode

The UDS listener loop also observes `ordinary-observation.json` under the same live-mode condition. The compatibility fixture must be isolated from Alpha live operation.

### Bridge result is not a real Godot result

The Rust `godot-bridge` immediately echoes a successful typed result for `body_intent`; the live trace does not start Godot 4.7.2 or execute the frozen presentation pack.

### Transition legality remains Python-owned

The 10,000-case campaign still executes the historical Python resolver, not production Godot routing.

### Sequence exhaustion can re-emit signed-64 max

After exhaustion the current V2 path can reset to max and emit the same maximum sequence repeatedly. Exhaustion must refuse further canonical intent emission.

### Long-horizon autonomy remains shallow

The V2-only qualification is an improvement, but daily samples remain dominated by one pending commitment and operative goals, development, consolidation, contradiction handling, and rich commitment lifecycle are unproven.

### Failure and care independence remain below directive

The 500-case campaign remains repeated orderly restart. Care remains inherited direct-care smoke rather than kill-companion/kill-care qualification.

### Restore/model outage remain bounded

The real resident service is not started from the restored clean root, and model-worker outage is not independently demonstrated through process/topology evidence.

### Physical sensors now exist on the target host

Video and audio devices are present. The next correction must attempt bounded low-level acquisition through sensor-gateway without semantic recognition claims. Openbox remains legitimately blocked without prohibited host reconfiguration.

## Completion position

Review 26 supersedes Review 25's 35% estimate. Evidence now supports **39% overall completion**.

If `COMPANION-ALPHA50-003-LIVE-001-C01` closes the central software boundary, independent review may support approximately 50–53% while unavailable Openbox remains an explicit blocker and semantic vision/STT/TTS/live escalation/release remain incomplete.

## Next action

Execute only `.agent/tasks/active/COMPANION-ALPHA50-003-LIVE-001-C01/DIRECTIVE.md`.
