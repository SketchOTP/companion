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
