# Evidence Record

Status: `ARCHITECT REVIEW 01 CORRECTED — RESUBMISSION PENDING PUBLICATION`

## Authority reconstruction

- Repository root and only applicable router: `/srv/ATLAS/100_ACTIVE/Projects/COMPANION/AGENTS.md`.
- Starting and routing head: `6559cec1beaf27bf958c2b9517b0717f04c83ea9`; initially equal to `origin/main`; tree clean.
- Full directive, bridge, Authority skill/references, current-state kernel, all active packet files, archived environment packet, repository history/tree, and Issue #3 plus all three comments: `PASSED`.
- Required Notion pages R01–R10, canonical project, operational end goal, roadmap, governance, research master, operator decision packet, open queue, risk register, visual bible, environment directive/report/review, active directive/full directive/report: `PASSED`; no truncation or unknown blocks.
- Direct visual inspection: identity master and six-view turnaround `PASSED`; recorded hashes/dimensions/anatomy match authority.
- ADR ledger: `37` unique rows, `21 Adopted / 14 Interim / 2 Rejected`, `has_more=false`.
- Evidence register: `46` unique rows, `33 A / 11 B / 2 C`; `33 Reviewed / 12 Candidate / 1 Needs Deep Review`, `has_more=false`.
- Retrieval confidence: `ADEQUATE`. Material contradictions: `NONE`.

## Primary-source research

Current official/primary sources were retrieved on 2026-09-09 for JSON Schema 2020-12, XDG Base Directory 0.8, SQLite WAL and Backup API, systemd service/exec/socket behavior, NIST SSDF/AI RMF/Privacy Framework, Kentucky AG KCDPA guidance, FTC HBNR guidance, FDA digital-health intended-use guidance, Godot 4.7 Window/license, CycloneDX 1.7, SPDX 3.0.1, and SLSA 1.2. Exact links and their recommendation mapping are in `DECISION_TRACEABILITY.md`.

Important current finding: SQLite's official WAL page states that a rare WAL-reset corruption bug affects 3.7.0 through 3.51.2, with the fix in 3.51.3 and documented fixed backports. The SQLite shortlist therefore requires exact embedded-version and concurrency/checkpoint/crash qualification.

## License and dependency evidence

- Repository license: Apache-2.0 observed and unchanged.
- Godot engine: official MIT license, but exact 4.7.2 artifact/bundled notices remain unverified.
- SQLite source: public-domain project claim; bindings/builds/compile options remain separate.
- Every model/weight/data/voice/asset/plugin/service is separately dispositioned; no repository license is treated as rights for associated artifacts.
- InsightFace supplied pretrained artifacts remain rejected for this consumer path absent exact commercial rights.
- No dependency, manifest, model, data, voice, service, or asset was installed, downloaded, generated, or approved.

## Alternatives and decisions

- Compared cohesive transactional core with isolated edges versus fully decomposed local services.
- Recommended the cohesive core because it maintains required safety/device/model/renderer isolation while avoiding distributed mutation/reconciliation risk.
- Rejected Godot-monolith, LLM-creature, whole-organism behavior-tree/RL, cloud canonical owner, and shared multiwriter database using exact ADR/risk relationships.
- No ADR or RQ was adopted/resolved by Codex.

## Changed paths

Only planning/evidence/state paths under `.agent/` are changed. Preserved unchanged: `CODEX_FULL_DIRECTIVE.md`, `AUTHORITY_CONTEXT_BRIDGE.md`, root `AGENTS.md`, `.agents/`, `.authority/`, `LICENSE`, and `.gitignore`.

Task artifacts completed:

- `AUTHORITY_CONTEXT_ACKNOWLEDGMENT.md`
- `PLAN.md`
- `ARCHITECTURE_OPTIONS.md`
- `RECOMMENDED_ARCHITECTURE.md`
- `PROCESS_PRIVILEGE_DATA_BOUNDARIES.md`
- `VERTICAL_SLICE_CONTRACT.md`
- `RESOURCE_EXPERIMENT_PLAN.md`
- `THREAT_PRIVACY_CLAIMS_MODEL.md`
- `DEPENDENCY_AND_RIGHTS_MATRIX.md`
- `REPOSITORY_CI_TEST_RELEASE_PLAN.md`
- `PRODUCT_CONTRACT_DISPOSITIONS.md`
- `DECISION_TRACEABILITY.md`
- `EVIDENCE.md`
- `HANDOFF.md`

Project state/append-only records updated: `.agent/CURRENT.md`, `.agent/DIRECTIVES.md`, `.agent/OUTCOMES.md`, `.agent/EXTERNAL.md`, and `.agent/LEARNINGS.md`.

## Validation

Validation is semantic as well as structural:

- exact live ADR ID/title/status and substantive relationship review;
- exact RQ title/status/disposition review;
- exact risk title and control relevance review;
- 10/10 end-goal pillar and 16/16 roadmap-phase coverage;
- one canonical writer per state/authority class and acyclic authority review;
- interface/privacy/SSHFS/network/rights/claims/scope review;
- full changed-tree and diff review;
- placeholder, prohibited-path, secret/private-identifier, and implementation-leakage scans;
- `git diff --check` and final local/remote synchronization.

Exact command results and publication markers are recorded in the publication addendum below.

## Evidence level and limits

- Authority/corpus reconstruction: `E2_REPRODUCED`.
- Planning crosswalk and target semantic validation: `E3_TARGET_TESTED` for documentation/architecture traceability only.
- Runtime/product evidence: `NOT APPLICABLE / NOT CREATED`.
- Architecture acceptance: `NOT RUN — ARCHITECT AUTHORITY`.
- Product capability, Phase 01, dependency approval, and release readiness: `NOT ESTABLISHED`.

## Publication addendum

- Coherent planning result commit: `5d6d87d93b017e42647e260b69d80b5ad3f8becc` — `docs: propose companion architecture v1.0`.
- Normal fast-forward from `6559cec1beaf27bf958c2b9517b0717f04c83ea9`: `PASSED`.
- Planning result push to `origin/main`: `PASSED`.
- Dedicated Notion coder report replaced with the complete proposal and exact result SHA: `PASSED`; re-fetched at `2026-09-09T14:28:33.690Z`; no pending-execution marker or truncation/unknown-block flag returned.
- Parent Notion directive status changed to `CODEX RESULT SUBMITTED — ARCHITECT REVIEW PENDING`, exact result section appended, and page re-fetched: `PASSED` at `2026-09-09T14:29:08.208Z`.
- GitHub Issue #3 result comment: `PASSED`, comment `5603553996`; exact result SHA re-fetched in comment body.
- GitHub Issue #3 final state: `OPEN`, four comments at `2026-09-09T14:29:36Z`; Codex did not close or self-accept.
- Mutable authority re-fetch immediately before publication: `PASSED`; canonical/roadmap/open/risk/directive/report states unchanged, 37 ADRs and 46 evidence rows returned with `has_more=false`.

### Final validation commands

- Changed paths outside `.agent/`: `PASSED — 0`.
- Preserved `CODEX_FULL_DIRECTIVE.md` and `AUTHORITY_CONTEXT_BRIDGE.md`: `PASSED — 0 diff lines`.
- Required active packet files: `PASSED — 17 present`.
- Output pending/placeholder markers: `PASSED — 0`.
- Exact end-goal pillar coverage: `PASSED — 10/10`.
- Exact roadmap phase coverage: `PASSED — Phase 00–15, 16/16`.
- Remaining RQ disposition coverage: `PASSED — 7/7`.
- Risk coverage: `PASSED — RISK-01 through RISK-14, 14/14`.
- Product/manifests/workflows forbidden-path check: `PASSED — 0`.
- Narrow secret/private-identifier scan of changed content: `PASSED — 0`.
- One-writer/authority-cycle and relationship-relevance review: `PASSED — manual semantic review`.
- `git diff --check` and staged `git diff --cached --check`: `PASSED`.
- Product/runtime tests, Godot tests, benchmarks, media tests, safety/notification tests: `NOT APPLICABLE / NOT RUN` because prohibited by this planning directive.

The publication-only reconciliation commit containing this addendum is reported in the canonical handoff after it is created; a commit cannot contain its own SHA.

## Architect Review 01 correction evidence

The original result and publication evidence above remain historical. Architect Review 01 at `c36525ae5e1bb478baf679cacc1a5f2fd22020c8` continued the directive and superseded prior pass claims for seven semantic areas. Accepted context reconstruction and topology were retained.

### Fresh authority/state retrieval

- Local clean `main` at `d8c7209e0ec0370c17fc4cf980fde879e54f10b5` and remote head `c36525ae5e1bb478baf679cacc1a5f2fd22020c8`: `PASSED`.
- Incoming history: one normal fast-forward commit changing only `.agent/CURRENT.md`, `.agent/INDEX.md`, and `ARCHITECT_REVIEW_01.md`: `PASSED`.
- Required repository review/current/index/kernel and affected artifacts: `PASSED`.
- Live Notion Architect review, parent directive, coder report, canonical project, and roadmap: `PASSED`; all agree the directive is continued, Architecture v1.0 is not adopted, Phase 01/product work are closed, and the retained corpus is 37 ADRs/46 evidence records.
- GitHub Issue #3 and six comments: `PASSED`; state `OPEN`, Architect continuation comment `5604351972` present.
- Full corpus re-ingest: `NOT RUN / NOT REQUIRED` because the Architect accepted it and no live authority change requiring repetition was found.
- Retrieval confidence: `ADEQUATE`; material authority contradiction: `NONE`.

### Refreshed primary sources

- RFC 8785: invariant JCS output, I-JSON constraint, duplicate-key prohibition, Unicode preservation without normalization, IEEE-754 input boundary, rejection of NaN/Infinity, deterministic property ordering, and UTF-8 generation: `PASSED`.
- systemd journal time semantics: monotonic time begins anew each boot and needs a boot identifier for well-defined cross-record use: `PASSED`.
- SQLite WAL: current page still records the WAL-reset affected range/fixed releases/backports and one-host/network-filesystem limits: `PASSED`.
- SQLite news: 3.52.0 withdrawal and 3.53-series releases reproduced; this disproves a generic `3.51.3+` eligibility expression but does not preselect a build: `PASSED`.
- Official Python 3.12, Rust, and Go documentation entry points: `PASSED`; used only to define the EXP-00 candidate boundary, not to select a winner or claim host fit.

### Corrected architecture assertions

- Direct safety ingress: authorized producer sends a safety candidate directly to care; companion cannot forward, gate, suppress, modify, or authorize it; care owns immutable receipts and incidents.
- Authority independence: common source ID/digest/provenance can link ordinary and safety messages without shared storage or mutation. Care starts/processes/replays without the companion store.
- Vault: one explicit owner for consent/revocation, biometric handles/templates, contacts/roles, provider credential handles, key references/recovery metadata, and privileged audit; foreign processes receive only decisions/opaque capabilities.
- Canonical events: `JCS-RFC8785-v1`, `sha-256-jcs-event-v1`, complete digest/signature scope, duplicate-key/Unicode/numeric rules, fixed-point/wide-integer representation, boot-scoped monotonic time, UTC uncertainty, owner sequence, and causation are specified.
- Phase semantics: Phase 01 foundation is distinct from a later Phase 02/03/04/10 milestone; milestone success completes no roadmap phase.
- Toolchain: EXP-00 compares Python 3.12 with exactly one Architect-selected compiled comparator from Rust or Go; no installation, code, benchmark, or winner exists. It blocks authoritative-service implementation, not all language-neutral Phase 01 foundation work.
- SQLite: eligibility is one exact supported non-withdrawn release or documented fixed backport with a complete build/topology/security record and crash/concurrency/checkpoint/disk/backup/restore/migration tests.
- Evidence floors: 100 replay/restart cases, 1,000 cycles, and 30 minutes are provisional minimum engineering floors with diversified seeds/states/schemas/kill points/boots; none is reliability, safety, endurance, capacity, or SLA evidence.

### Correction validation scope

- Safety-path cross-artifact consistency and five required direct-ingress/forgery/idempotency/outage/DB-independence tests specified: `PASSED`.
- Companion mood/memory/language/model/dream/animation suppression or transition authority excluded and negative-tested: `PASSED`.
- Vault ownership/interface plus absent/locked/corrupt/unavailable/revoked behavior across architecture, boundaries, threat, milestone, dependency, test, and traceability: `PASSED`.
- Canonicalization/digest/numeric/time fields and rejection/replay fixtures across architecture, milestone, repository-test plan, and traceability: `PASSED`.
- Phase 01 versus cross-phase milestone separation and exact Phase 02/03/04/10 contributions: `PASSED`.
- EXP-00 evaluation dimensions/blocking boundary/no-winner constraint: `PASSED`.
- No loose SQLite minimum remains in operative recommendations; historical review text is preserved: `PASSED`.
- Provisional-floor label, intended-detection/limitation table, diversified cases, and later escalation: `PASSED`.
- Product/runtime tests, Godot execution, toolchain/database benchmarks, media, biometrics, notification, and safety runtime: `NOT APPLICABLE / NOT RUN — PROHIBITED`.

The correction artifact evidence is `E3_TARGET_TESTED` for documentation semantics and cross-document consistency only. It establishes no runtime or product capability and does not constitute Architect acceptance.
