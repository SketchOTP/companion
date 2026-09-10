# Roadmap Phase 01 engineering foundation

This repository now contains a modular Rust workspace, versioned contracts,
isolated development-store migrations, six executable process shells, a
project-owned supervisor, an independent synthetic safety transport, an XDG
path guard, a neutral Godot 4.7.2 habitat shell, and read-only operator health
tooling.

The foundation is deliberately not a product runtime. It has no organism
drives, memory, learning, dreaming, camera or microphone capture, speech or
model inference, biometrics, contacts, notifications, or live caregiving
behavior. Synthetic packets and stores are engineering fixtures only.

## Process topology

`ops-supervisor` provisions a private `AF_UNIX` `SOCK_SEQPACKET` pair, starts
ordinary shells before the direct care pair, and passes only the producer
endpoint to `sensor-gateway` and the care endpoint to `care-core`. The sender
is therefore a direct producer; companion state and the companion store are
not in the care path. Restart, backoff, and health extensions remain bounded
Phase 01 foundations rather than a security certification.

## Persistence

Companion, care, and vault each use a distinct local XDG SQLite development
store and one-writer policy. WAL and synchronous FULL are explicit. Migrations,
integrity checks, idempotent event append, backup, and fresh-directory restore
are exposed through the shared library. Release suitability remains
conditional on the accepted qualification evidence.

## Reproducibility

Use the private accepted qualification cache via `scripts/bootstrap.sh`; it
does not edit the system or commit binaries. Runtime data belongs below the
caller-selected XDG root. The CI workflow uses immutable action references,
locked Cargo inputs, schema checks, deterministic synthetic cycles, and
forbidden-path/secret scans.
