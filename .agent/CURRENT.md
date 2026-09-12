# Current Project State

## Current stage

Roadmap Phase 02 remains active and not accepted. Architecture v1.0 remains adopted. Roadmap Phase 01 remains accepted. Phase 03 and later remain closed.

PR #9 at reviewed head `4263ae7cc085475e9b80f1c00615639ebbba679b` is continued under:

- Directive: `COMPANION-P02-EMBODIMENT-001-R04-C04`
- Repository review: `.agent/tasks/active/COMPANION-P02-EMBODIMENT-001/ARCHITECT_REVIEW_08.md`
- Notion review: https://app.notion.com/p/3d9833cb27ff81f5a5e6f29d53888e48
- Issue #8: open
- PR #9: draft, open, unmerged

## Review 08 disposition

C03 is accepted within its bounded diagnostic/intake/runtime scope. Retain:

- exact ALSA diagnostic capture before correction;
- explicit Godot Dummy-audio qualification;
- one canonical Godot runner and channel classifier;
- separate stdout/stderr/engine/Xvfb logs and hashes;
- cold/warm Godot qualification;
- fail-closed application-error policy;
- always-published diagnostic artifacts;
- exact final-head Phase 02 workflow `34671402258`: SUCCESS;
- artifact `10290394916`, digest `sha256:d396c2213bfa68da0927380b85ea1bee499fd0dac95a10eacc1f90049a1b68d3`.

`READY_FOR_ARCHITECT_FRAME_PACK` is not yet accepted because the final exact task head triggered Phase 01 run `34671402263`, which failed in `foundation_runtime_check.py` before later foundation checks.

## Decisive blocker

The Phase 01 runtime probe waits for `supervisor.sock` and then samples health exactly once. The final failure observed the supervisor resident and all expected roles present, but `observed_ready=false` and `care_coverage=degraded`.

A control socket becoming available is not equivalent to all children completing startup. The health contract already exposes explicit readiness state. The qualification must wait for stable complete readiness rather than sample once immediately after socket creation.

## Active objective

Codex executes only R04-C04:

1. preserve completed C02/C03 work;
2. replace the one-shot readiness sample with bounded monotonic polling of explicit health state;
3. require all expected roles healthy/ready and `care_coverage=synthetic`;
4. require two consecutive complete-ready observations before success;
5. retain a sanitized startup trace and fail closed on timeout or early supervisor exit;
6. add delayed-ready, never-ready, and supervisor-exit synthetic tests;
7. run complete Phase 01 verification;
8. obtain one exact-head hosted Phase 01 success plus two same-head rerun successes;
9. keep Phase 02 green on the same exact task head;
10. return `READY_FOR_ARCHITECT_FRAME_PACK` only after that stability proof.

No production character pixels or operator visual-review request are authorized in C04.

## External evidence basis

Service readiness is distinct from process or socket existence. The authoritative Companion readiness values are the child `ready/state` fields and `care_coverage`, so the probe must wait on them rather than infer startup completion from endpoint creation.

## Protected work

The primary SSHFS checkout's operator-owned `.gitignore` and `AGENTS.md` modifications remain protected. Continue only in the clean local ext4/NVMe secondary worktree.

## Capability boundary

No Architect-authored production frame pack, accepted body construction, approved motion language, production embodiment, visual aliveness, or Phase 03+ capability exists. C03 establishes substantial bounded synthetic engineering evidence, but final pre-art readiness is blocked by inherited Phase 01 readiness-test nondeterminism.

## R04-C04 implementation status — 2026-09-12

Architect Review 08 was merged normally from `origin/main` as merge commit
`e9915015a4df69f1af895ae33cefc97a7440c218` after verifying the additional
authority-only main commits. The inherited resident probe now uses monotonic,
bounded polling of explicit health state, requires two consecutive complete-ready
samples separated by a nonzero interval, records a sanitized startup trace, and
fails closed on timeout or supervisor exit. Deterministic delayed-ready,
never-ready, and early-exit tests pass. Local Rust 1.98.1 checks and the actual
resident probe pass; hosted same-head stability and publication remain required.

## R04-C04 completion — 2026-09-12

Candidate `e5f3bbb47f9f20d3e896956c9a1aabcd751cfd3b` passed hosted Phase 01
run `34674883461` / job `103502845478`, same-head rerun #1 job `103503853827`,
and same-head rerun #2 job `103504776796`. Phase 02 run `34674883457` / job
`103502845517` passed on that exact SHA and published artifact `10292635102`
(`sha256:6efff4d21517c1983ddabfa86f9eaaf516ee60be0557625890d3ca7944f68fb8`).
The bounded handoff is `READY_FOR_ARCHITECT_FRAME_PACK`; Phase 02 remains
active and unaccepted, with no production art or visual approval claimed.
