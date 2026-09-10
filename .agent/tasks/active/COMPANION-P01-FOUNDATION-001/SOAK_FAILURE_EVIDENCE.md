# Soak and Failure Evidence — COMPANION-P01-FOUNDATION-001

Status: `PENDING CODEX EXECUTION`

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
