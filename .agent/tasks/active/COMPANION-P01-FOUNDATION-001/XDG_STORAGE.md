# XDG and Storage Boundary — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

Document the shared path-policy implementation for configuration, data, state, cache, logs, runtime sockets, backups, exports and secrets.

Required proof:

- local XDG resolution and private permissions;
- deterministic test overrides;
- repository-path rejection;
- SSHFS/network-filesystem rejection for canonical stores, WAL, locks, sockets and backup staging;
- explicit fatal/degraded outcomes instead of unsafe fallback;
- no canonical write beneath the checkout during unit, integration, Godot or soak runs;
- migration/restore paths use local ext4/NVMe.

## Implemented path guard

`foundation_core::paths::XdgPaths` supports deterministic XDG overrides,
creates private 0700 directories, rejects paths below the checkout/repository
root, and detects common network filesystem types from sanitized mount
metadata. Canonical data, WAL/lock files, sockets and backup staging therefore
fail closed rather than silently falling back. Runtime data used by tests was
outside the repository.

## Review 01 continuation

Defaults now follow the XDG specification (`.config`, `.local/share`,
`.local/state`, `.cache`, and a required private runtime directory). Missing
`HOME` or `XDG_RUNTIME_DIR` fails visibly unless the explicit isolated test
root is supplied. Relative paths, traversal, checkout descendants, unsafe
permissions/ownership, symlink escapes, and network mounts are rejected;
mount metadata failure is not treated as local. Optional cache use may degrade,
but canonical stores, WAL/locks, sockets, and backup staging never fall back to
`/tmp`.
