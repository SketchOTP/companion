# PERFORMANCE AND ENDURANCE — COMPANION-P02-EMBODIMENT-001

## 10,000-case matrix

Record retained seeds, intent categories, direction/posture transitions,
interruptions, pack swaps, missing-pack cases, exact pass/fail counts, illegal
transitions, latency distributions, and result hash.

## Two-hour playback

Record:

- exact start/end UTC and duration;
- Godot/foundation PIDs and build IDs;
- frame-time p50/p95/p99/max;
- pack-load and first-use p50/p95/p99/max;
- intent/result latency;
- RSS/VRAM where observable;
- atlas/pack residency;
- resize events;
- interruptions;
- bridge restart/reconnect;
- missing-pack degradation/recovery;
- simulated topology loss/restoration;
- resource growth;
- log volume;
- checkout/SSHFS write result;
- process-owned AF_INET/AF_INET6 census;
- failures and recoveries.

The run must fail on an unmet required invariant. Its evidence ceiling remains
bounded engineering evidence, not production reliability or an SLA.

## Executed result

The deterministic transition runner passed 10,000 cases over seeds 17, 23, and
41 with zero illegal transitions, invalid resource references, root drift, or
unrecovered bridge disconnects (`evidence/phase02/transition_matrix.json`). A
five-second synthetic smoke passed but did not start Godot or the resident
foundation. The target-host probe found no dedicated 1366×768 Openbox output
in the current session; the required two-hour continuous target-host run is
`NOT RUN` pending the authorized target display/session. No reliability claim
is made.
