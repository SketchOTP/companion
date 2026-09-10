# Architect Review 03 — COMPANION-P00-QUAL-001

## Verdict

`CONTINUE — NARROW EVIDENCE-BINDING CORRECTION REQUIRED`

- Reviewed PR head: `fd6f4752ed4fed33c79bbcf8d1da2475724c40ba`
- Pull request: `#5` — open, draft, unmerged
- GitHub issue: `#4` — open
- Merge approval: `NOT GRANTED`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `CLOSED`
- Dependency adoption: `NONE`
- Product implementation: `CLOSED`
- Canonical Notion review: https://app.notion.com/p/3d6833cb27ff81b38ea9e132d31888ab

## Review scope

The Architect independently inspected the final-hardening commit range, current PR metadata and body, the committed result bundle, provenance manifest, fail-closed validator, Python/Rust/Node canonicalization harnesses, real-process IPC harness, SQLite matrix and VFS wrapper, current Notion report/directive, and live ADR/evidence counts. Current primary sources were rechecked for Rust 1.98.1, Godot 4.7.2, SQLite 3.53.4, RFC 8785, and the `canonicalize` package.

## Evidence retained

Do not repeat unchanged qualification work. Retain:

1. Protected primary-worktree handling and local ext4/NVMe secondary-worktree isolation.
2. Exact Godot 4.7.2 artifact/version evidence at `E1_OBSERVED`.
3. Transient systemd-user feasibility at bounded `E3_TARGET_TESTED`.
4. Weak pathname-socket injection as accepted evidence of insufficiency.
5. Separate supervisor, producer, care, and attacker processes; actual `SOCK_SEQPACKET` traffic; `SCM_CREDENTIALS`; pidfd liveness; restart/replay; generation/capability rejection; and the exact host `pidfd_getfd=EPERM` result as bounded observations only.
6. Bounded Python/Rust/oracle profile agreement and release-build timing/RSS observations.
7. SQLite 3.53.4 identity, overlap, migration rejection, backup/restore, page-limit failure, and narrow `xSync` observations as bounded candidate evidence.

These observations do not adopt a language, IPC mechanism, database, supervisor, canonicalizer, dependency, or product capability.

## Why final acceptance remains blocked

### 1. Result files are not bound to provenance or runner history

`validate_results.py` reads curated JSON summaries but does not recompute and compare the result-file SHA-256 values recorded in `provenance.json`, verify the committed fixture hash, or verify that the evidence commit belongs to the checked-out branch history. `validation_results.json` is consumed as a self-declared pass input, creating circular evidence.

`provenance.json` records `2026-09-09T00:00:00Z` as an execution timestamp. That is a date placeholder, not observed timestamp precision. It also lacks the exact source commit or npm registry-integrity identity for `canonicalize@5.0.0`. The results README lacks the required regeneration procedure and environment inputs.

### 2. IPC pass fields include construction assertions rather than observations

The corrected process path is real, but several fields—descriptor inheritance closure, opposite-endpoint absence, and supervisor non-read behavior—are hard-coded instead of instrumented or explicitly classified as code-inspected properties.

The runner does not assert every required runtime outcome: the exact old-channel failure, successful valid receipt with companion/database absent, absence of capability material from attacker argv/environment, denied descriptor acquisition, and all readiness/hardening fields. The field `false_normality=true` is semantically inverted and must be replaced by an unambiguous statement such as `normal_coverage_claimed=false`.

### 3. Toolchain/JCS summaries claim more than the runners establish

The bounded profile vectors are useful. However, durable result fields such as `altered_digest_detection`, `no_egress`, `controlled_shutdown`, and full `rejection_reasons` parity are not each tied to a matching assertion and sanitized runner outcome. The escaped-equivalent duplicate case is present in shell self-tests, but the conformance runner does not directly submit it through both shells. The validator checks curated booleans rather than deterministic raw-to-summary derivation.

Unsupported fields may be removed or narrowed instead of expanding this qualification.

### 4. SQLite state preservation is not calculated exactly

`sqlite_results.json` records `logical_state_preserved=true` for checkpoint faults, but `sqlite_matrix.py` does not calculate a complete before/after logical and schema digest for those fault cases. It checks target count and integrity.

The concurrency matrix derives expected old/new counts from observed values instead of recording the pre-transaction count and requiring `during == before` and `after == before + 1`. Commit-fault cases do not prove all pre-existing logical state remained unchanged. These gaps allow a weaker outcome than the durable summary claims.

## Required narrow correction

### A. Bind results to provenance

- Recompute and verify every committed result-file SHA-256 recorded by the manifest.
- Recompute and verify the committed fixture hash.
- Record actual start/end UTC timestamps, or rename the field to an honest date-only value; do not fabricate midnight precision.
- Add the exact npm registry integrity or exact source commit for `canonicalize@5.0.0`, in addition to the tarball SHA-256.
- Add a concise regeneration procedure and required environment inputs to `results/README.md`.
- Treat `validation_results.json` only as generated output; do not trust it as an input to its own verdict.
- Verify that the evidence commit is an ancestor of the checked-out final branch head.

### B. Make IPC claims correspond to observed evidence

- Derive descriptor/endpoint ownership fields from instrumentation, label them `CODE_INSPECTED`, or remove them.
- Assert the exact old-channel failure result.
- Assert a valid care receipt while `companion-core` and its database are absent.
- Assert attacker argv/environment contain no capability material and descriptor-acquisition attempts return the exact expected failures.
- Assert every producer/care readiness and child-hardening field.
- Replace the ambiguous outage field with `normal_coverage_claimed=false` or equivalent.
- Exit nonzero for every required mismatch.

### C. Align JCS/toolchain claims with executed evidence

- Submit decoded escaped-name duplication through both shells, or remove the cross-language claim.
- Compare exact sanitized rejection/result codes wherever parity is claimed.
- Test or remove `altered_digest_detection`, `no_egress`, and `controlled_shutdown` result fields.
- Generate the committed summary from sanitized runner output, or commit the sanitized raw output from which it deterministically derives.
- Keep queue overflow explicitly deferred and Rust unselected.

### D. Make SQLite state assertions exact

- Record the row count before the overlapping writer; require both readers to see that exact count and post-commit readers to see exactly `before + 1`, including the inserted row.
- For commit faults, compare all pre-existing logical/schema state after reopen and separately require the three-row transaction group to be wholly absent or wholly present.
- For checkpoint faults, calculate complete logical/schema state immediately before the injected checkpoint and after reopen; all already committed rows must remain present.
- Derive `logical_state_preserved` from those digests rather than curating it.
- Generate the sanitized summary deterministically from runner results and validate its hash.

### E. Reconcile publication

Update the active packet, mutable Authority state, append-only superseding records, Coder Qualification Report, parent directive, PR #5 body, and Issue #4. Preserve all prior failed attempts as history. Leave PR #5 draft/open/unmerged and Issue #4 open.

## Acceptance gate

The next result passes only when:

1. Provenance and fixture hashes are recomputed and verified by the validator.
2. Timestamp precision and `canonicalize@5.0.0` source identity are honest and exact.
3. The README contains a reproducible regeneration procedure.
4. IPC pass fields are observed, code-inspected and labeled, or removed; every required runtime outcome is asserted.
5. JCS/toolchain result fields exactly match executed checks.
6. SQLite concurrency and fault outcomes are tied to explicit before/after state digests and exact count relationships.
7. Curated summaries are deterministically traceable to sanitized runner outputs.
8. Protected work remains untouched; PR #5 and Issue #4 remain open; no dependency, phase transition, implementation, security certification, reliability claim, or safety-efficacy claim is created.

## Publication rule

Continue on `codex/p00-qual-001` and update existing draft PR #5. Use one narrow correction commit and at most one publication-reconciliation commit. Do not rerun unchanged Godot or systemd work. Do not broaden the qualification scope. Stop for independent Architect review.

## Disposition

- Qualification task: `CONTINUE — EVIDENCE INTEGRITY ONLY`.
- PR #5: draft/open/unmerged; not approved.
- Architecture v1.0: adopted and unchanged.
- Roadmap Phase 01, dependencies, and product implementation: closed.
- Live source snapshots at review: 45 ADRs and 55 research-evidence records.
