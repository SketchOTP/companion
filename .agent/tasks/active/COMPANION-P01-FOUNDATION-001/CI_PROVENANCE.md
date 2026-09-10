# CI, Security and Provenance — COMPANION-P01-FOUNDATION-001

Status: `PENDING CODEX EXECUTION`

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
