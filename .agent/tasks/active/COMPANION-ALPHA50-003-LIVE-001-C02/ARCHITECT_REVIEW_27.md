# Architect Review 27 — C01 Partial Accepted; Final Alpha Software Closeout Required

## Verdict

**CONTINUE — `COMPANION-ALPHA50-003-LIVE-001-C01` PARTIAL ACCEPTED.**

Alpha50 and Roadmap Phase 02 remain unaccepted. The next active directive is `COMPANION-ALPHA50-003-LIVE-001-C02`.

## Reviewed authority

- Architect main before review: `25c8a6807449046ad12071c456a47695be10282c`
- C01 executable: `794571f10e6bec1814af6b7d27da227a234f2566`
- C01 publication: `113d747cdfba2d33c8673d32233cd537448aa4ab`
- Alpha run: `35037567847`
- Alpha artifact: `10424275946`
- Independently downloaded artifact ZIP SHA-256: `7e5bada75cfff0e87ab6693898604fc71b5374775e448460473f7c31fd143e43`
- Frozen R06 pack: `1596bc28f2aac81344c4ba814a47deaa3f746e88e53278a81985977d41c8af40`
- PR #9 draft/open/unmerged; Issue #8 open.

## Retained bounded capability

Retain:

- V2-only Alpha qualification and V1 guard;
- fixed-point canonical organism numerical state;
- ordinary evidence authenticated against expected sensor-gateway PID/UID/generation and a separately provisioned HMAC domain;
- durable message reservation before V2 mutation and restart-persistent duplicate checking direction;
- fail-closed signed-64 intent sequence exhaustion;
- real Godot 4.7.2 R06 invocation with `RenderingServer.frame_post_draw` observed before companion outcome learning;
- exact-head CI and all accepted Phase 01/C06 regressions.

## Material findings

1. **Transition qualification is not production routing.** `godot/alpha50_transition_campaign.gd` contains a second hard-coded graph and `_resolve()` implementation. It executes in Godot but does not invoke the live R06 production resolver/director/controller path. The Python verifier duplicates the same graph. Treat this only as Godot-hosted transition-model evidence.
2. **Real Godot execution is still a narrow adapter.** The Rust bridge hard-codes `listen/acknowledge -> track 05`, all other actions -> track 00, and invokes `r06_black_pack_test.gd`. This proves real renderer participation but not general production embodiment routing.
3. **Resident paired causality is not proven.** Preference, correction, commitment and learned-result comparisons plus post-restart remembered behavior remain unrun through the real authorized producer -> companion -> Godot chain.
4. **V2 Rust typing is ambiguous.** V2 still imports historical `Goal`, `Commitment`, `MemoryRecord`, `EvidenceRef` and `BodyNeutralIntent`. C02 must either promote those shared types explicitly as version-neutral canonical contracts or define V2-native replacements.
5. **Long-horizon autonomy is degenerate.** Daily 30-day samples remain all `acknowledge`; operative goals/development/retrieval/consolidation and varied consequences remain unqualified.
6. **Failure and care gates remain open.** `failures.json` is still repeated restart evidence and `care.json` remains direct-care smoke.
7. **Resident restore/model independence remain open.** The actual resident stack has not booted from clean-root restore, and model-worker independence is not topology-qualified.
8. **Target sensor evidence is not governed yet.** The handoff reports bounded host camera/mic capture, but reviewed exact-head artifacts do not contain sanitized target-host records.
9. **Artifact hash manifest still includes an empty temporary file.** Redirection creates `artifact-sha256.txt.tmp` before `find`, so it is hashed as an empty file. Exclude temp files or write outside the scanned directory.
10. **Legacy ordinary file ingress remains live-capable.** The exact C01 resident ordinary-listener loop still reads `ordinary-observation.json` whenever `COMPANION_ALPHA_LIFE` is absent—the same condition under which the ordinary UDS listener is created. The positive Alpha trace does not use the file, but the alternate unauthenticated path remains available. C02 must gate this behind an explicit compatibility-only test flag and prove that Alpha live mode ignores/rejects the file without organism/event mutation.

## Completion position

Evidence-grounded overall completion is **44%**. This supersedes Review 26's 39%.

A complete C02 central-software closeout may support approximately **52–55%** after independent review. The dedicated Openbox target may remain an explicit physical blocker.

## Next action

Execute only `COMPANION-ALPHA50-003-LIVE-001-C02`. Do not merge PR #9, close Issue #8, accept Phase 02, or self-assign Alpha/completion acceptance.