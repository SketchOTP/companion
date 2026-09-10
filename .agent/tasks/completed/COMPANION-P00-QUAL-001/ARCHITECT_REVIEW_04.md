# Architect Review 04 — COMPANION-P00-QUAL-001

## Verdict

`ACCEPTED — BOUNDED FOUNDATION QUALIFICATION`

- Reviewed task head: `75740ad399f6d3068f3061821f058a2bb461b9e6`
- Merge commit: `80dab0c1942e4a799328a957331381104b892945`
- Pull request: `#5` — merged
- GitHub issue: `#4` — closed as completed
- Canonical Notion acceptance: https://app.notion.com/p/3d6833cb27ff819fabc2e5c9cb443aae
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 00 implementation-opening gate: `CLOSED`
- Roadmap Phase 01: `AUTHORIZED UNDER A NEW DIRECTIVE`

## Accepted evidence

The Architect independently reviewed the final correction range, committed result/provenance bundle, fail-closed validator, tamper-negative result, Python/Rust/Node profile harnesses, real-process direct-care IPC harness, SQLite matrix and VFS wrapper, PR publication, and Notion report.

Accepted at the stated bounded levels:

- exact Godot 4.7.2 artifact identity and version-only execution — `E1_OBSERVED`;
- Python 3.12.3 versus Rust 1.98.1 project-profile behavior and target-host measurements — `E3_TARGET_TESTED`;
- integer/fixed-point/string canonical event profile agreement against `canonicalize@5.0.0` — `E3_TARGET_TESTED`;
- direct-care IPC candidate behavior using real processes, `SOCK_SEQPACKET`, kernel credentials, pidfd/generation, rotated capability material, replay/restart and same-user negative tests — `E3_TARGET_TESTED`;
- exact SQLite 3.53.4 single-writer WAL candidate behavior for the executed concurrency, migration, backup/restore, bounded disk-full and narrow `xSync` matrix — `E3_TARGET_TESTED`;
- transient systemd-user lifecycle feasibility — `E3_TARGET_TESTED`;
- committed evidence hashes, fixture identity, ancestry, deterministic summaries and tamper detection — `E3_TARGET_TESTED`.

## Evidence ceilings

This acceptance does not establish Companion runtime capability, safety efficacy, security certification, production reliability, realistic power-loss durability, lifetime database behavior, SLA performance, or suitability against root, kernel, full-account or fully compromised authorized-producer threats.

It does not approve any speech, vision, model, biometric, voice, notification, service or cloud dependency.

## Technology disposition

Separate Architect decisions now authorize the Phase 01 development baseline:

- Rust 1.98.1 for authoritative local service foundations;
- exact Godot 4.7.2 artifact;
- exact SQLite 3.53.4 for separate single-writer local development stores, with release qualification still conditional;
- supervisor-created private sequenced-packet direct-care transport as an interim Phase 01 implementation baseline;
- project-owned Rust supervisor with systemd-user only as an optional outer launcher.

## Delivery cadence

Future normal directives are phase-sized or major-milestone-sized and must deliver coherent executable capability packages. Narrow continuations are reserved for material correctness, safety, privacy or evidence failures.

## Next authority

`COMPANION-P01-FOUNDATION-001` is the active phase-sized directive. It must complete Roadmap Phase 01 in one coherent run or return one precise blocker with evidence.
