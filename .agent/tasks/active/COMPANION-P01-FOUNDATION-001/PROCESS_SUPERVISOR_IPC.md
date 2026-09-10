# Process, Supervisor and Direct-Care IPC — COMPANION-P01-FOUNDATION-001

Status: `PENDING CODEX EXECUTION`

Document the implemented process graph and authority boundaries for:

- `ops-supervisor`;
- `companion-core`;
- `care-core`;
- `identity-consent-vault`;
- `sensor-gateway`;
- `godot-bridge`.

For each process record startup dependencies, owned mutable state, allowed filesystem/device/network access, IPC endpoints, health/readiness, shutdown, restart and degraded behavior.

Required proof:

- dependency-ordered startup;
- bounded restart/backoff and crash-loop visibility;
- capability generation/revocation;
- actual private `SOCK_SEQPACKET` direct-care transport;
- kernel credentials and pidfd/generation checks;
- idempotent care-owned receipts;
- valid operation with `companion-core` and its store absent;
- same-user unauthorized-client, replay, malformed, stale generation/capability and descriptor-inheritance negatives;
- care outage creates explicit degraded coverage;
- no companion, Godot, model, mood, memory or language message can create/suppress a care transition.

State the exact bounded threat ceiling. Do not claim security certification or spoken-help capability.
