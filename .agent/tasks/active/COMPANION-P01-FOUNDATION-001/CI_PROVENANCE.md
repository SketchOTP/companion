# CI, Security and Provenance — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

Document all CI workflows, pinned action SHAs, exact tool versions, network use, generated artifacts and retention.

Required checks:

- Rust formatting and clippy with warnings denied;
- locked debug/release builds;
- unit, property, schema, contract, integration and negative tests;
- accepted qualification-result validator;
- Godot 4.7.2 headless project validation;
- dependency vulnerability and license review;
- CycloneDX or SPDX SBOM generation and validation;
- secret/private-data/forbidden-runtime-path scans;
- no-default-network assertions for runtime configuration;
- clean-clone reproducibility;
- concise sanitized evidence artifacts.

Record every adopted/dev-only dependency and rights disposition. No CI pass may be represented as product capability, security certification or reliability evidence.

## Implemented CI/provenance foundation

`.github/workflows/phase01.yml` uses an immutable checkout action reference,
installs only the exact Rust toolchain on the ephemeral runner, runs locked
format/lint/tests, schema validation, the retained-seed matrix, secret/private
path scans and diff checks. `scripts/generate_sbom.py` emits an SPDX-2.3
inventory to a caller-selected private output. No remote CI result is claimed
by this local execution; the workflow remains reviewable source configuration.
