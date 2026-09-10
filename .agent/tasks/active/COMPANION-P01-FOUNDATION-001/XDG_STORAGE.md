# XDG and Storage Boundary — COMPANION-P01-FOUNDATION-001

Status: `PENDING CODEX EXECUTION`

Document the shared path-policy implementation for configuration, data, state, cache, logs, runtime sockets, backups, exports and secrets.

Required proof:

- local XDG resolution and private permissions;
- deterministic test overrides;
- repository-path rejection;
- SSHFS/network-filesystem rejection for canonical stores, WAL, locks, sockets and backup staging;
- explicit fatal/degraded outcomes instead of unsafe fallback;
- no canonical write beneath the checkout during unit, integration, Godot or soak runs;
- migration/restore paths use local ext4/NVMe.
