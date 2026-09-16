# C02 implementation checkpoint — 2026-09-16

Status: `CONTINUE / PARTIAL IMPLEMENTATION`; Alpha50 acceptance is not claimed.

Authority was merged normally from Architect `main` (`ac572d5...`). The
secondary worktree remains clean apart from this candidate change set; the
primary operator-owned `.gitignore` and `AGENTS.md` edits were not touched.

Implemented corrections:

- the authenticated ordinary-evidence UDS is now provisioned in both Alpha live
  and compatibility runs; the legacy `ordinary-observation.json` reader is
  gated by explicit `COMPANION_PHASE01_COMPAT=1` and is not live-capable;
- the live trace writes a valid legacy file while Alpha mode is active and
  proves zero `ordinary_observation` events before authenticated ingress;
- the Rust bridge resolves presentation tracks from the frozen pack's declared
  family/facing metadata rather than an action-to-track shortcut;
- Godot's 10,000-case campaign and the live director share
  `mon_transition_resolver.gd`, backed by `transition_authority.json`;
- the independent Python verifier reads the same authority data source rather
  than embedding a second transition graph;
- V2 fields now explicitly use version-neutral canonical contract aliases for
  goals, commitments, memories, evidence references, and body-neutral intents;
- the Alpha artifact manifest temporary file is created outside the scanned
  evidence directory, preventing self-inclusion of an empty `.tmp` file.

Local evidence:

- `cargo test --workspace --locked`: PASSED (26 foundation-core, 6
  foundation-services, binaries and doc tests).
- `cargo clippy --workspace --all-targets --locked -- -D warnings`: PASSED.
- schema validation, Python compilation, transition-authority validation,
  scanner self-test, and `git diff --check`: PASSED.
- local supervisor probe: legacy file produced zero ordinary events: PASSED.
- exact Godot 4.7.2, hosted C02, resident paired causality, rich V2
  qualification, multi-class failure, care-loss, clean-root restore, and
  governed target/Openbox evidence: NOT RUN or BLOCKED in this checkpoint.

The C02 changes do not create or modify character artwork and preserve the
frozen R06 pack hash. The remaining central Alpha criteria require further
resident-process qualification and Architect review.
