# COMPANION-P00-INGEST-001 — Evidence Record

## Repository preflight

- Repository root: `/srv/ATLAS/100_ACTIVE/Projects/COMPANION` — `PASSED`.
- Branch: `main`.
- Starting local HEAD: `0fbedc441cb8ea2b098a32b46d00ce2415c65f07`.
- Published directive HEAD after `git fetch --prune origin` and `git merge --ff-only origin/main`: `bb879150f66e4c19bc4058967c628070087d553e`.
- Directive planning baseline relationship: `9056c0362a43f2b635ffb910451943b59e4ee1f0` is the parent of `bb879150...`; original local HEAD was an ancestor. `PASSED`.
- Remote: `git@github.com:SketchOTP/companion.git`; GitHub repository `SketchOTP/companion`, default branch `main`.
- Working-tree state before work: clean after the authorized fast-forward. `PASSED`.
- Applicable `AGENTS.md` files: root `AGENTS.md` only; no nested router found. `PASSED`.
- Authority startup: root router, Authority skill, `.agent/INDEX.md`, mandatory kernel, task packet, result/evidence/state/directive/safety references all read. `PASSED`.
- Repository history: six commits from `b7266b5` through `bb87915`; full committed tree inspected. `PASSED`.
- GitHub state: Issue #1 open; no open pull request; no workflow run on directive SHA; no tags; only `main` observed at directive SHA. `PASSED`.
- Preservation of unfamiliar work: no unexplained dirty work existed; no history rewrite, deletion, force push, or product file change performed. `PASSED`.

## Notion traversal evidence

- Retrieval start: `2026-09-08T19:40:23Z`.
- Retrieval end: `2026-09-08T20:29:51Z`.
- Named authority pages expected/fetched: `18 / 18` — `PASSED`.
- Named corpus: canonical project, end goal, roadmap, governance, Research Phase 01, R01–R10, Visual Bible, Open Decisions, and Risk Register.
- Workflow pages fetched: canonical directive and dedicated coder report.
- Additional material authorities discovered/fetched: `1 / 1` — the explicitly superseded duplicate directive, retained as audit history.
- Material authorities fetched including schemas/rows/workflow/additional/assets: `101` manifest records.
- Pages/rows with truncated output: `0`.
- Pages/rows with unknown blocks: `0`.
- Broken/inaccessible mandatory links or attachments: `0`.
- Ancestor disposition: “Animus Machinae” is a parent container, not a COMPANION child authority; it is not counted as project material.
- Retrieval tooling/query log:
  - Notion connection and search capability verified.
  - Each named page was fetched by canonical page URL.
  - Canonical descendant search was run with page size 50; direct link-graph traversal supplied completeness because row pages dominate descendant search.
  - Both data-source schemas were fetched, then queried in row mode with limit 100 and `has_more=false`.
  - All 76 returned row URLs were fetched individually; no row fetch errored or truncated.
  - Every authority link extracted from the fetched corpus was reconciled to a fetched page, database, row, workflow/audit page, visual reference, or the out-of-scope ancestor container.

## Database evidence

### Architecture Decision Ledger

- Live row count: `32`.
- Unique stable IDs/titles/URLs: `32 / 32 / 32`; contiguous `ADR-01`–`ADR-32`.
- Status totals: `16 Adopted / 14 Interim / 2 Rejected`.
- Type totals: `12 Architecture Ruling / 7 Operator Ruling / 2 Build vs Adopt / 9 Constraint / 2 Hypothesis`.
- Missing/duplicate rows: `0 / 0`.
- Query/retrieval evidence: data-source row query returned 32 rows with `has_more=false`; every row page and all decision properties were fetched. ADR-28's nonblank body approval evidence was also read.

### Research Evidence Register

- Live row count: `44`.
- Unique stable IDs/titles/URLs: `44 / 44 / 44`; contiguous `SRC-01`–`SRC-44`.
- Evidence grades: `31 A / 11 B / 2 C`.
- Review statuses: `31 Reviewed / 12 Candidate / 1 Needs Deep Review`.
- Source types: `26 Official Guidance / 10 Peer-reviewed / 3 Preprint / 5 Official Repository`.
- Missing/duplicate rows: `0 / 0`.
- Finding, implication, limitation, license note, and recheck trigger fields reviewed: `PASSED — 44 / 44`.
- Query/retrieval evidence: data-source row query returned 44 rows with `has_more=false`; every row page and all required properties were fetched.

## Visual inspection evidence

- Identity master direct inspection: `PASSED` — purple compact creature, edge-spiked flame head, black eye fields, white pupils, small mouth, flat cel shading.
- Identity canonical native marker: `SHA-256 86ce1f9428f9a998d57e1a99c4245347d5a05e9f0bcf853c2b68065f351bdb56`, `1254×1254 RGBA`.
- Identity derivative marker: `SHA-256 a242d3f493db7c70e766ce64259850c3961e4e1cdbbfae015fc85611324af6f9`.
- Six-view turnaround direct inspection: `PASSED` — front/back/left/right/top/bottom directional identity sheet.
- Turnaround canonical native marker: `SHA-256 3696c7d63594de38d408438d5b882f3207635bc63e59fb270f624715faeb09e4`, `1448×1086 RGB`.
- Turnaround derivative/embedded-preview markers: `SHA-256 ac760dfc80a6cba867ba1e34fc8013c4ae6e979086b8f8fa158132412b8057cc` and `e9fc7793bd326db090425b8765fbff8930c732f6c0bb5b7d1104aae76134c8e5`.
- Temporary render files remained outside the repository in `/tmp`; no asset was introduced.
- Final authority re-read: `PASSED` — corrected a draft transcription before Notion publication; the canonical anatomy is exactly two fingers plus one thumb per hand and exactly three toes per foot.

## Artifact validation

| Check | Result | Evidence/details |
|---|---|---|
| `INGEST_MANIFEST.json` parses | PASSED | `jq -e`; 101 records |
| Stable record identifiers are unique | PASSED | 101 unique of 101 |
| Mandatory authority coverage | PASSED | 96/96 mandatory records plus five workflow/audit/visual records |
| Live counts reconciled | PASSED | 18 pages, 2 databases, 32 ADRs, 44 evidence rows |
| Reproducibility marker coverage | PASSED | 101/101 records |
| Every comprehension section completed | PASSED | Sections 1–16 present; no pending placeholder |
| Every self-test answered | PASSED | A–L present and answered |
| All end-goal pillars traced | PASSED | 10/10 |
| Roadmap Phase 00–15 traced | PASSED | 16/16 |
| Contradiction classifications completed | PASSED | 10 findings; no true conflict |
| No product files/dependencies/assets/CI added | PASSED | changed paths are task/state Markdown/JSON only |
| `git diff --check` | PASSED | clean |
| Narrow secret scan | PASSED | no private-key, provider-token, credential-assignment, or common API-secret pattern in the diff |
| Changed-file scope inspection | PASSED | 13 paths, all under `.agent/` |
| Notion report update and re-fetch | PASSED | complete counts, ADEQUATE confidence, summary, open decisions, result SHA, E2, and boundary verified; no truncation/unknown blocks |
| Directive status update and re-fetch | PASSED | Codex-complete/Architect-review-pending status and result SHA verified; issue remains open |
| Canonical project synchronization and re-fetch | PASSED | result SHA, pending review, governance-only boundary, and closed product gate verified |
| Normal commit/push | PASSED | result artifacts and anatomy correction normally pushed through `7ea6985ab278439e1903ba0ede0b1deaf71af6c8` |
| Local/remote exact-SHA equality | PASSED | `HEAD == origin/main == 7ea6985ab278439e1903ba0ede0b1deaf71af6c8` after result push; repeated after publication-evidence commit |

## Retrieval confidence

- Classification: `ADEQUATE`.
- Justification: every mandatory authority and both database schemas were retrieved live; all 76 live rows were enumerated and individually fetched; both visual references were directly inspected; the GitHub/repository surface was reconstructed; counts, links, markers, required properties, and contradictions were reconciled with no missing or truncated mandatory record.
- Blocking gaps: `NONE`.

## Evidence level

- Achieved level: `E2_REPRODUCED` for live corpus coverage and the completed comprehension/traceability artifacts.
- Justification: issue-time counts and stated authority were independently re-queried and reproduced from live page/database/repository evidence. No target product behavior was created or tested.
- Product-capability evidence: `NOT APPLICABLE`.

## Final scope review

- Product implementation introduced: `NO`.
- Dependency/model/data/voice/asset introduced: `NO`.
- Strategic project decision changed: `NO`.
- Unrelated work changed: `NO`.
- Historical evidence rewritten: `NO`; current-state mirrors were updated and append-only ledgers received new entries.
- Final diff reviewed: `PASSED`; only governance/current-state and task-packet records changed.

## Architect Review 01 supersession

- Review-state baseline: `f4a312b29fd8cc07a330242a1f1d6afaf8cd3858`.
- Architect verdict: `CONTINUE — CORRECTIONS REQUIRED`; acceptance remains `NOT GRANTED`.
- Provisionally retained: corpus enumeration, counts, repository scope/hygiene, visual hashes/dimensions, and corrected anatomy.
- Superseded first-submission claims: comprehension section 15, ADR traceability, risk traceability, contradiction C-01/C-08 interpretation, and the structural-only `PASSED` claims for those areas.
- Preservation: the prior commits and evidence above remain historical; this section records the focused correction rather than rewriting the failed result.

## Correction cycle 1 — focused source retrieval

- Focused retrieval completed: `2026-09-09T00:46:18Z`.
- Open Decisions page: `PASSED` — fetched live; 14 queue rows total, comprising 3 resolved and exactly 11 open/partial records; no returned truncation or unknown block.
- Architecture Decision Ledger: `PASSED` — schema fetched; row-mode query with limit 100 returned 32 rows and `has_more=false`; 32 unique exact ID/title/status triples; 16 Adopted, 14 Interim, 2 Rejected.
- Initial Risk Register: `PASSED` — fetched live; 14 exact ID/title rows; no returned truncation or unknown block.
- Architect review, coder report, and active directive: `PASSED` — fetched at review-state head before correction.
- Full re-ingest: `NOT RUN / NOT REQUIRED` — Architect provisionally accepted corpus coverage and no focused source change required unrelated retrieval.
- `INGEST_MANIFEST.json`: `UNCHANGED` — the accepted 101-record corpus evidence remains intact; the focused semantic source crosswalk is recorded separately.

## Correction cycle 1 — semantic validation

Machine-readable evidence: `SEMANTIC_VALIDATION.json`.

Validation method:

1. Normalize the live ADR query to `ADR-NN — exact title — exact status`.
2. Parse the live Open Decisions and Initial Risk Register tables into exact ID/title pairs and derive the explicit open/partial status from each RQ row.
3. Compare all 11 required RQ pairs against `COMPREHENSION.md` and the machine-readable crosswalk.
4. Compare every ADR cited by `TRACEABILITY.md` against the live 32-row ledger and require its exact title/status at first use.
5. Compare every risk cited by `TRACEABILITY.md` against the live 14-risk register and require its exact title at first use.
6. Enforce reference closure: every ADR/risk token in traceability must exist in the semantic crosswalk and every crosswalk entry must be cited.
7. Check each of the ten end-goal pillar rows for its manually reviewed, substantively relevant ADR/risk set; numeric proximity is never evidence of relevance.

Results:

| Semantic check | Result | Exact outcome |
|---|---|---|
| Live RQ table parsed | PASSED | 14 rows; 11 open/partial target rows |
| RQ ID/title/status/consequence | PASSED | 11/11 exact; RQ-12 product name and RQ-14 screen habitat restored |
| Live ADR query parsed | PASSED | 32 rows; 25 cited decisions checked |
| ADR ID/title/status at first use | PASSED | 25/25 exact |
| ADR reference closure | PASSED | 25 traceability IDs = 25 semantic-map IDs |
| Live risk table parsed | PASSED | 14 rows; 13 cited risks checked |
| Risk ID/title at first use | PASSED | 13/13 exact |
| Risk reference closure | PASSED | 13 traceability IDs = 13 semantic-map IDs |
| Ten pillar relationship sets | PASSED | 10/10 rows contain the reviewed ADR/risk relationships |
| Required primary risk relationships | PASSED | Caregiving RISK-01/02; privacy RISK-03/04; memory RISK-05; continuity RISK-08; development RISK-11 |
| Unsupported substitute RQ meanings | PASSED | none found |
| Semantic validator errors | PASSED | 0 |

Validator execution note: two draft harness invocations were discarded before evidence classification. The first parsed the connector's outer JSON envelope instead of its embedded page text and therefore found zero RQ/risk rows; the corrected parser unwrapped the page text and reproduced `11 / 32 / 14` live RQ/ADR/risk counts with zero comparison errors. A later shell closure check mistakenly allowed Markdown backticks to be interpreted by the shell; its output was not accepted. The corrected fixed-string rerun exited zero and produced the results above. Neither harness defect changed a source or project artifact.

## Correction-cycle evidence level

- Corrected semantic artifacts: `E3_TARGET_TESTED`.
- Retained corpus coverage: `E2_REPRODUCED`.
- Product-capability evidence: `NOT APPLICABLE`.
- Retrieval confidence: `ADEQUATE`.
- Architect acceptance: `NOT RUN` for the corrected submission.
