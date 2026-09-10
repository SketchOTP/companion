# Current Project State

## Current stage

Planning Phase 02 remains the governing delivery roadmap.

Roadmap Phase 00 has satisfied its implementation-opening gate. Architecture v1.0 remains adopted. Roadmap Phase 01 — Environment and Engineering Foundation is active under `COMPANION-P01-FOUNDATION-001`.

## Active objective

Codex phase implementation is present on `codex/p01-foundation-001` in the
clean local secondary worktree and is awaiting Architect review. The submitted
foundation includes a locked Rust workspace, contracts and XDG guard, six
synthetic service shells, direct care transport, separate development-store
migrations, a neutral Godot shell, operator tooling and CI/provenance
definitions. The bounded target-host soak is recorded in the final evidence;
any production-capability claims remain explicitly out of scope until
independent acceptance.

Complete the entire Roadmap Phase 01 engineering foundation in one phase-sized run. The repository must become a reproducible, executable, observable local foundation containing:

1. a locked Rust 1.98.1 workspace and exact artifact bootstrap;
2. versioned contracts, canonical fixtures and negative tests;
3. XDG path enforcement and refusal of canonical state on SSHFS or inside the checkout;
4. Rust shells for `ops-supervisor`, `companion-core`, `care-core`, `identity-consent-vault`, `sensor-gateway`, and `godot-bridge`;
5. a direct synthetic safety path to `care-core` independent of `companion-core`;
6. separate single-writer SQLite 3.53.4 development stores;
7. a Godot 4.7.2 bounded resizable habitat shell on the selected Openbox display;
8. structured health, logging, CI, SBOM, license and provenance evidence;
9. a 1,000-cycle deterministic integration matrix and 60-minute target-host soak.

## Active directive

- Directive: `COMPANION-P01-FOUNDATION-001`
- Status: `IMPLEMENTED — AWAITING INDEPENDENT ARCHITECT REVIEW`
- Accepted qualification merge baseline: `80dab0c1942e4a799328a957331381104b892945`
- Notion directive: https://app.notion.com/p/3d7833cb27ff815ebe3ed1999f05beba
- Required Notion report: https://app.notion.com/p/3d7833cb27ff81c5b0eee3e6c98b54b5
- GitHub Issue #6: https://github.com/SketchOTP/companion/issues/6
- Active packet: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/`
- Required branch: `codex/p01-foundation-001`
- Required publication: one unmerged pull request to `main`
- Acceptance authority: ChatGPT AI Architect
- Roadmap Phase 02 and later: `CLOSED`
- Product capability claims: `PROHIBITED`

## Completed qualification gate

- Directive: `COMPANION-P00-QUAL-001`
- Final reviewed head: `75740ad399f6d3068f3061821f058a2bb461b9e6`
- Merge commit: `80dab0c1942e4a799328a957331381104b892945`
- Architect acceptance: https://app.notion.com/p/3d6833cb27ff819fabc2e5c9cb443aae
- GitHub PR #5: merged
- GitHub Issue #4: closed as completed
- Archived packet: `.agent/tasks/completed/COMPANION-P00-QUAL-001/`

The accepted evidence remains bounded. It establishes no organism, memory, embodiment, speech, vision, learning, dreaming, caregiving, notification, security-certification, lifetime-reliability or product capability.

## Adopted Phase 01 technology direction

- Authoritative service foundations: Rust 1.98.1.
- Python: qualification tooling and future nonauthoritative model/perception adapters only.
- Embodiment engine: exact official Godot 4.7.2 Linux x86_64 artifact.
- Persistence: exact SQLite 3.53.4 for separate single-writer local development stores; release qualification remains conditional.
- Direct-care transport: supervisor-created private `AF_UNIX` `SOCK_SEQPACKET`, kernel credentials, pidfd/generation binding, rotated capability material and care-owned receipts under the documented threat ceiling.
- Supervision: project-owned Rust `ops-supervisor`; systemd-user may be an optional non-installed outer launcher.
- Canonical event profile: `JCS-RFC8785-v1` / `sha-256-jcs-event-v1`, bounded to authoritative integer/fixed-point/string values.
- Storage: local XDG paths on ext4/NVMe; no canonical database, WAL, lock, runtime socket or backup staging in the SSHFS checkout.

Exact runtime crate versions remain subject to the active directive's dependency envelope, locks, rights review and Architect acceptance of the resulting pull request.

## Protected operator work

The primary SSHFS worktree has operator-owned uncommitted changes to root `.gitignore` and `AGENTS.md`. Codex must not read their modified contents into evidence, commit, discard, reset, overwrite, stash, reformat or otherwise alter them. Work must use a clean secondary worktree on local ext4/NVMe.

## Foundation boundary

Phase 01 may implement engineering foundations and synthetic process/store/IPC behavior only. It may not implement or claim:

- mon personality, real needs, drives, goals or autonomy;
- long-term memory, learning or dreaming;
- production sprites or Phase 02 embodiment capability;
- webcam/microphone capture, STT, TTS or model inference;
- biometrics, real user/contact data or notification delivery;
- live spoken-help detection, care escalation or safety efficacy;
- medical, emergency, security-certification, reliability or SLA claims.

## Canonical snapshots

After the Phase 00 acceptance decisions, the Architecture Decision Ledger contains 52 records by construction: 31 Adopted, 19 Interim and 2 Rejected. The latest Research Evidence Register snapshot is 55 records. Codex must query live Notion before relying on counts.

## Delivery cadence

Normal work now uses phase-sized or major-milestone-sized directives with internal checkpoints. Codex must complete the whole phase while feasible and may return early only for a precise stop-condition blocker supported by evidence.

## Next review point

Codex completes the full Phase 01 task packet, pushes `codex/p01-foundation-001`, opens one pull request, publishes the complete Notion report and Issue #6 result, leaves both open, and stops for independent Architect review.
