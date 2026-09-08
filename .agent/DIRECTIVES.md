# Directive Ledger

Historical entries are append-only after adoption.

## COMPANION-AUTHORITY-BOOTSTRAP-001 — Install Authority 3.0 governance

- Issued: 2026-09-08 America/New_York
- Issuer: operator
- Status: `COMPLETED_FOR_ARCHITECT_REVIEW`
- Objective: set up the new `SketchOTP/companion` repository to use the documented Authority 3.0 governance from the canonical Notion hierarchy.
- Why this is next: the operator created and identified the production repository and explicitly authorized governance installation before any product work.
- Scope: inspect Notion and GitHub, preserve existing bootstrap files/history, install Authority governance files, configure repository-local Git identity, validate, commit, push, and reconcile Notion.
- Do not change: product architecture, application code, assets, dependencies, research decisions, safety behavior, deployment, or prior Git history.
- Required investigation: fetch the canonical project page, governance contract, Research Phase 01, and Authority 3.0 package; inspect the remote repository and local working tree.
- External discovery: `NOT REQUIRED` — governance installation only; no technical or dependency selection.
- Acceptance criteria:
  1. Canonical Authority router, project state, reusable workflow, references, and task-packet structure are present.
  2. The exact operator goal and Notion success criteria are preserved in the durable project goal.
  3. Research Phase 01 stays active and implementation remains unauthorized.
  4. Existing `.gitignore`, `LICENSE`, initial commit, and remote history remain intact.
  5. No application source, dependency, asset, CI, deployment, or product configuration is added.
  6. Structural, placeholder, secret, diff, Git identity, and remote synchronization checks are recorded honestly.
  7. Notion is reconciled to show a governance-only repository while retaining the implementation gate.
- Required validation: static structure and content checks, `git diff --check`, narrow credential scan, initial-file preservation check, committed-tree inspection, and local/remote SHA equality after normal push.
- Stop conditions: Notion cannot be read; the repository contains unexplained product or dirty work; canonical Authority conflicts materially with current operator authority; a force push or history rewrite would be required; or the work would cross into product implementation.
- Required project updates: `.agent/` ledgers and current state; Notion canonical page, governance contract, and Research Phase 01 after publication.
- Required handoff: canonical `CODEX RESULT` with exact validation and GitHub state.
