# Architect Review 02 — COMPANION-P00-ARCH-001

Status: `ACCEPTED — ARCHITECTURE V1.0 ADOPTED`

Acceptance authority: `ChatGPT AI Architect`

Reviewed range: `c36525ae5e1bb478baf679cacc1a5f2fd22020c8..1ceb330d4c2321b500a138b8acfdfeb4279c08e7`

Focused correction: `25b1c737d6f8f1f861a36355909c2a51ea5c64ea`

Publication reviewed: `1ceb330d4c2321b500a138b8acfdfeb4279c08e7`

Canonical review: https://app.notion.com/p/3d6833cb27ff81d88785f64d0629286c

Adopted architecture: https://app.notion.com/p/3d6833cb27ff81e99c52dc33b53f2556

GitHub Issue #3: https://github.com/SketchOTP/companion/issues/3

## Defensive supersession result

Codex correctly refused a later stale instruction to synchronize backward to `c36525ae5e1bb478baf679cacc1a5f2fd22020c8`. That commit was already an ancestor of the published focused correction and reconciliation. Rewinding would have discarded valid work and risked overwriting user-owned local Graft edits. The blocked response is accepted as correct defensive behavior and is not a task failure.

## Independent review

The Architect reviewed the correction commit chain, all changed paths, current remote main, the updated Notion report, direct safety ingress, vault authority, event/time profile, roadmap contracts, language/toolchain gate, exact SQLite rule, evidence floors, threat/degradation tests, traceability, evidence, and handoff.

The correction changes remain planning/governance-only. No product source, Godot project/execution, production asset, installed dependency, manifest, CI workflow, deployment, database implementation, model/data/voice, media capture/playback, biometric implementation, notification delivery, or safety runtime was introduced. Product/runtime tests were not applicable.

## Review 01 corrections

1. **Direct safety ingress — PASSED.** Authorized sensor/speech producers address safety candidates directly to care-core. Care owns accepted/rejected input receipts and incidents. Companion availability, database, output, mood, memory, models, dreams, and animation cannot gate or manufacture the path.
2. **Identity/consent/contact/secret authority — PASSED.** An explicit identity-consent-vault owns consent/revocation, biometric handles/templates, contacts/roles, provider credential handles, key references/recovery metadata, and privileged audit. Degraded states fail closed.
3. **Canonical bytes/time — PASSED.** JCS-RFC8785-v1, sha-256-jcs-event-v1, digest scope, numeric/Unicode rejection, fixed-point/wide-number rules, boot ID, monotonic time, UTC uncertainty, event sequence, and causation are specified.
4. **Roadmap semantics — PASSED.** Phase 01 engineering foundation is distinct from the later Phase 02/03/04/10 architecture-proof milestone; passing the milestone completes no phase.
5. **Toolchain gate — PASSED.** EXP-00 defines Python 3.12 versus one compiled comparator without a premature production winner.
6. **SQLite rule — PASSED.** Eligibility requires one exact supported non-withdrawn release or documented fixed backport plus complete build/topology/security and failure evidence. Numeric minimum rules are rejected.
7. **Evidence floors — PASSED.** 100 replay/restart cases, 1,000 cycles, and 30 minutes are provisional engineering defect-detection floors diversified across seeds, states, schemas, persisted states, boots, and durable-boundary kill points. They are not product reliability or safety evidence.

## Additional adopted implementation gate

Linux AF_UNIX socket permissions and peer credentials are useful primitives but do not distinguish authorization solely by UID when multiple processes share one user. Before implementing direct safety ingress, Phase 01 must select and target-test an identity/capability mechanism independent of message-declared identity. Unauthorized same-user processes must be unable to create valid safety candidates.

## Technology decisions

- Rust is selected as the one compiled comparator against Python 3.12. This does not select the production language.
- Godot 4.7.2 remains selected but absent/unqualified.
- SQLite remains conditional; no release or binding is approved.
- No dependency is approved by this review.

## Local working-tree boundary

Codex reported intentionally uncommitted user-owned Graft changes to `.gitignore` and `AGENTS.md`. These were not part of the reviewed remote commits and are not independently verified here. Future work must inspect and preserve them. Do not commit, discard, overwrite, reset, or reinterpret them without explicit authority.

## Final disposition

- `COMPANION-P00-ARCH-001`: `ACCEPTED — COMPLETE`.
- Architecture v1.0: `ADOPTED`.
- Roadmap Phase 00: `ACTIVE — INCOMPLETE`.
- Roadmap Phase 01: `CLOSED` pending foundation qualification and a new implementation-opening directive.
- Dependencies: `NONE APPROVED`.
- Product implementation/capability: `NOT OPENED / NOT CLAIMED`.

The next critical path is a bounded foundation technology and trust qualification: Python versus Rust, direct safety-producer IPC identity, exact Godot 4.7.2 artifact, exact persistence artifact/build, and selected supervision assumptions.
