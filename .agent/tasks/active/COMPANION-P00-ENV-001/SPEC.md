# COMPANION-P00-ENV-001 — Specification

## Authority

- Roadmap: Planning Phase 02, Roadmap Phase 00.
- Verified baseline: `ddb6b130ab6428a1f395cd223d309eeaa2ac7462`.
- Notion directive: https://app.notion.com/p/3d6833cb27ff81e6ab93e37fc851b49d
- Required Notion report: https://app.notion.com/p/3d6833cb27ff8159b66fdebeb690be90
- GitHub issue: https://github.com/SketchOTP/companion/issues/2
- Acceptance authority: Architect.

## Objective

Perform a privacy-safe, non-destructive, non-privileged inventory of the actual Linux host and iteration-one peripherals. Convert observed facts into a decision-ready product-contract brief for architecture v1.0 without selecting dependencies, modifying the machine, capturing private media, or implementing product functionality.

## Required outcomes

1. Sanitized machine-readable inventory of OS/session, CPU, memory, GPU and graphics APIs, storage, display, webcam metadata, audio devices and routing, installed Godot state, existing relevant tools, and safely observable always-on constraints.
2. Human-readable report separating `OBSERVED`, `INFERRED`, `UNKNOWN`, and `OPERATOR INPUT REQUIRED`.
3. Capability matrix that does not claim workload or local-model headroom without later benchmarks.
4. Product-contract brief covering all eleven current open or partially resolved RQ records by exact ID and title.
5. Architecture implications limited to constraints and options; no architecture v1.0 or dependency selection.
6. Complete evidence, privacy sanitization, Notion publication, normal GitHub fast-forward, and canonical handoff.

## Hard boundaries

- No elevated privileges, package installation, system reconfiguration, device-setting changes, service changes, or disruptive probes.
- No camera-image capture, audio recording, screen capture, or sound playback test.
- Remove private machine and account identifiers from all committed and Notion-visible output.
- No application code, Godot project, assets, dependencies, manifests, CI, deployment, models, datasets, voices, database implementation, benchmark harness, biometric operations, notifications, or safety integration.
- Do not resolve operator decisions or claim Roadmap Phase 00 complete.

## Required files

- `PLAN.md`
- `ENVIRONMENT_RAW.json`
- `ENVIRONMENT_REPORT.md`
- `CAPABILITY_MATRIX.md`
- `PRODUCT_CONTRACT_BRIEF.md`
- `ARCHITECTURE_IMPLICATIONS.md`
- `EVIDENCE.md`
- `HANDOFF.md`

The full operative contract, acceptance criteria, validation, research basis, and stop conditions are in the Notion directive and control if this summary is incomplete.
