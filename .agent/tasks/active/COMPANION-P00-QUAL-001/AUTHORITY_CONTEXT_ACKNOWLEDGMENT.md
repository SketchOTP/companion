# COMPANION-P00-QUAL-001 — Authority Context Acknowledgment

## Correction-cycle acknowledgment — 2026-09-09

The Architect Review 01 at main `9ea7cdbb824a9d5be88181a4374df7a4e593fbbe`
was re-read before this correction. The prior in-process IPC, ordinary JSON
JCS, serial-reader, guard-only migration, and count-only restore claims are
historical and not accepted as current evidence. The corrected work is limited
to the existing qualification branch/worktree and does not alter the protected
primary Graft files.

The live ledger re-query returned 45 ADR rows and 55 Research Evidence rows.
Evidence 54 (Linux `pidfd_getfd(2)`) and Evidence 55 (SQLite official I/O,
crash, power-loss, and concurrency testing methods) were fetched and included
in the correction context. No material authority discrepancy remains.

Correction execution remains authorized only for the bounded target tests:
real process-boundary IPC, oracle-backed canonicalization/profile parity,
release-build measurements, and corrected exact-SQLite overlap/migration/
backup/fault checks. Architecture v1.0 remains adopted; Roadmap Phase 01,
dependencies, product implementation, and product capability remain closed.

Status: `COMPLETED — QUALIFICATION PREFLIGHT PASSED`

Complete this in your own words before downloading artifacts or running tests.

## Retrieval confidence

- Confidence: `ADEQUATE`
- Retrieval completed at: `2026-09-09 America/New_York`; all named Notion pages returned complete, untruncated content; both live databases returned complete result sets.
- Current `origin/main`: `fb4d4750182bae765e8366265d6cfb1ee36e105d`.
- Task branch/worktree: `codex/p00-qual-001` in a clean secondary checkout on local ext4/NVMe, based directly on that remote head.
- Issue #4 state: `OPEN`; one Architect publication-sync comment read.
- Material unavailable or contradictory authority: `NONE`. The primary checkout's local tracking ref was stale at `1ceb330…`, but read-only remote verification found `fb4d475…`; the independent secondary checkout was created directly from that verified remote head without mutating the protected primary checkout.

## Mandatory live sources

All mandatory sources: `PASSED`.

- Canonical project, end goal, roadmap, governance, Architecture v1.0, Architect Review 02, open decisions, risk register, active directive, and pending result page: fetched live on `2026-09-09`; no truncation or material contradiction. They agree that Architecture v1.0 is adopted while Roadmap Phase 01, dependency adoption, and ordinary product implementation remain closed.
- Architecture Decision Ledger: `PASSED` — `45` live rows (`27 Adopted`, `16 Interim`, `2 Rejected`). ADR-38 through ADR-45 were individually verified by ID, title, status, rationale, consequence, evidence basis, and review trigger.
- Research Evidence Register: `PASSED` — `53` live rows (`40 Grade A`, `11 Grade B`, `2 Grade C`; `40 Reviewed`, `12 Candidate`, `1 Needs Deep Review`). Evidence 47–53 verified the RFC 8785, unix(7), SQLite WAL/news, boot-time, Rust, and Python sources relevant to this qualification.

### Review 03 live re-query supersession

The Review 03 re-query returned `55` live Research Evidence Register rows,
with `42` Grade A, `11` Grade B, and `2` Grade C records. The additional live
records for Linux `pidfd_getfd(2)` and SQLite I/O/crash/concurrency methods were
available. The earlier 53-row statement is retained as historical context and
does not represent the current snapshot. Architecture decisions remain `45`
(`27 Adopted`, `16 Interim`, `2 Rejected`). Retrieval confidence remains
`ADEQUATE`; no material Notion/GitHub/repository contradiction was found.
- GitHub Issue #4 and its complete current comment set: `PASSED` — `OPEN`, consistent with the packet and Notion directive.
- Archived Architecture v1 packet and every active qualification-packet file: `PASSED` — read from the task checkout; the archive establishes the accepted architecture and the active packet establishes this bounded qualification scope.

## Architecture v1.0 acknowledgment

1. `companion-core` alone writes creature identity/epoch, organism and world state, needs/drives/goals, ordinary accepted evidence, typed memories, relationships/preferences, development/skills, and body-neutral intents.
2. An authorized producer sends ordinary observations to `companion-core` and separately addresses safety candidates to `care-core`. `care-core` alone owns accepted/rejected receipts, deterministic policy, degraded safety coverage, incidents, acknowledgments, and audit; companion state or availability cannot create, suppress, delay, or authorize a care transition.
3. `identity-consent-vault` alone owns consent/revocation, biometric templates or opaque handles, trusted contacts/roles, credential handles, key references/recovery metadata, and privileged-change audit. Its absent, locked, corrupted, unavailable, and revoked states fail closed; no foreign component substitutes cached secret/biometric material.
4. Sensors, model workers, Godot, notification transport, and operations are nonauthoritative adapters. Their output is scoped evidence, presentation state, operational status, or untrusted delivery metadata rather than canonical organism, incident, secret, or policy truth.
5. Canonical events use `JCS-RFC8785-v1` and `sha-256-jcs-event-v1` over semantic event content. Duplicate keys, invalid Unicode/lone surrogates, NaN/Infinity, unsupported numeric ranges, and noncanonical representations are rejected. Canonical truth is bounded/fixed-point integers or canonical decimal strings; `boot_id`, `monotonic_ns`, `utc_observed`, `utc_uncertainty_us`, owner `event_sequence`, and `causation_id` provide reboot-aware ordering.
6. Durable runtime artifacts use explicit local XDG paths on ext4/NVMe, never the SSHFS source checkout. Network egress is off by default.
7. Roadmap Phase 01 is the engineering foundation; the remembered-care/shadow-help proof is a later bounded Phase 02/03/04/10 milestone that completes none of those phases.
8. AF_UNIX permissions, peer credentials, and message fields alone are insufficient to authenticate a safety producer among same-UID processes. A target-host process identity/capability gate must pass before direct ingress implementation.
9. Python, Rust, an SQLite build/binding, user supervision, and cached Godot are qualification candidates only. None is production-adopted by this task.

1. sole authority of `companion-core`;
2. independent direct safety path and sole authority of `care-core`;
3. sole authority and degraded states of `identity-consent-vault`;
4. nonauthority of sensors, models, Godot, notification, and operations;
5. JCS/digest/numeric/boot-time rules;
6. local XDG/ext4-NVMe and no-SSHFS/no-default-network rules;
7. Phase 01 versus cross-phase milestone distinction;
8. IPC producer-authentication gate;
9. no production language, database build, supervisor, or Godot artifact currently approved.

## Protected local work

- Root `.gitignore` Graft edit preserved: `PASSED` — protected primary status identifies only the path; content was not copied or altered.
- Root `AGENTS.md` Graft edit preserved: `PASSED` — protected primary status identifies only the path; content was not copied or altered.
- Secondary clean worktree used: `PASSED` — qualification branch is clean on local ext4/NVMe.
- Primary worktree modified/stashed/reset by task: `NO`.

Do not copy protected file contents into this artifact.

## Qualification objective

The toolchain workstream compares equivalent synthetic service shells and recommends, without adopting, a language direction; it cannot establish product performance or reliability. The IPC workstream attacks same-user local ingress designs and selects a bounded producer-authentication candidate; it cannot defend against root, kernel, full account, or fully compromised authorized-producer compromise. The Godot workstream proves official-artifact provenance to its stated ceiling and runs only version identification; it cannot qualify rendering, display, projects, or embodiment. The SQLite workstream exercises one exact local build/configuration with bounded synthetic faults; it cannot establish lifetime reliability. The supervision workstream determines whether transient user-service probes are feasible without host changes; it cannot install or select a production supervisor.

## Hard boundary

Confirmed: no root/sudo, system package installation, host configuration, persistent services, primary Graft changes, main push/merge, product modules, Godot project/window/renderer, sprites, media, personal data, biometrics, contacts, notification delivery, live safety behavior, cloud models, dependency adoption, Phase 01 opening, or product-capability claims. All generated artifacts will remain in private local XDG qualification roots; committed work is limited to the packet, append-only governance records when required, and `experiments/p00-foundation-qual/`.

## Gate

- Mandatory sources verified: `PASSED`
- Architecture v1 understood: `PASSED`
- Protected work isolated: `PASSED`
- Clean branch/worktree established: `PASSED`
- Retrieval confidence: `ADEQUATE`
- Qualification execution authorized by this preflight: `YES`
