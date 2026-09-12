# Architect Review 08 — C03 Accepted; Exact-Head Phase 01 Readiness Race Must Be Stabilized

## Verdict

`CONTINUE — C03 ACCEPTED; READY_FOR_ARCHITECT_FRAME_PACK NOT YET ACCEPTED ON FINAL EXACT HEAD`

- Reviewed branch: `codex/p02-embodiment-001`
- Reviewed head: `4263ae7cc085475e9b80f1c00615639ebbba679b`
- PR: `#9 — DRAFT / OPEN / UNMERGED`
- Issue: `#8 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: accepted capability boundary; inherited CI readiness gate currently flaky
- Roadmap Phase 02: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 03 and later: `CLOSED`
- Canonical Notion review:
  https://app.notion.com/p/3d9833cb27ff81f5a5e6f29d53888e48

C03 solved the Godot diagnostic-parity blocker. The exact ALSA error was retained
before correction, wrapper and Godot channels are now separated, qualification
uses the documented Dummy audio driver, and the final exact-head Phase 02
workflow is green. C03 is accepted within its bounded synthetic intake/runtime
scope.

Frame-pack readiness is still blocked because the same final task head triggered
a failing inherited Phase 01 workflow. Independent inspection shows a concrete
one-shot startup-readiness race in `scripts/foundation_runtime_check.py`.

## Retained C03 evidence

Do not repeat unless inputs change:

- exact historical Godot ALSA diagnostic capture;
- explicit `--audio-driver Dummy` qualification boundary;
- canonical Godot runner shared by CI and evidence generation;
- separate stdout, stderr, Godot engine log, and Xvfb diagnostic channels;
- fail-closed Godot `ERROR:` classification;
- cold/warm Phase 02 qualification;
- always-upload diagnostic artifact behavior;
- semantic/tamper-negative C02/C03 evidence;
- exact final-head Phase 02 workflow `34671402258`: SUCCESS;
- exact final-head Phase 02 artifact `10290394916`, digest
  `sha256:d396c2213bfa68da0927380b85ea1bee499fd0dac95a10eacc1f90049a1b68d3`.

## New independent blocker

Exact-head Phase 01 workflow `34671402263` failed during `Contract validation`.
The runtime check reported:

- supervisor resident: true;
- all five expected roles present;
- `observed_ready=false`;
- `care_coverage=degraded`;
- process-owned network sockets: zero;
- shutdown return code: zero.

Later Phase 01 steps were skipped.

### Root cause in the readiness probe

`foundation_runtime_check.py` currently:

1. starts `ops-supervisor`;
2. waits only for `supervisor.sock` to exist;
3. issues exactly one health query;
4. immediately evaluates child readiness and care coverage.

A connectable control socket proves that the supervisor endpoint exists. It does
not prove all supervised child processes have completed startup. The health
contract already exposes the explicit readiness state, so the probe should wait
on that state rather than infer readiness from socket creation.

The exact-head failure is consistent with this race: all expected roles were
already visible, but one or more child readiness transitions and synthetic care
coverage had not completed at the instant of the single health sample.

Earlier green reruns do not remove the defect. Alternating pass/fail behavior on
unchanged semantics is itself evidence that the qualification is nondeterministic.

# CODEX DIRECTIVE — COMPANION-P02-EMBODIMENT-001-R04-C04

## Objective

Stabilize the inherited Phase 01 resident-readiness qualification without
weakening its acceptance condition, then prove Phase 01 and Phase 02 green on the
same final exact task head.

Return `READY_FOR_ARCHITECT_FRAME_PACK` only after repeated exact-head success.

## Why this is next

C03 is accepted. The only current blocker is the inherited foundation runtime
probe's one-shot readiness sample. Production-art authoring must not begin while
the accepted-foundation regression gate remains timing-dependent.

## Authoritative basis

Read and reconcile:

- Architecture v1.0;
- accepted Phase 01 foundation boundary;
- Architect Reviews 06–08;
- current Phase 02 directive and report;
- `scripts/foundation_runtime_check.py`;
- `.github/workflows/phase01.yml`;
- final-head Phase 01 run `34671402263` logs;
- final-head Phase 02 run `34671402258` and artifact;
- PR #9 and Issue #8.

## Scope

### A. Preserve completed C02/C03 work

Do not modify the authored-frame schemas, bounded request profile, PNG policy,
fsync/atomic-intake semantics, canonical Godot runner, Dummy-audio correction,
or visual-authorship boundary unless the readiness investigation directly proves
a dependency.

### B. Correct `foundation_runtime_check.py`

Replace socket-exists -> single-health-sample behavior with an explicit readiness
wait based on monotonic time.

The complete ready condition is:

- supervisor process remains alive;
- all five expected roles are present;
- every expected child reports `ready=true`;
- every expected child reports `state=healthy`;
- `care_coverage == synthetic`.

Poll until the complete condition is observed or the bounded timeout expires.

Require at least **two consecutive** complete-ready observations separated by a
nonzero poll interval before declaring readiness stable.

Do not treat socket existence as service readiness.

### C. Retain bounded startup evidence

The result JSON must include a sanitized startup trace sufficient to diagnose a
failure:

- sample index;
- monotonic elapsed milliseconds;
- observed role set;
- ready roles;
- not-ready/unhealthy roles;
- care coverage;
- supervisor alive state;
- query error class when present.

Also record:

- `socket_observed_ms`;
- `all_roles_observed_ms`;
- `all_ready_observed_ms`;
- `stable_ready_observed_ms`;
- total sample count;
- timeout and poll interval.

Do not retain hostnames, usernames, private absolute paths, capabilities, packet
contents, or secret-bearing environment data.

### D. Fail closed

If the deadline expires, fail and preserve the final health sample plus a
sanitized bounded supervisor stderr tail.

If the supervisor exits during startup, fail immediately.

Do not silently extend the timeout according to runner speed.

### E. Prove the race and correction

Add focused synthetic readiness tests where:

1. the control endpoint becomes available before child readiness;
2. early samples report degraded/not-ready;
3. later samples report complete readiness;
4. the corrected waiter passes only after stable readiness;
5. a never-ready fixture times out and fails;
6. a supervisor-exits-before-ready fixture fails immediately.

Do not modify production child startup merely to make the check pass.

### F. Re-run complete inherited gates

Run the complete Phase 01 workflow, not only the readiness script. The exact
final task head must show Phase 01 and Phase 02 green simultaneously.

### G. Stability proof

After the first exact-head Phase 01 success, rerun the Phase 01 `verify` job at
least **twice** on that same exact commit. Both reruns must pass.

Retain the exact-head Phase 02 green result. Rerun Phase 02 only if C04 changes a
shared dependency, workflow input, or repository path consumed by Phase 02.

## Required validation

- delayed-ready synthetic waiter: PASS;
- never-ready timeout negative: PASS;
- supervisor-exits-before-ready negative: PASS;
- actual local foundation runtime check: PASS;
- complete local Phase 01 verification: PASS;
- exact-head hosted Phase 01: PASS;
- two additional exact-head Phase 01 reruns: PASS;
- exact-head hosted Phase 02: PASS;
- `git diff --check`: PASS;
- secret/private-path scan: PASS.

## External basis

Service-manager readiness semantics distinguish endpoint/process creation from
startup completion. A service should signal or expose readiness only after
initialization is finished. Companion already exposes explicit child `ready`,
`state`, and `care_coverage` health fields, so the qualification must wait for
those authoritative values rather than equating control-socket creation with
readiness.

## Do not change

- approved reference bytes and hashes;
- visual-authorship boundary;
- `MON_FRAME_V1`;
- authored-frame source/ingested/receipt contracts;
- Architecture v1.0;
- Godot 4.7.2;
- canonical C03 Godot diagnostic boundary;
- accepted Phase 01 capability claims;
- existing branch, PR #9, and Issue #8;
- protected operator-owned primary-worktree edits.

## Prohibited work

No production character pixels, no operator visual review, no new art/3D
dependency, no sprite-library expansion, no final atlas scale-up, no Openbox
endurance, no Phase 03 work, no PR merge, and no Issue closure.

## Acceptance criteria

C04 passes only when:

1. readiness is evaluated from explicit health state rather than a one-shot
   socket-existence sample;
2. stable readiness requires consecutive complete-ready observations;
3. never-ready and early-exit cases fail closed;
4. startup evidence is retained and sanitized;
5. Phase 01 is green three consecutive times on the same exact task head;
6. Phase 02 is green on that exact task head;
7. final local and remote task heads match;
8. final handoff status is exactly `READY_FOR_ARCHITECT_FRAME_PACK`.

No art or Phase 02 acceptance follows automatically.

## Stop and return to Architect if

- explicit health never converges despite child processes actually being healthy;
- correction requires changing product startup semantics rather than the probe;
- readiness stabilization requires an unapproved dependency;
- Phase 01 continues to fail after deterministic readiness polling;
- current `origin/main` cannot be merged normally;
- protected work cannot be preserved.

Return the exact startup trace and minimum Architect decision required.

## Required project updates

Update active Phase 02 task records, `.agent/CURRENT.md`, `.agent/INDEX.md`,
append-only directive/outcome/record/learning state, Phase 02 Notion directive and
report, PR #9, and Issue #8. Preserve C02/C03 evidence and historical failures.

Leave PR #9 draft/open/unmerged and Issue #8 open.

## Required handoff

Return:

`CODEX RESULT — COMPANION-P02-EMBODIMENT-001-R04-C04`

with:

- original exact-head Phase 01 failure;
- readiness-race proof;
- corrected readiness algorithm;
- startup trace fields;
- positive/negative readiness tests;
- local Phase 01 result;
- exact-head Phase 01 run ID;
- two exact-head rerun job IDs;
- exact-head Phase 02 run ID;
- artifact/hash evidence where applicable;
- Notion/GitHub reconciliation;
- commits and remote equality;
- final readiness status.

## Capability boundary

A passing C04 establishes a stable pre-art engineering gate only. It does not
accept visual art, Phase 02, visual aliveness, organism behavior, or later
product capability.
