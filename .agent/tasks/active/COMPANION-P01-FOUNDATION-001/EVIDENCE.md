# Phase 01 Evidence Record — COMPANION-P01-FOUNDATION-001

Status: `IMPLEMENTED — AWAITING ARCHITECT REVIEW`

For every material claim, record:

- requirement and acceptance criterion;
- exact command/test;
- exact build, artifact and dependency identities;
- fixture/seed/input identity;
- expected and observed result;
- result artifact and hash;
- commit SHA and CI run;
- evidence level and ceiling;
- failed, blocked or unqualified surfaces;
- Notion/GitHub publication reference.

Required evidence groups:

1. authority and protected-work reconstruction;
2. clean-clone/bootstrap/build;
3. contracts/canonicalization;
4. XDG/storage refusal;
5. process/supervisor/health;
6. direct-care IPC and negatives;
7. persistence/migration/integrity/backup/restore;
8. Godot headless and bounded-window behavior;
9. CI/SBOM/license/provenance/scans;
10. 1,000-cycle matrix;
11. 60-minute soak and failure recovery.

No result may be upgraded beyond what was executed. Preserve negative evidence.

## Current execution record

The clean secondary worktree implemented and exercised the modular Rust
workspace, contract schemas, canonical integer/JCS-shaped encoder, XDG guard,
six service shells, supervisor-created direct synthetic care channel, separate
care/companion/vault SQLite migrations, Godot 4.7.2 headless shell, health
command, bootstrap/verification scripts, CI definition and a 3-seed/3,000-
cycle synthetic matrix. Runtime stores and build outputs remained outside Git
under caller-selected temporary/XDG roots. These are E1/E2/E3 engineering
observations only; no product, safety, security-certification or reliability
claim is made. A bounded Openbox window probe passed without media capture;
display-loss recovery and the full 60-minute soak remain unqualified until
their long-running host evidence is independently reviewed.

## Review 01 continuation evidence

The resident runtime now has a stable private control socket and a process
registry. `scripts/cycle_matrix.py` drove three retained seeds through 1,000
actual packet cycles each (3,003 packets including one duplicate per seed),
with durable care receipts and no companion dependency. `scripts/health.py`
queries the live supervisor. Rust persistence uses direct SQLite ABI calls,
prepared statements, committed migration text, integrity/checkpoint methods,
and the Online Backup API. XDG resolution follows the specification and fails
closed on missing required bases and unsafe placement. These results are E3
target tests for the synthetic foundation; producer replacement, broad
failure/recovery injection, target-host display recovery, and a completed
continuous 60-minute injected soak remain unqualified.

## Review 01 continuation evidence — 2026-09-10

Commands and observations:

- `cargo fmt --all`, `cargo clippy --workspace --all-targets --all-features
  --locked -- -D warnings`, `cargo test --workspace --locked`, and
  `cargo build --workspace --locked --release`: `PASSED`.
- `bash scripts/verify.sh`: `PASSED` with exit code 0. It ran the locked
  workspace checks, Draft 2020-12 fixture validation, nine-schema/type
  crosswalk, actual resident 3-seed matrix, three-store smoke, direct-care
  smoke, bounded failure matrix, SPDX generation, live health query, and
  resident no-egress check.
- `scripts/cycle_matrix.py --cycles 1000 --seeds 17,23,41`: 3,000 accepted
  packets plus one duplicate rejection per seed; evidence ceiling `E3`.
- `scripts/storage_smoke.py`, `scripts/direct_care_smoke.py`, and
  `scripts/failure_matrix.py`: all bounded synthetic checks `PASS`; they do
  not establish production persistence, security, or safety properties.
- With private `COMPANION_SQLITE_SOURCE` set to the cached 3.53.4 amalgamation,
  the Rust build linked a static exact-source archive; `ldd` showed no sqlite
  dynamic dependency and the binary exposed `3.53.4`. The source digest is
  `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189`.

Unqualified surfaces remain: 3,600-second injected soak; full process
replacement and capability rotation; target-host display-loss recovery;
adversarial descriptor/capability attacks; and the complete SQLite VFS,
power-loss, and long-duration matrix. These are recorded as `NOT RUN`, not
converted to passes.

## Live authority re-fetch — 2026-09-10

Immediately before publication reconciliation, the live Architecture Decision
Ledger query returned 52 rows (31 Adopted, 19 Interim, 2 Rejected). The live
Research Evidence Register query returned 55 rows (42 Grade A, 11 Grade B,
2 Grade C, 0 Grade D). The required Phase 01 directive, coder report,
canonical project, roadmap, Architect Review 01, GitHub Issue #6, and PR #7
were re-fetched or inspected. Retrieval confidence remains `ADEQUATE`; no
material authority contradiction was found. Notion and GitHub state still
record the phase as active and unaccepted.
