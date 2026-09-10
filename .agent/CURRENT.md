# Current Project State

## Current stage

Planning Phase 02 remains the governing delivery roadmap.

Roadmap Phase 00 is complete at the implementation-opening boundary.
Architecture v1.0 remains adopted. Roadmap Phase 01 — Environment and
Engineering Foundation is active but **not accepted**.

PR #7 at `3fbc4284d2a0053034c0e5dea2cd97cb61e6330f` received Architect Review 02.
The implementation made substantial progress, but the phase still lacks an
evidence-bound resident control plane, contract-aligned direct-care
authentication, exact SQLite identity in CI, real Godot UDS integration, the
complete failure matrix, and the continuously resident injected soak.

## Active objective

Complete the final Phase 01 integration gate in the existing phase-sized PR:

1. observed supervisor readiness, liveness, health, restart/backoff,
   crash-loop, signal, and orphan behavior;
2. channel/generation/capability rotation with retained pidfd-equivalent
   binding and contract-aligned canonical HMAC verification;
3. durable care receipts and idempotency across restart with fail-closed store
   loss;
4. mandatory exact SQLite 3.53.4 source identity in local acceptance and CI;
5. semantic schema/type/wire compatibility and full positive/negative fixtures;
6. real Godot 4.7 UDS handshake, target-screen placement, geometry, reconnect,
   and display-loss fallback;
7. observed health/log/network state rather than hard-coded conclusions;
8. deterministic artifact bootstrap, real vulnerability/license checks,
   complete SBOM, provenance, and CI evidence;
9. one resident 3,000-message matrix, full failure/recovery matrix, and one
   continuously resident 3,600-second target-host soak with controlled failures.

Broad SQLite VFS/power-cut/lifetime qualification is deferred to later
resilience and release phases; it is not a Phase 01 blocker.

## Active directive and review

- Directive: `COMPANION-P01-FOUNDATION-001`
- Status: `ARCHITECT REVIEW 02 — CONTINUE; FINAL RESIDENT INTEGRATION GATE`
- Original Phase 01 routing baseline: `4171a02385b67f3e8d7ecbd6349d45c0bf1e0a8e`
- Architect Review 01 main: `3325d8a30406657c1c247fe126f7d3b4ce89de10`
- Reviewed continuation head: `3fbc4284d2a0053034c0e5dea2cd97cb61e6330f`
- Repository review: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/ARCHITECT_REVIEW_02.md`
- Notion review: https://app.notion.com/p/3d7833cb27ff810ba5abd1e1c4ee2237
- Notion directive: https://app.notion.com/p/3d7833cb27ff815ebe3ed1999f05beba
- Notion report: https://app.notion.com/p/3d7833cb27ff81c5b0eee3e6c98b54b5
- GitHub Issue #6: https://github.com/SketchOTP/companion/issues/6
- Pull request #7: https://github.com/SketchOTP/companion/pull/7
- Active packet: `.agent/tasks/active/COMPANION-P01-FOUNDATION-001/`
- Required branch: `codex/p01-foundation-001`
- Required publication: continue existing draft/unmerged PR #7
- Acceptance authority: ChatGPT AI Architect
- Roadmap Phase 02 and later: `CLOSED`
- Product capability claims: `PROHIBITED`

## Retained progress

Retain the Rust workspace, role-specific binaries, direct SQLite FFI and
prepared statements, corrected XDG defaults, initial resident supervisor and
control socket, private capability pipes, kernel-credential transport,
care-owned store, OS boot/monotonic utilities, nine schema/type names, Godot
project/display helper, bootstrap scripts, green CI history, and all preserved
negative evidence.

## Current material gaps

- Health marks registry entries healthy/ready without live readiness or liveness.
- Producer and care terminate after bounded cycles and are not rebuilt under the
  direct-care lifecycle.
- The producer pidfd is observed then dropped rather than retained as active
  generation authority.
- The safety schema/type requires `capability`, while the wire message sends
  `mac`.
- Custom HMAC-like code and string equality remain in the trust path.
- The 3,000-message driver uses three `--once` foundations and does not cover
  invalid/restart/recovery categories.
- The failure matrix does not exercise its named recovery properties.
- CI can fall back to host SQLite instead of exact 3.53.4.
- Contract drift checks test names rather than semantic compatibility.
- Godot and Rust use different bridge-state paths; no real handshake exists.
- CI vulnerability/license/SBOM evidence remains policy-only or incomplete.
- The required continuously resident injected 60-minute soak was not run.

## Mandatory Codex continuation

Codex cannot see operator–Architect chat. It must read the repository Review 02
and exact Notion Review 02, merge current `origin/main` normally into the
existing branch, preserve the protected primary worktree, complete the whole
phase gate in the same PR, update Notion/GitHub, and stop for independent
review.

## Protected operator work

The primary SSHFS worktree contains operator-owned uncommitted root
`.gitignore` and `AGENTS.md` changes. They remain outside this directive. Do
not read their modified contents into evidence, commit, discard, reset,
overwrite, stash, reformat, or reinterpret them.

## Scope boundary

No real organism, memory, learning, dreaming, production sprite body,
camera/microphone capture, STT/TTS, model inference, biometrics, real contacts,
notification delivery, spoken-help recognition, live escalation, medical
capability, security certification, production reliability, SLA, or Phase
02–10 capability may be added or claimed.

## Next review point

Codex completes the final resident integration gate in PR #7, publishes one
reconciled result with direct evidence, leaves PR #7 and Issue #6 open, and
stops for independent Architect acceptance.

## Review 01 continuation update — 2026-09-10

The continuation replaces the one-shot service entry point with a resident
`ops-supervisor` and explicit `--once` test mode, separate role binaries,
supervisor-backed health, direct SQLite ABI calls with prepared statements and
the Online Backup API, corrected XDG defaults with fail-closed placement, and
private capability delivery for the real direct-care socket. Three retained
seeds now drive 3,000 actual packet cycles through separate processes. The
remaining full failure/recovery injection, target-host Godot recovery, exact
3.53.4 host-library binding verification, and completed continuous 60-minute
injected soak remain tracked as unqualified until independently observed.

## Review 01 continuation recheck — 2026-09-10

The private exact SQLite 3.53.4 amalgamation build path is now exercised when
`COMPANION_SQLITE_SOURCE` is present; the resulting release binary statically
exposes SQLite 3.53.4 and has no SQLite dynamic dependency. The verification
script also starts a resident supervisor before querying the operator health
command, so the health result reflects live child state. The bounded verify
run completed successfully. Full injected one-hour soak, broad restart and
display-loss recovery, adversarial IPC, and VFS/power-loss coverage remain
unrun and continue to block phase acceptance.

## Publication re-fetch — 2026-09-10

The live Architecture Decision Ledger currently has 52 rows (31 Adopted,
19 Interim, 2 Rejected); the live Research Evidence Register has 55 rows
(42 Grade A, 11 Grade B, 2 Grade C, 0 Grade D). The branch and PR remain
unaccepted pending the explicitly unrun long soak and recovery matrices.

## Final publication reconciliation — 2026-09-10

The task branch is `codex/p01-foundation-001` at
`19eb169c26e10106004a910f3cce763b44c3c44a`, matching the remote branch.
Historical bounded soak observations remain retained, but the final status is
`PHASE 01 CANDIDATE — ARCHITECT REVIEW REQUIRED`: no continuous-resident
injected soak, broad process-replacement/adversarial IPC matrix, target-host
display-loss recovery, or complete SQLite VFS/power-loss matrix was executed.
Architecture v1.0 remains adopted, Roadmap Phase 02+ remain closed, and no
product capability or dependency was self-approved.

## CI ancestry correction — 2026-09-10

The final task-branch head is `4cfc1c512b2da6c7b25087cd35627cb7eb10bdda`,
matching the remote branch. The workflow now retains full Git history so the
accepted-qualification evidence validator can verify ancestry on CI; both
push and pull-request runs passed. Phase 01 remains a candidate pending the
continuous injected soak and recovery/fault gates listed below.
