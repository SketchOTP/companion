# COMPANION-P00-INGEST-001 — Contradictions, Stale Records, and Retrieval Gaps

## Classification rules

- **TRUE CONFLICT:** two current authorities prescribe incompatible project truth and the authority order does not resolve it safely.
- **STALE SNAPSHOT:** an older summary differs from a later authoritative decision or verified repository fact.
- **UNRESOLVED DECISION:** Notion explicitly leaves the choice open; this is not an inconsistency and must not be guessed.
- **HARMLESS WORDING DIFFERENCE:** wording differs while meaning and authority remain aligned.
- **BROKEN REFERENCE:** a link, page, row, attachment, or repository pointer cannot be resolved.
- **INACCESSIBLE/TRUNCATED EVIDENCE:** a source could not be fully retrieved or contained unresolved unknown blocks.
- **COUNT/ENUMERATION MISMATCH:** live records differ from expected counts or cannot be uniquely enumerated.

## Findings

| ID | Classification | Sources compared | Exact mismatch | Authority resolution | Action taken | Architect/operator action required |
|---|---|---|---|---|---|---|
| C-01 | STALE SNAPSHOT | R10 current-art-state text vs Visual Bible and ADR-29 | R10 says a canonical eight-view turnaround remains before scaling; later approved authority establishes a six-view turnaround and deliberately leaves four three-quarter references/detailed construction open | Later operator-approved Visual Bible and ADR-29 govern | Recorded; did not rewrite research history | None for ingest; RQ-14 remains a later art-planning choice |
| C-02 | STALE SNAPSHOT | R10/ADR-25 review wording vs Visual Bible and ADR-28/29 | Older review language says art style still requires selection; flat cel-shaded style is now approved. Screen habitat remains open | Later operator rulings narrow the unresolved set | Recorded without altering the historical ADR | None; habitat still needs an operator decision |
| C-03 | STALE SNAPSHOT / NARROW SUPERSESSION | ADR-18 vs Governance, ADR-30, and repository history | ADR-18 rejects initializing a production repository before research exit; a later ruling authorizes and accepts a governance-only repository | The later ruling is narrower and does not authorize production implementation | Preserved both records; documented the boundary | None |
| C-04 | HARMLESS WORDING DIFFERENCE | ADR-21 vs ADR-22/R09 | ADR-21 names a desktop Linux research host generally; ADR-22 selects the user's existing Linux PC and connected peripherals specifically | Later decision refines, rather than contradicts, the interim host class | Recorded; no change | None |
| C-05 | STALE SNAPSHOT | ADR-30 rationale vs accepted repository history | ADR-30 names `5cba889` as the reviewed bootstrap; `0fbedc4` was subsequently accepted as the count reconciliation before planning/directive commits | Git history and later accepted outcome supply current repository truth | Recorded; historical decision retained | None |
| C-06 | STALE SNAPSHOT | Research Phase 01 repository-status row and Governance expansion note vs GitHub `main` | Those snapshots stop at `9056c036...`; the published directive commit is `bb879150...` | GitHub/live Git governs versioned repository fact | Recorded; current `.agent` state reflects directive commit | None |
| C-07 | STALE SNAPSHOT | `.agent/PROJECT_PROFILE.md` vs Canonical, Roadmap, `.agent/INDEX.md`, and `.agent/CURRENT.md` | Profile says “Current phase: Research Phase 01”; current strategic phase is Planning Phase 02 / Roadmap Phase 00 | Current Notion status and later repository state are unambiguous | Corrected the repository mirror to Planning Phase 02 / Roadmap Phase 00 | None |
| C-08 | UNRESOLVED DECISION | Open Decisions page vs future roadmap dependencies | RQ-02/03/04/05/07/08/09/10/11/14 remain open and RQ-12 remains partial | The queue intentionally reserves these decisions; no inference is permitted | Enumerated them in comprehension/traceability | Operator/Architect must resolve them through later directives when required |
| C-09 | HARMLESS WORDING DIFFERENCE | Duplicate directive page vs canonical directive/GitHub Issue #1 | A concurrent, less-complete directive page exists | It is explicitly titled and marked superseded and routes to the canonical directive | Fetched and retained as one additional audit authority | None |
| C-10 | HARMLESS WORDING DIFFERENCE | Canonical descendant search vs link-graph traversal | The ancestor page “Animus Machinae” appears in paths but is not a COMPANION child authority | Ancestor container is outside the project child-authority corpus | Excluded from material child count; all project links traversed | None |

## Explicit checks

- Canonical project versus end goal: `PASSED` — canonical summary and ten operational pillars align.
- Canonical project versus roadmap: `PASSED` — Planning Phase 02 and Roadmap Phase 00 gates align.
- Canonical project versus research foundation: `PASSED` — R01–R10 support the end goal; later rulings refine older research snapshots.
- Canonical project versus governance contract: `PASSED` — authority, evidence, and implementation prohibitions align.
- Canonical project versus open-decision queue: `PASSED` — no open item was silently resolved.
- Canonical project versus Architecture Decision Ledger: `PASSED` — 32 rows uniquely enumerated and reconciled.
- Canonical project versus visual bible and sprite contract: `PASSED WITH STALE SNAPSHOTS` — later six-view/style rulings resolve older wording.
- Canonical project versus current GitHub HEAD: `PASSED` — published directive commit was present and cleanly fast-forwarded.
- Notion current phase versus `.agent/INDEX.md`: `PASSED`.
- Notion current phase versus `.agent/PROJECT_PROFILE.md`: `FAILED BEFORE CORRECTION; PASSED AFTER CORRECTION`.
- Notion current phase versus `.agent/CURRENT.md`: `PASSED`.
- Repository implementation boundary versus committed tree: `PASSED` — governance only.
- Expected versus live decision count: `PASSED` — 32 expected, 32 live.
- Expected versus live evidence count: `PASSED` — 44 expected, 44 live.
- Named links and discovered child authorities: `PASSED` — all 18 named pages, two databases, workflow pages, and one superseded audit page fetched.
- Attached visual references and asset metadata: `PASSED` — both references directly inspected and native/derivative SHA-256 markers recorded.

## Resolution summary

No true conflict blocks certification. Six historical/current-state wording issues were classified under their later unambiguous authorities; only the stale repository phase mirror was corrected because it is current-state metadata and the directive authorizes reconciliation. Open/partial RQ items remain operator decisions. There are no broken references, incomplete database enumerations, inaccessible mandatory authorities, truncated results, or unknown blocks. Retrieval confidence is therefore `ADEQUATE`.
