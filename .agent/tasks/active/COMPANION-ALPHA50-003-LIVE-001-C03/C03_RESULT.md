# C03 implementation checkpoint — 2026-09-16

Status: `CONTINUE / PARTIAL IMPLEMENTATION`; Alpha50 acceptance is not claimed.

## Restart regression repair

The C02 failure was reproduced: `companion-core` entered its ordinary-evidence
listener loop before the Alpha-life snapshot-producing branch, so the retained
standalone restart harness observed `0/500` snapshots. The failed hosted run
`35055274200` and artifact `10430534095` remain preserved as historical negative
evidence.

C03 now performs one explicit supported V2 state step during Alpha-mode service
initialization, before the listener loop. This is a production precondition for
restart qualification, not a hidden background snapshot side effect.

Local evidence after rebuilding the workspace:

- 20-case restart probe: `20/20` bounded local cases passed;
- identity remained stable across restart;
- each case produced two durable organism snapshots;
- foundation-services tests passed;
- no source art or frozen R06 bytes changed.

## Remaining C03 scope

Unified full production Godot causality, resident paired memory/learning,
remembered post-restart behavior, Godot-loss continuity, rich V2 behavior,
multi-class failure injection, care process-loss independence, resident clean
restore, model-worker topology, and governed sensor publication remain open.

Hosted push validations for implementation head `98e970854f55e263ef78b642110d396633cea833`
were dispatched as runs `35086825130` (Alpha), `35086825139` (Phase 01), and
`35086825239` (R06); results were pending at checkpoint creation.
