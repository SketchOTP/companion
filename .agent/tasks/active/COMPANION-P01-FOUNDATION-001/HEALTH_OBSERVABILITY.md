# Health and Observability — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

Document the payload-minimized structured logging and health model.

Required fields and behavior:

- process, version and build identity;
- `boot_id`, local sequence, correlation and causation identifiers;
- severity, privacy class and event type;
- readiness, liveness and degraded-state transitions;
- restart, backoff and crash-loop reason;
- store, channel and Godot bridge health;
- explicit unknown/unavailable coverage;
- no secrets, capabilities, raw personal data or unrestricted payloads.

Provide and test one operator-facing health command that gives a coherent snapshot without mutating state or inventing normal coverage.

## Implemented observability

The Rust logger emits process/version/build, boot and local sequence, severity,
privacy class, correlation/causation and reason fields without payloads.
`scripts/health.py --json` is read-only, reports all six roles, XDG storage
class, SQLite availability, default-deny network policy and explicit degraded
coverage when no persistent runtime is running.

## Review 01 continuation

`ops-supervisor` is resident by default and answers a private Unix control
socket with child PID, generation, restart/backoff, role, care-coverage, boot
identifier, and default-deny network metadata. The logger uses the kernel boot
identifier and `CLOCK_MONOTONIC` rather than wall-clock nanoseconds. Health is
queried from supervisor state; unavailable control is reported explicitly, not
converted into normality. Runtime socket census remains engineering evidence.

## Architect Review 02 continuation

Health now includes observed child state/readiness, live PID, restart count,
backoff, retained producer pidfd/liveness, care coverage, and exact SQLite
runtime identity/options. The control protocol is explicit JSON and the Python
health client sends a `health` command. The no-egress checker records census
errors rather than treating inaccessible `/proc` entries as zero sockets; its
current result is `FAILED` under intentional child dumpability hardening.

## Evidence correction — 2026-09-10

The checker now classifies the expected `/proc/<pid>/fd` denial as
`blocked_by_child_dumpable_hardening` and independently observes process-owned
AF_INET/AF_INET6 sockets through `ss -H -tunp`. The corrected run observed zero
owned network sockets, live readiness, synthetic care coverage, and clean
shutdown; it did not weaken child dumpability or claim a complete host-wide
socket census.
