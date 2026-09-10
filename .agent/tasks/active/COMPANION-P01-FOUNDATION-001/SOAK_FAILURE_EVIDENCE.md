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
`scripts/failure_matrix.py`. The required soak was run with
`scripts/soak.py --duration-seconds 3600 --interval 60`; the sanitized result
below records the exact timestamps, sample count and failures. Each sample is
a bounded supervisor invocation at the requested interval, not a continuous
resident runtime. No product SLA, reliability or safety claim is inferred from
these engineering floors.

## Final soak result

The sanitized run returned `PASS` with 60 samples and no failures over the
required 3,600 seconds. It started at `2026-09-10T01:17:56Z` and ended at
`2026-09-10T02:17:59Z`, using the release `ops-supervisor` build from the task
branch. Each sample was a bounded supervisor invocation at a 60-second
interval; this is not a continuous resident runtime or production reliability
claim. The raw sample output remains outside Git in the private temporary
qualification area; the committed summary is
`evidence/phase01-foundation-summary.json`.

## Review 01 continuation

The prior repeated-invocation soak is historical evidence only. The corrected
`scripts/soak.py` starts one resident supervisor, queries its private control
socket throughout the requested interval, records sanitized health hashes and
network-census values, and performs signal shutdown. A complete 60-minute run
with injected companion, producer, Godot, and care failures has not yet been
executed in this continuation; it remains `NOT RUN` until observed.
