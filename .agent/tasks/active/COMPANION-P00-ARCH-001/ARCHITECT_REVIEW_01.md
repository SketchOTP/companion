# Architect Review 01 — COMPANION-P00-ARCH-001

Status: `CONTINUED — FOCUSED CORRECTIONS REQUIRED`

Acceptance authority: `ChatGPT AI Architect`

Reviewed range: `6559cec1beaf27bf958c2b9517b0717f04c83ea9..d8c7209e0ec0370c17fc4cf980fde879e54f10b5`

Planning result: `5d6d87d93b017e42647e260b69d80b5ad3f8becc`

Publication head reviewed: `d8c7209e0ec0370c17fc4cf980fde879e54f10b5`

Canonical Notion review: https://app.notion.com/p/3d6833cb27ff81bd834cf3693f8ae9a5

GitHub Issue #3: https://github.com/SketchOTP/companion/issues/3

Architecture v1.0 adoption: `NOT GRANTED`

Roadmap Phase 01: `CLOSED`

Product implementation: `CLOSED`

## 1. Independent review performed

The Architect independently inspected the normal two-commit fast-forward, all changed paths, current `main`, the Notion coder report, authority acknowledgment, architecture alternatives, recommended architecture, process/privilege/data boundaries, product-contract dispositions, first vertical-slice contract, dependency/rights matrix, threat/privacy/claims model, repository/CI/test/release plan, experiment plan, traceability, evidence, and handoff.

Live Notion state was independently reproduced:

- Architecture Decision Ledger: `37` total — `21 Adopted`, `14 Interim`, `2 Rejected`.
- Research Evidence Register: `46` total — `33 Grade A`, `11 Grade B`, `2 Grade C`; `33 Reviewed`, `12 Candidate`, `1 Needs Deep Review`.
- ADR-33 through ADR-37 matched their exact live titles, statuses, rationales, and consequences.
- GitHub Issue #3 remains open.
- Current result head has no CI/status checks, which is expected for a planning-only repository.

## 2. Accepted foundation

Do not repeat or rewrite these accepted parts unless a live authority changes:

- Complete source reconstruction and `ADEQUATE` context acknowledgment.
- Governance/planning-only scope and normal fast-forward publication.
- Local-first cohesive companion core with consequence-driven edge isolation as the preferred topology direction.
- Independent deterministic `care-core` as a separate authority and store.
- Nonauthoritative sensor, model, Godot, notification, and operations adapters.
- Local XDG state on ext4/NVMe and no canonical runtime state on SSHFS.
- No outbound network by default.
- Typed/versioned local IPC, explicit degradation, one writer per mutable authority class, owner portability, artifact-specific rights, and narrow Kentucky/nonmedical claims boundaries.
- The remembered-interaction plus shadow-help concept as a valuable integrated architecture proof, subject to the phase and contract corrections below.
- No dependency, RQ, architecture, phase, or product capability was self-approved.

## 3. Material corrections required

### 3.1 Safety evidence must bypass companion authority

Current inconsistency:

- `PROCESS_PRIVILEGE_DATA_BOUNDARIES.md` assigns durable perception evidence to the `companion-core` evidence ledger and says care reads scoped views.
- The same file's spoken-help flow describes audio/ASR evidence entering `care-core` directly.
- `RECOMMENDED_ARCHITECTURE.md` says `care-core` may continue its already-qualified input path when `companion-core` is unavailable, but the direct independent input path is not defined.

This is architecture-blocking. A failed, compromised, or stalled companion core must not be able to delay, suppress, rewrite, or be required to forward a safety candidate.

Required correction:

1. Define an authenticated direct path from the authorized sensor/speech producer to `care-core` for safety candidates.
2. Make `care-core` the sole writer of an append-only safety-input receipt/journal and all incident state.
3. Permit `companion-core` to receive a separately authorized copy for ordinary interaction, but it may not validate, gate, suppress, authorize, or be required for the care transition.
4. Preserve the source `message_id`, producer identity, provenance, freshness, quality, replay/media flags, and evidence digest across scoped receipts without creating shared mutable truth.
5. Define common-mode sensor/model failure as explicit degraded care coverage.
6. Add negative tests proving:
   - `companion-core` outage cannot suppress delivery to `care-core`;
   - a compromised or malformed companion message cannot create a care input;
   - companion mood, memory, LLM output, and dream content cannot manufacture, suppress, or authorize a care transition;
   - duplicate safety candidates remain idempotent inside `care-core`.
7. Update every affected architecture, boundary, slice, threat, traceability, evidence, and handoff statement.

### 3.2 Add an explicit identity/consent/contact/secret authority

Current gap:

- The trust-zone and state tables refer to a future vault.
- The recommended process map does not fully define the authoritative vault responsibility required by the directive.

Required correction:

1. Add an explicit `identity-consent-vault` or equivalently named architecture component/process.
2. Make it the canonical owner of:
   - consent grants and revocation;
   - biometric templates or opaque biometric handles;
   - trusted-contact records and role bindings;
   - provider credential handles;
   - encryption-key references/recovery metadata;
   - privileged enrollment/change audit.
3. Keep secrets and biometrics out of Godot, model workers, logs, `companion-core`, and `care-core` stores.
4. Define minimum interfaces and capability handles without selecting an encryption implementation.
5. State what is absent or stubbed in the first slice.
6. Define startup and degraded behavior when the vault is absent, locked, corrupted, or unavailable.

### 3.3 Specify canonical event bytes, numeric rules, and reboot epochs

Current gap:

- The slice requires byte-stable normalized events and projection hashes.
- JSON Schema validates structure but does not define invariant byte serialization.
- Monotonic timestamps are included without a boot/clock epoch, even though monotonic time resets at reboot.

Required correction:

1. Select RFC 8785 JSON Canonicalization Scheme or define an equivalent versioned canonical event encoding.
2. Define the exact content covered by an event digest/signature and how envelope/signature fields are included or excluded.
3. Define canonical numeric rules:
   - use bounded integers/fixed-point integers or canonical decimal strings for canonical organism, policy, and event values where precision matters;
   - prohibit duplicate JSON keys;
   - reject NaN, Infinity, unsupported numeric ranges, and noncanonical representations at authority boundaries;
   - do not depend on platform-specific floating-point serialization for canonical state.
4. Add `boot_id`, `clock_epoch`, or an equivalent identifier beside monotonic time.
5. Use owner event sequence and causation as authoritative ordering across boots; treat UTC as an observed wall-clock value with uncertainty.
6. Update deterministic replay, hashing, golden fixtures, schema validation, and cross-reboot tests.

Primary source: RFC 8785 defines canonical JSON for repeatable hashing/signing, uses deterministic property sorting, constrains input to I-JSON, rejects NaN/Infinity, and recommends strings for values outside interoperable number precision: https://www.rfc-editor.org/rfc/rfc8785.html

Primary source: systemd documentation states that monotonic time starts again each reboot and is well-defined across records only when paired with a boot identifier: https://www.freedesktop.org/software/systemd/man/sd_journal_get_cutoff_realtime_usec.html

### 3.4 Preserve roadmap phase semantics

Current inconsistency:

- `VERTICAL_SLICE_CONTRACT.md` calls the proposal a `PROPOSED PHASE-01 CONTRACT`.
- The accepted roadmap defines Phase 01 as environment and engineering foundation.
- The slice includes bounded work from Phase 02 embodiment, Phase 03 organism, Phase 04 evidence/memory, and Phase 10 care-core foundation.

Required correction:

1. Define a separate Roadmap Phase 01 engineering-foundation acceptance contract.
2. Reclassify the remembered-interaction plus shadow-help slice as a named cross-phase integration milestone, or place it after explicit prerequisite phase/subphase gates.
3. List which roadmap phases contribute bounded work.
4. State explicitly that passing the slice does not mark those roadmap phases complete.
5. Preserve early verification of care/companion separation without silently collapsing Phases 02–10.
6. Update the roadmap/phase traceability and entry gates accordingly.

### 3.5 Add an implementation-language/toolchain evidence gate

Current gap:

- The dependency matrix retains Python and Rust/Go as candidates.
- The experiment plan does not define how the core/care language, packaging, and toolchain will be selected.
- Phase 01 cannot create a reproducible production foundation while this choice remains implicit.

Required correction:

1. Add a bounded language/toolchain experiment or decision gate.
2. Compare the smallest credible set, for example Python 3.12 and one compiled candidate selected from Rust or Go.
3. Evaluate deterministic behavior, type/schema tooling, process isolation, packaging, startup/RSS, dependency and native-library surface, security maintenance, update/rollback, long-term support, developer velocity, testability, and target-host fit.
4. State whether the result blocks all Phase 01 repository expansion or only core/care implementation.
5. Define required artifacts and pass/fail criteria.
6. Do not install toolchains, create product code, or choose a winner during this correction cycle.

### 3.6 Tighten SQLite eligibility

Current issue:

- The packet correctly identifies the WAL-reset corruption bug.
- The expression `3.51.3+` is too broad: SQLite 3.52.0 was later withdrawn for compatibility issues.

Required correction:

1. Require one exact, currently supported, non-withdrawn SQLite release or one specifically documented fixed backport.
2. Record source ID/digest, binding, compile options, filesystem, connection/writer/checkpoint topology, backup API, vulnerabilities, and compatibility status.
3. Do not treat every numeric version greater than or equal to 3.51.3 as automatically eligible.
4. Keep SQLite conditional until crash/checkpoint/disk-full/migration/backup/restore tests pass.

Controlling primary sources:

- https://www.sqlite.org/wal.html
- https://sqlite.org/news.html

At review time, official SQLite news lists 3.53.0 as a fixed major release and documents the withdrawal of 3.52.0. This does not preselect 3.53.0; it invalidates a loose minimum-version rule.

### 3.7 Label and diversify slice evidence floors

Current issue:

- `100` replay/restart runs, `1,000` interaction cycles, and `30` minutes are useful provisional engineering floors.
- They are not evidence of statistical product reliability or long-duration safety performance.

Required correction:

1. Label them as provisional minimum engineering evidence floors.
2. Explain what each floor is intended to detect and what it cannot establish.
3. Use multiple deterministic seeds, durable-boundary kill points, schema variations, and state-boundary cases rather than repeating only one sequence.
4. Add property/randomized testing where reproducible seeds are retained.
5. Define escalation to 24-hour, multi-day, accessibility, media, shadow-safety, pilot, and operational evidence in later gates.

## 4. Correction scope

Continue the existing directive. Do not repeat the accepted full ingest or rewrite correct sections without need.

Update only the affected files among:

- `RECOMMENDED_ARCHITECTURE.md`
- `PROCESS_PRIVILEGE_DATA_BOUNDARIES.md`
- `VERTICAL_SLICE_CONTRACT.md`
- `DEPENDENCY_AND_RIGHTS_MATRIX.md`
- `RESOURCE_EXPERIMENT_PLAN.md`
- `THREAT_PRIVACY_CLAIMS_MODEL.md`
- `REPOSITORY_CI_TEST_RELEASE_PLAN.md`
- `DECISION_TRACEABILITY.md`
- `EVIDENCE.md`
- `HANDOFF.md`
- `PLAN.md`
- mutable `.agent` current routing/state records
- append-only directive/outcome/learning records through new superseding entries only
- the dedicated Notion coder report and parent directive
- GitHub Issue #3

Preserve prior results and failed/review history. Do not rewrite this Architect review.

## 5. Correction acceptance criteria

1. Safety candidates reach and are durably received by `care-core` without `companion-core` availability, approval, or forwarding.
2. Companion state, output, models, memory, mood, and dreams cannot fabricate, suppress, or authorize a care transition.
3. One explicit vault authority owns consent, contacts, biometric handles, credentials, and key references, with absent/locked/degraded behavior.
4. Canonical event serialization, numeric representation, content hashing, boot epoch, and cross-reboot ordering are unambiguous and versioned.
5. Phase 01 foundation acceptance is separate from the cross-phase vertical-slice milestone.
6. A language/toolchain experiment exists with explicit blocking status and no premature winner.
7. SQLite eligibility requires an exact supported non-withdrawn build, not a loose minimum-version expression.
8. Provisional evidence counts are labeled, diversified across seeds and failure boundaries, and not represented as reliability claims.
9. All affected threat, degradation, test, experiment, traceability, evidence, and handoff statements agree.
10. Notion, Issue #3, task packet, result commits, and remote `main` agree after publication.
11. No product code, Godot execution, assets, dependencies, manifests, CI workflow, benchmark, media capture, biometric implementation, notification integration, safety runtime, phase transition, architecture self-approval, or product-capability claim is introduced.

## 6. Required handoff

Publish one focused correction commit and, only if necessary, one publication-reconciliation commit. Return the canonical `CODEX RESULT` with exact changed files, validation, external-source changes, unresolved items, result SHAs, clean-tree/remote equality, Issue #3 state, Notion publication result, and explicit confirmation that Architecture v1.0, Roadmap Phase 01, dependency approval, and product implementation remain pending Architect authority.

## 7. Disposition

- Context reconstruction: `ACCEPTED`.
- Topology direction: `PROVISIONALLY ACCEPTED`.
- Current Architecture v1.0 package: `NOT ADOPTED`.
- Directive: `CONTINUED`.
- Issue #3: `REMAINS OPEN`.
- Roadmap Phase 01: `CLOSED`.
- Product implementation: `CLOSED`.
