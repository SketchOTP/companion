# Current Project State

## Current stage

Planning Phase 02 — Master Delivery Roadmap remains active.

Roadmap Phase 00 — Planning and Product Contract remains active. `COMPANION-P00-ARCH-001` is accepted and complete. Architecture v1.0 is adopted. Roadmap Phase 01, dependency approval, experiments, and product implementation remain closed pending new bounded Architect authority.

## Current objective

Close and archive the accepted architecture packet, then execute the next Roadmap Phase 00 foundation-qualification directive. The critical unknowns are the Python-versus-Rust toolchain choice, enforceable process identity for direct safety ingress, exact Godot 4.7.2 artifact provenance, exact persistence artifact/build, and target-host supervision assumptions.

## Accepted architecture authority

- Canonical Architecture v1.0: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556
- Architect Review 02: https://app.notion.com/p/3d6833cb27ff81d88785f64d0629286c
- Architecture routing mirror: `.agent/ARCHITECTURE_V1.md`
- Accepted focused correction: `25b1c737d6f8f1f861a36355909c2a51ea5c64ea`
- Corrected publication reviewed: `1ceb330d4c2321b500a138b8acfdfeb4279c08e7`
- Architect acceptance records: `00dc566adf4f4210fe439b9a1a74c0ee947d79dd` and `0d8cdb7542cdbe5049b77e4074ccf3ea179e2645`
- Completed packet: `.agent/tasks/completed/COMPANION-P00-ARCH-001/`
- GitHub Issue #3: closes as completed after archive publication

## Architecture v1.0 summary

- `companion-core` is the sole writer for ordinary creature truth.
- `care-core` independently owns safety-input receipts, deterministic scenario policy, degraded safety coverage, incidents, acknowledgment state, and care audit.
- `identity-consent-vault` solely owns consent/revocation, biometric handles/templates, trusted contacts/roles, provider credential handles, key references/recovery metadata, and privileged audit.
- Authorized sensor/speech producers send ordinary observations to `companion-core` and safety candidates directly to `care-core`; companion availability or permission is not required for the care path.
- Sensor, model, Godot, notification, and operations processes are nonauthoritative adapters.
- Canonical events use `JCS-RFC8785-v1` and `sha-256-jcs-event-v1`, bounded/fixed-point numeric rules, boot-scoped monotonic time, UTC uncertainty, owner sequence, and causation.
- Runtime state uses local XDG paths on ext4/NVMe, never the SSHFS checkout.
- Outbound network is disabled by default.
- Roadmap Phase 01 engineering foundation is separate from the later Phase 02/03/04/10 remembered-care and shadow-help architecture-proof milestone.

## Mandatory implementation gates

1. Direct safety ingress requires process-level producer authentication independent of message-declared identity and same-UID socket access.
2. Authoritative service implementation requires an accepted Python 3.12 versus Rust qualification result; Rust is the selected compiled comparator, not the winner.
3. Godot 4.7.2 requires exact official artifact provenance and target-host qualification; existing 4.6 is not a substitute.
4. Persistence requires one exact supported non-withdrawn artifact/build and crash/checkpoint/disk/migration/backup/restore evidence; SQLite remains conditional.
5. systemd/user-service supervision remains conditional because accepted host evidence reported degraded managers.
6. RQ-04 and RQ-07 through RQ-12 remain open or partially resolved.

## Canonical counts after architecture adoption

- Architecture decisions: `45` total — `27 Adopted`, `16 Interim`, `2 Rejected`.
- Research evidence: `53` total — `40 Grade A`, `11 Grade B`, `2 Grade C`; `40 Reviewed`, `12 Candidate`, `1 Needs Deep Review`.

These are snapshots. Future agents must query live Notion.

## Local working-tree protection

Codex reported intentionally uncommitted user-owned Graft changes to root `.gitignore` and `AGENTS.md`. They are not part of the reviewed remote commits and have not been independently inspected through GitHub. Future Codex work must inspect and preserve them. Do not commit, discard, reset, overwrite, or reinterpret them without explicit authority.

## Hard boundary

No active directive currently authorizes product source, Godot project execution, production sprites, dependency adoption, CI workflows, deployment, biometrics, notification delivery, live safety behavior, Roadmap Phase 01, or product-capability claims.

## Next review point

A new Architect directive will define the exact foundation-qualification scope, permitted disposable experiment artifacts, source map, stop conditions, validation, Notion result, GitHub issue, and acceptance gate.
