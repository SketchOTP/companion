# Handoff — Architect Review 01 Correction

Status: `CORRECTION PUBLISHED FOR INDEPENDENT ARCHITECT REVIEW; NOT ACCEPTED`

## Retained recommendation

Retain the provisionally accepted local-first event-sourced modular companion core with consequence-driven isolation. `companion-core` is the sole writer for ordinary creature truth; `care-core` separately and deterministically owns safety-input receipts, policy evaluation, incident state, and care audit; `identity-consent-vault` explicitly owns consent, biometric/contact/credential/key material and privileged changes. Sensors/speech, models, Godot, notification, and operations remain nonauthoritative adapters.

## Seven focused corrections

1. **Independent safety ingress:** an independently authorized sensor/speech producer sends ordinary observation to companion and safety candidate directly to care. Shared immutable source IDs/digests do not create shared authority. Companion cannot validate, forward, delay, suppress, modify, or authorize safety input. Care owns the append-only receipt journal and works without the companion process/database.
2. **Vault authority:** `identity-consent-vault` owns consent/revocation, biometric templates/opaque handles, trusted contacts/roles, provider credential handles, key references/recovery metadata, and enrollment/privileged audit. Its APIs return only decisions/opaque capabilities. Absent, locked, corrupted, unavailable, and revoked states fail closed and degrade precisely.
3. **Canonical events/time:** `JCS-RFC8785-v1` and `sha-256-jcs-event-v1` define invariant bytes and digest/signature scope. Duplicate keys, invalid Unicode, NaN/Infinity, unsupported/noncanonical numbers fail. Canonical state uses bounded/fixed-point integers or canonical decimal strings. `boot_id`, `monotonic_ns`, `utc_observed`, `utc_uncertainty_us`, `event_sequence`, and `causation_id` define reboot-aware evidence; owner sequence/causation—not UTC—orders across boots.
4. **Roadmap semantics:** a distinct Roadmap Phase 01 foundation contract covers repository/environment/process/IPC/XDG/logging/health/supervisor/deterministic-control/CI/provenance foundations. “One remembered care loop plus shadow help” is a later Phase 02/03/04/10 cross-phase milestone. Passing it completes none of those phases; early care work retires authority-coupling risk rather than bypassing Phase 10.
5. **Language/toolchain gate:** EXP-00 compares Python 3.12 with exactly one Architect-selected compiled comparator from Rust or Go over equivalent frozen evidence. It selects no winner here and blocks authoritative-service implementation only, not all language-neutral Phase 01 foundation work.
6. **SQLite eligibility:** no numeric minimum is allowed. One exact currently supported non-withdrawn SQLite release or specifically documented fixed backport must have exact source/digest, binding, compile, filesystem, connection/writer/checkpoint, Backup API, migration, vulnerability, and compatibility records and pass crash/concurrent-write/checkpoint/disk-full/backup/restore/migration tests.
7. **Evidence floors:** 100 replay/restart cases, 1,000 cycles, and 30 minutes are provisional minimum engineering defect-detection floors, diversified across seeds/states/schemas/invalid inputs/kill points/persisted states/boots/property tests. They are not reliability, safety, endurance, capacity, or SLA evidence; later 24-hour, multi-day, media, shadow-safety, accessibility, pilot, and operational gates remain.

## Required negative evidence now specified

- stopped companion cannot block direct safety receipt/processing;
- forged or well-formed companion messages cannot create safety input/incident;
- duplicate safety candidates are idempotent across care restart;
- sensor/model/producer outage becomes explicit degraded coverage, never false normality;
- care starts, processes, replays, backs up, and restores without the companion database;
- mood, memory, language/model output, dreams, animation, and Godot state cannot produce or suppress a care transition;
- vault secrets/biometrics cannot reach core, model, renderer, logs, or foreign stores.

## Evidence and limitations

The accepted source reconstruction remains `E2_REPRODUCED`. The focused correction crosswalk is `E3_TARGET_TESTED` for planning-document semantics only. No product/runtime code, dependency, toolchain, database build, experiment, CI, Godot execution, media, biometric, notification, safety capability, or operational evidence exists.

Primary-source updates are RFC 8785, systemd boot/monotonic semantics, current SQLite WAL/news, and official Python/Rust/Go documentation. SQLite 3.52.0’s withdrawal disproves the earlier loose minimum but does not approve 3.53.x or another build.

## Unresolved and authority boundary

- Architecture v1.0: `RECOMMENDED / CORRECTED — NOT ADOPTED`.
- Roadmap Phase 00: `ACTIVE / INCOMPLETE`.
- Roadmap Phase 01: `CLOSED / NOT AUTHORIZED`.
- Language/toolchain comparator and winner: `OPEN / ARCHITECT DECISION AFTER EVIDENCE`.
- Dependencies, exact SQLite build, vault implementation: `NOT APPROVED`.
- Cross-phase milestone: `NOT AUTHORIZED`.
- Product implementation/capability: `NOT IMPLEMENTED / NOT ACCEPTED`.
- GitHub Issue #3: must remain `OPEN` for independent Architect review.

## Publication

- Focused correction: `25b1c737d6f8f1f861a36355909c2a51ea5c64ea` — normal fast-forward and push passed.
- Notion coder report: updated and re-fetched at `2026-09-09T16:54:10.517Z` with the focused SHA and current correction section.
- Parent Notion directive: updated and re-fetched at `2026-09-09T16:54:12.116Z` with the focused SHA and correction summary.
- GitHub Issue #3: correction comment `5605575746`; re-fetched open with seven comments.
- The one authorized reconciliation commit records these facts. Its SHA and final clean-tree/remote equality are reported in the canonical result because a commit cannot contain itself.
