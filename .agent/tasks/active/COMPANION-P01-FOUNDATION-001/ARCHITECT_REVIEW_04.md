# Architect Review 04 — COMPANION-P01-FOUNDATION-001

## Verdict

`CONTINUE — PHASE 01 NOT ACCEPTED; ONE NARROW EVIDENCE-SEMANTICS CORRECTION REQUIRED`

- Reviewed PR: `#7`
- Reviewed branch: `codex/p01-foundation-001`
- Reviewed head: `62f1f08f2878aa6be457183050fbd982afbcb47d`
- Required PR state: `OPEN / DRAFT / UNMERGED`
- GitHub Issue: `#6 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 02 and later: `CLOSED`
- Product capability: `NOT ESTABLISHED`
- Canonical Notion review: https://app.notion.com/p/3d7833cb27ff81ea95e4e313f695a988

## Objective

Correct the semantic validity of the Phase 01 evidence without reopening broad
foundation design. The implementation contains substantial reusable foundation
code, but several committed `PASS` results do not demonstrate the named
behaviors.

This continuation is deliberately narrow:

1. repair the control-to-producer injection mapping;
2. make message results enforce expected outcomes and exact reasons;
3. replace self-attesting scenario labels with a smaller directly exercised
   acceptance matrix;
4. align contract claims with actual Rust and wire executions;
5. prove Godot client state transitions rather than bridge-file changes alone;
6. run one focused resident regression after the correction; and
7. bind those semantics in the closeout validator.

When this correction passes independent review, the intended Architect action
is to accept and merge Phase 01 and issue the complete Roadmap Phase 02
embodiment directive. Do not add unrelated hardening or later-phase capability.

## Review scope

The Architect re-synchronized PR #7, current branch history, the final green CI
job, resident supervisor and control plane, direct-care packet generation and
validation, exact SQLite build, contract scripts, failure matrix, Godot reconnect
test, closeout validator, committed evidence, and live Notion result.

Current official documentation was rechecked for Godot socket polling and screen
selection. Godot 4.7 requires socket state to be updated through `poll()` before
state is relied on. Cargo-deny documentation was also rechecked; its advisory,
license, ban, and source checks remain useful later gates but are explicitly
removed from the Phase 01 acceptance blocker.

## Retained implementation progress

Preserve and build on:

1. Rust 1.98.1 workspace and six role-specific binaries.
2. Exact Godot 4.7.2 and SQLite 3.53.4 identities.
3. Fail-closed exact SQLite source build, direct FFI, prepared statements,
   committed migrations, integrity, checkpoint, and backup direction.
4. RustCrypto HMAC and aligned public safety-message fields.
5. Private capability pipes, kernel credentials, retained producer pidfd,
   generation rotation, and direct-pair rebuilding.
6. Corrected XDG placement direction.
7. Resident supervisor and versioned local control socket.
8. Care-owned receipt and attempt storage.
9. Same-process headless Godot bridge reconnect direction.
10. Green CI at the submitted head.
11. The completed 3,600-second resident host run as bounded residency and
    controlled-restart evidence.
12. Exact artifact hashes, Cargo lock, current SBOM, and evidence manifest.

These assets are substantial implementation progress. They do not make the
current evidence semantics valid.

## Material finding 1 — most requested invalid categories were accepted

The committed closeout summary reports 3,000 requested messages with 414
`valid` messages and hundreds of requested replay, malformed,
unsupported-major, unknown-field, invalid-UUID, invalid-date, duplicate-key,
stale-generation, invalid-MAC, companion-state, ordinary-observation, and
unauthorized-sender categories.

The same summary reports:

```text
accepted: 2805
duplicate: 4
rejected: 199
```

The runner increments a category count when the care attempt journal grows. It
does not require that category's expected acceptance state or exact rejection
reason. It creates `expected_rejections` but never uses it.

The control plane maps only `valid` to `inject_valid` and
`ordinary_observation` to `inject_ordinary`; other names are forwarded
unchanged. The producer mutation logic expects names such as `inject_replay`,
`inject_malformed`, `inject_duplicate_key`, `inject_unsupported_major`,
`inject_stale_generation`, and `inject_invalid_mac`. Unrecognized raw names
therefore fall through to valid packet generation.

The committed 3,000-message `PASS` result is rejected and superseded. It proves
only that 3,000 control requests caused journal activity.

## Material finding 2 — the 37-scenario matrix is largely command acceptance

Several scenarios do not induce or verify the behavior named:

- `startup_failure` is true when the live supervisor answers health.
- `readiness_timeout_guard` does not induce a timeout.
- `crash_loop_visibility` only checks that restart fields are integers.
- `vault_denied_operation` becomes true when an injection command is accepted.
- checkpoint, display topology, backup/restore, unsafe-storage, and incompatible
  migration cases can pass from a control response whose observation is only
  `control_state_recorded`.
- store corruption is represented by a marker/command, not by creating and
  detecting corruption in a copied synthetic store.

The committed `37/37` claim is rejected and superseded. Preserve the file as
negative evidence; do not continue trying to defend its scenario labels.

## Material finding 3 — contract closeout overstates wire coverage

The contract script generates one sample from each schema and applies a limited
set of mutations. It does not commit a complete fixture corpus, round-trip every
domain through Rust, or exercise every actual wire producer/consumer. The
`actual_wire_domains` field is populated from schema filenames rather than
observed wire executions.

Retain the nine schemas and Rust types. Remove unsupported wire-conformance
claims and add only the focused round trips required below.

## Material finding 4 — the resident soak is useful but narrower than claimed

The 3,600-second run is retained as bounded evidence that one supervisor
remained resident while four control operations were accepted and observed
process replacement occurred. It does not by itself prove every direct-care
rejection, persisted idempotency, bridge-session transition, store recovery, or
display-recovery invariant.

Do not repeat the full hour unless the supervisor lifecycle is materially
redesigned. After the narrow correction, run a focused 900-second resident
regression that verifies the corrected message and recovery semantics.

## Material finding 5 — supply-chain work is not a Phase 01 blocker

The exact artifacts, lockfile, current SBOM, and source hashes are retained.
`cargo-deny` was unavailable and was not run. Automated advisory/license/bans/
source policy and formal legal review are deferred to the dedicated security,
resilience, pilot, and release phases.

Correct all labels so the current offline dependency policy is not called a
vulnerability scan or legal clearance.

# CODEX CONTINUATION DIRECTIVE

## 1. Mandatory synchronization

Continue only in the existing local ext4/NVMe secondary worktree.

```bash
git fetch origin
git status --short
git rev-parse HEAD
git rev-parse origin/main
git rev-parse origin/codex/p01-foundation-001
git log --oneline --decorate --graph -30
git merge --no-ff origin/main
```

Do not rebase, force-push, reset backward, rewrite published commits, create a
replacement branch/PR, merge PR #7, or close Issue #6.

The primary SSHFS worktree and its operator-owned root `.gitignore` and
`AGENTS.md` modifications remain protected. Do not read their modified contents
into evidence or commit, discard, reset, stash, copy, reformat, or otherwise
alter them.

Read this file and the live Notion Review 04 before changing source.

## 2. Required correction A — exhaustive typed injection protocol

Replace raw string fallthrough with one exhaustive typed injection command
shared by the supervisor control plane and producer. Unknown injection kinds
must be rejected by the supervisor before transport.

Required supported kinds:

- valid ordinary observation;
- valid safety candidate;
- duplicate safety candidate;
- replayed safety candidate;
- malformed frame;
- duplicate decoded key;
- unsupported schema major;
- unknown field;
- invalid UUID;
- invalid date-time;
- stale generation;
- invalid MAC;
- stale MAC after rotation;
- unauthorized sender attempt; and
- forbidden companion-state input.

The ordinary observation must traverse the ordinary path to `companion-core`.
It must not enter the care attempt journal or create a care transition.

Every safety kind must map to exactly one producer mutation. Add unit tests that
prove the exhaustive mapping and prove unknown input fails before transport.

## 3. Required correction B — truthful resident 3,000-message matrix

Run one resident supervisor through at least 3,000 actual messages across
retained seeds `17`, `23`, and `41`. The seeds must deterministically change
scenario order or message identity.

For every category define before execution:

- requested count;
- expected transport path;
- expected accepted/rejected/duplicate outcome;
- expected exact reason;
- whether the care attempt journal must increment; and
- whether the canonical candidate outcome must change.

The runner must assert:

1. valid safety messages are accepted exactly once;
2. every invalid safety category is rejected with its exact reason;
3. invalid safety accepted count is zero;
4. duplicate attempts increment the attempt journal but do not create a second
   canonical outcome;
5. idempotency survives a care restart;
6. ordinary observations reach `companion-core` and never enter care authority;
7. producer rotation changes generation, capability, channel, and pidfd-bound
   process state;
8. old generation, old MAC, and old endpoint inputs fail;
9. care-store fault prevents durable acceptance and health becomes degraded;
10. care recovers only after its store verifies; and
11. `care-core` remains alive after malformed and hostile input.

The committed result must expose per-category requested, accepted, rejected,
duplicate, outcome, and exact-reason counts. The validator must recompute all
accounting equations rather than trust a top-level `PASS`.

## 4. Required correction C — twelve-group minimum Phase 01 gate

Replace the false `37/37` result with these directly exercised acceptance
groups:

1. normal startup and generation-bound readiness for every required role;
2. restart and bounded backoff for each ordinary required role;
3. producer/care-pair replacement with generation, capability, channel, and
   pidfd state rotation;
4. care outage, explicit degraded coverage, and verified recovery;
5. care-store failure, prevented durable acceptance, and verified recovery;
6. companion absent and companion-store unavailable/corrupt while direct care
   remains independently observable;
7. full invalid safety-input matrix with `care-core` remaining alive;
8. duplicate/idempotency behavior across care restart;
9. exact SQLite identity plus actual integrity, incompatible migration
   rejection, checkpoint, backup, and fresh-restore equivalence through the
   existing persistence test path;
10. actual XDG unsafe-path and network-filesystem refusal through the path
    library, not a control acknowledgement;
11. same-process Godot bridge disconnect/restart/reconnect plus deterministic
    simulated topology loss/fallback/restore; and
12. clean shutdown, orphan cleanup, no checkout writes, and bounded
    process-attributed AF_INET/AF_INET6 census.

Each group must retain concrete observations. `accepted=true` or
`control_state_recorded` is not sufficient evidence of the underlying behavior.

Explicitly mark `DEFERRED` or `NOT RUN`, rather than `PASS`, for:

- repeated crash-loop stress beyond one bounded backoff/restart proof;
- physical monitor hot-unplug;
- broad SQLite VFS/power-cut/lifetime qualification;
- cargo-deny/advisory database analysis; and
- formal legal review.

## 5. Required correction D — focused contract gate

For each of the nine Phase 01 contract domains:

- retain one explicit valid JSON fixture;
- validate it with pinned Draft 2020-12 tooling;
- deserialize and reserialize it through the matching Rust type;
- validate the emitted JSON again;
- compare required/optional fields, constants, enums, bounds, formats,
  nullability, and unknown-field policy; and
- retain focused negative fixtures for missing required, unknown field, wrong
  type, unsupported major, format error, and bound error when applicable.

For direct-care and ordinary-observation contracts, exercise the actual producer
and consumer wire paths.

Remove `actual_wire_domains` or derive it only from recorded Rust wire
executions. Full combinatorial contract testing is deferred to the later
memory/evidence/security phases.

## 6. Required correction E — focused Godot acceptance

Retain the same-process headless reconnect direction, but make its result depend
on the Godot client's observed states rather than only bridge-state file updates
or a Python socket probe.

Required Phase 01 evidence:

1. one Godot process reports `connected`;
2. bridge stops and the same process reports `disconnected` or `degraded`;
3. replacement bridge starts and the same process reports `connected` again;
4. headless topology simulation proves target loss, safe fallback, restoration,
   and geometry clamping; and
5. one bounded target-host metadata probe verifies the window is assigned to the
   selected Openbox display and remains within its usable geometry, without
   screenshots or media capture.

Use Godot's socket `poll()` and explicit status handling before relying on
connection status. Physical hot-unplug remains deferred.

## 7. Required correction F — focused resident regression

Do not repeat the previous 3,600-second run unless core supervisor lifecycle
logic changes materially. Preserve it as bounded resident evidence.

After the correction passes locally, run one continuously resident 900-second
regression. During the same lifetime:

1. submit and verify an invalid safety candidate;
2. restart care and prove idempotency persists;
3. rotate the producer and prove generation, pidfd-bound process, channel, and
   authentication state changed;
4. prove old state is rejected and new state is accepted;
5. fail the care store and prove durable acceptance is prevented and coverage
   degrades;
6. clear the fault and prove recovery;
7. restart the bridge and prove the same Godot client reconnects; and
8. verify no checkout write and no observed process-owned AF_INET/AF_INET6
   socket.

The runner must fail on any resource-inspection error that affects its
conclusion.

## 8. Required correction G — semantic closeout validator

The validator must independently enforce:

- every result and fixture hash;
- Git ancestry;
- exact matrix equations;
- exact expected outcome and reason for every category;
- invalid accepted count equals zero;
- ordinary observations never enter care attempt/outcome counts;
- duplicate attempt and canonical-outcome equations;
- post-restart idempotency;
- all twelve real acceptance groups;
- Godot client-state transitions;
- 900-second regression invariants;
- explicit `NOT RUN`/`DEFERRED` state for non-required surfaces; and
- no circular consumption of generated validation output.

Retain the tamper-negative test.

## 9. Required correction H — supply-chain disposition

Preserve exact Rust, Godot, SQLite, Cargo lock, hash, license metadata, and the
current component inventory. Correct labels so the existing offline dependency
policy is not called a vulnerability scan or legal review.

Do not install `cargo-deny` solely for this closeout. Record advisory/license/
bans/source analysis as a required Phase 11 and release gate. Any known active
vulnerability discovered during normal work still requires immediate Architect
escalation.

## 10. Scope and publication

Continue on `codex/p01-foundation-001` and PR #7. Use one focused semantic
correction commit and at most one publication-reconciliation commit. Preserve
prior false or partial results as superseded evidence; do not erase history.

Update:

- the active task packet;
- `.agent/CURRENT.md` and `.agent/INDEX.md`;
- append-only ledgers with superseding entries;
- the Phase 01 Notion report and parent directive;
- PR #7 body and result comment; and
- Issue #6.

Leave PR #7 draft/open/unmerged and Issue #6 open for independent Architect
acceptance.

## 11. Acceptance boundary

Phase 01 will be accepted when the typed injection protocol, truthful
3,000-message matrix, twelve-group real acceptance gate, focused contract round
trips, Godot client-state reconnect/topology evidence, focused 900-second
regression, and semantic closeout validator all pass and agree with Notion and
GitHub.

No additional broad Phase 01 hardening is authorized. The next Architect action
after a passing result is to merge PR #7, archive Phase 01, and issue the complete
Roadmap Phase 02 embodiment directive.

## 12. Hard boundary

Do not add or claim:

- organism needs, drives, goals, autonomy, or temperament;
- autobiographical memory;
- learning or dreaming;
- production sprite embodiment;
- camera or microphone capture;
- STT, TTS, or model inference;
- biometrics, contacts, or notifications;
- spoken-help recognition or live escalation;
- medical capability;
- security certification;
- production reliability, lifetime durability, or SLA performance; or
- any Roadmap Phase 02–10 completion.

## 13. Required result

Return `CODEX RESULT — COMPANION-P01-FOUNDATION-001` with:

- exact branch, merge, implementation, reconciliation, and remote state;
- the fixed exhaustive injection mapping;
- exact per-category matrix equations and reasons;
- twelve-group evidence and all deferrals;
- contract Rust round trips and actual-wire evidence;
- Godot client state transitions and target-screen metadata evidence;
- 900-second regression result;
- validator and tamper-negative result;
- CI runs and artifacts;
- Notion/GitHub publication; and
- every `FAILED`, `BLOCKED`, `NOT RUN`, or `DEFERRED` surface.

Do not report `PASS` for behavior that was not directly exercised.
