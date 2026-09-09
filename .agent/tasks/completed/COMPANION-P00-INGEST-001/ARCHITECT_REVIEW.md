# COMPANION-P00-INGEST-001 — Architect Review 01

## Verdict

`CONTINUE — CORRECTIONS REQUIRED`

- Reviewed through: `fce544262f164e4da1508879ec9d8865b0cecfa2`
- Reviewed result range: `bb879150f66e4c19bc4058967c628070087d553e..fce544262f164e4da1508879ec9d8865b0cecfa2`
- Architect acceptance: `NOT GRANTED`
- Product implementation authorization: `CLOSED`
- Canonical review record: https://app.notion.com/p/3d5833cb27ff819b9433f230c7bc06ad

## Review performed

The Architect independently inspected:

- the three submitted commits and full compare range;
- the final committed tree and changed-file scope;
- `INGEST_MANIFEST.json`, `COMPREHENSION.md`, `TRACEABILITY.md`, `CONTRADICTIONS.md`, `EVIDENCE.md`, `PLAN.md`, and `HANDOFF.md`;
- the dedicated Notion coder report and directive status;
- the live Open Decisions page;
- all 32 live Architecture Decision Ledger rows through a fresh Notion query;
- the live Research Evidence Register aggregate through a fresh Notion query;
- the Initial Risk Register;
- GitHub Issue #1 and current `main`.

## Accepted portions

- The three commits are a normal fast-forward from the directive commit.
- The final tree remains governance-only. No product source, Godot project, sprite asset, dependency, CI, deployment, model, dataset, voice, database implementation, experiment, notification, or safety integration was introduced.
- Independent Notion queries reproduce 32 unique architecture decisions and 44 unique research-evidence records.
- The evidence distribution independently reproduces as 31 Grade A, 11 Grade B, 2 Grade C; 31 Reviewed, 12 Candidate, and 1 Needs Deep Review.
- The approved visual source hashes and dimensions match the recorded evidence.
- The correction commit accurately restores the canonical hand/foot anatomy: two fingers plus one thumb on each hand and three toes on each foot.
- Corpus enumeration is provisionally accepted. A full re-ingest is not required unless a canonical source changes during correction.

## Material findings

### F-01 — Open-decision comprehension is incorrect

`COMPREHENSION.md` section 15 assigns the wrong meaning to most live RQ identifiers and introduces unsupported statements.

The canonical queue is:

- `RQ-02 — First user population and household model` — open.
- `RQ-03 — Intended product use and commercialization path` — open.
- `RQ-04 — Offline, cloud, compute, power, noise, and cost boundary` — open.
- `RQ-05 — First caregiving scenario and escalation jurisdiction` — open.
- `RQ-07 — Multi-user identity, ownership, and relationship model` — open.
- `RQ-08 — Voice, languages, wake word, and interruption model` — open.
- `RQ-09 — Memory retention, export, backup, and deletion promises` — open.
- `RQ-10 — Notification and trusted-contact transport` — open.
- `RQ-11 — Support lifetime and continuity promise` — open.
- `RQ-12 — Canonical product name` — partially resolved; repository name is fixed and the product-facing name remains open.
- `RQ-14 — Godot presentation mode and screen habitat` — open.

The submitted comprehension instead maps these IDs to architecture/plugins, model selection, database strategy, cloud boundary, safety evidence, contact flow, shipping population, longitudinal evaluation, touch/physical embodiment, and construction views. Several are legitimate planning topics elsewhere, but they are not the corresponding RQ records. The `RQ-12` touch/physical-embodiment statement is unsupported by the canonical queue.

This fails the directive requirement to explain every open or partially resolved decision without inventing answers.

### F-02 — ADR traceability is semantically wrong

`TRACEABILITY.md` repeatedly cites identifiers whose actual decisions do not support the associated statement. Examples:

- Notion source-of-truth is `ADR-02 — Use Notion as the single source of truth for project meaning and status`, not ADR-19.
- Companion/caregiving separation is `ADR-03 — Keep the caregiving safety core architecturally independent from the companion`, not ADR-10.
- Hybrid organism direction is `ADR-04`; homeostatic drives are `ADR-06`.
- Dream/fact separation is `ADR-09 — Treat dreaming as governed offline consolidation, not factual experience`, not ADR-06.
- Uncertain perception is `ADR-11`; affect limits are `ADR-12`, not ADR-08.
- Local survival and owner portability are `ADR-14`, not ADR-15/16.
- `ADR-19` rejects a monolithic LLM; it does not establish Notion governance.

The table is structurally complete but semantically invalid. Presence of an ADR number is not traceability.

### F-03 — Risk traceability is materially misassigned

Primary risks are omitted or replaced with unrelated IDs. At minimum:

- Caregiving utility must directly account for `RISK-01 — Missed qualified emergency or distress event` and `RISK-02 — False safety escalation and alarm fatigue`.
- Privacy/security must directly account for `RISK-03 — Biometric misidentification or spoofing` and `RISK-04 — Private camera, microphone, memory, or safety data exposure`.
- Development/teaching must account for `RISK-11 — Developmental gates produce either a fake infant or an unsafe/incompetent system`.
- Persistent identity/memory must account for `RISK-05 — False or corrupted autobiographical memory`; continuity also materially relates to `RISK-08 — Cloud, subscription, vendor, model, or service shutdown`.

Every risk citation must be checked by title and substantive relationship, not numeric proximity.

### F-04 — Contradiction report repeats the RQ error

`CONTRADICTIONS.md` describes `RQ-14` as a later art-construction choice. The canonical queue defines `RQ-14` as Godot presentation mode and screen habitat. Remaining construction and three-quarter references are open visual work, but they are not the meaning of RQ-14.

### F-05 — Validation established structure, not semantic correctness

The submitted checks verified headings, counts, JSON parsing, uniqueness, and file presence. They did not verify that each RQ/ADR/risk ID matched its title and supported the relationship claimed. The previous `PASSED` claims for comprehension, traceability, and contradiction analysis are superseded until this semantic correction passes review.

## Required continuation

The same directive remains active. Codex must perform a focused correction pass:

1. Re-fetch the current Open Decisions page, Architecture Decision Ledger, and Initial Risk Register.
2. Rewrite `COMPREHENSION.md` section 15 using exact `ID — title — status — unresolved consequence` entries. Remove unsupported touch/physical-embodiment language.
3. Audit every ADR reference in `TRACEABILITY.md`; include each cited ADR's exact title at first use and retain only substantively relevant references.
4. Audit every risk reference in `TRACEABILITY.md`; include each cited risk's exact title at first use and restore omitted primary risks.
5. Correct `CONTRADICTIONS.md`, especially C-01 and C-08, so visual construction work and `RQ-14` screen-habitat work are not conflated.
6. Update `EVIDENCE.md` with a semantic validation method that verifies ID/title pairs and relationship relevance.
7. Update `HANDOFF.md`, `.agent` current state, the Notion coder report, directive status, and GitHub Issue #1 with this review and the correction result.
8. Preserve the existing manifest and prior commits. Update source markers only when a source is re-fetched or changed; do not rewrite history.
9. Commit and normally push the focused correction, then return a revised canonical `CODEX RESULT`.

## Correction acceptance gate

The next review passes only when:

- all 11 open/partial RQ records are accurately represented;
- every cited ADR ID matches its exact title and materially supports the statement;
- every cited risk ID matches its exact title and materially relates to the pillar;
- no unsupported project fact remains;
- task artifacts, Notion, `.agent` state, issue handoff, and GitHub head agree;
- product implementation remains closed.

## Architect disposition

- Retrieval coverage: `PROVISIONALLY ACCEPTED`.
- Repository scope and hygiene: `ACCEPTED`.
- Visual identity understanding after correction commit: `ACCEPTED`.
- Open-decision understanding: `FAILED — CORRECTION REQUIRED`.
- ADR/risk traceability: `FAILED — CORRECTION REQUIRED`.
- Overall ingest certification: `NOT ACCEPTED; DIRECTIVE CONTINUED`.
- Next-phase authority: `NOT GRANTED`.
