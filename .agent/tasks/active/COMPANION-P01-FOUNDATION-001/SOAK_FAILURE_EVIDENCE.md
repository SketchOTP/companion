# Soak and Failure Evidence — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — PARTIAL EVIDENCE — AWAITING ARCHITECT REVIEW`

## Deterministic matrix

Record at least 1,000 contract/message cycles across multiple retained seeds. Include valid, duplicate, replay, malformed, unsupported version, stale generation/capability, process restart and persistence cases.

## Target-host soak

Record at least 60 minutes of supervised foundation operation with:

- start/end time and exact build;
- process restart counts and reasons;
- peak/steady CPU and RSS per process where available;
- store integrity and checkpoint results;
- socket/channel health;
- Godot bridge/window connectivity;
- no-network/default-deny result;
- proof of no canonical checkout writes;
- log volume and secret/privacy scan;
- every warning, failure and degradation.

## Failure matrix

Exercise clean stop/start, kill/restart of every shell, crash loops, companion absence/corrupt store, care outage/degraded coverage, Godot absent/disconnected/reconnected, safe display-loss simulation, invalid contracts, storage refusal, migration failure, backup/restore and orphan cleanup.

These are engineering evidence floors, not product reliability or safety statistics.

## Current run

The deterministic matrix is implemented by `scripts/cycle_matrix.py` with
retained seeds 17, 23 and 41 and 1,000 cycles per seed (3,000 total). A
bounded clean start/stop and orphan-cleanup probe is available through
`scripts/failure_matrix.py`. The required 60-minute soak is running separately
with `scripts/soak.py --duration-seconds 3600 --interval 60`; its result will
be recorded only after the process completes. No product SLA, reliability or
safety claim is inferred from these engineering floors.
