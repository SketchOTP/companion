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
