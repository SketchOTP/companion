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
