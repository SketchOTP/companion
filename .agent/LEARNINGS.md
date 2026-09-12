# Durable Learnings

Historical entries are append-only after adoption.

## COMPANION-L001 — Repository bootstrap predates Authority installation

### Learning

GitHub `SketchOTP/companion` began on `main` at `b7266b5806ef0612a14d2d6b7d324841070625ac` with only `.gitignore` and an Apache-2.0 `LICENSE`; no product source existed.

### Why it matters

Future agents must preserve that history and must not infer a language, architecture, or dependency from the Python-oriented bootstrap ignore file.

### Recheck trigger

Recheck the remote and working tree at every substantial directive.

## COMPANION-L002 — Repository authorization is governance-only

### Learning

The operator explicitly authorized the named GitHub repository and Authority 3.0 setup on 2026-09-08. This supersedes the earlier "no repository exists or is authorized" status only enough to host governance; it does not satisfy or waive the Research Phase 01 implementation gates.

### Why it matters

Repository existence must not be mistaken for authorization to write product code, add dependencies, create CI, or begin experiments.

### Recheck trigger

A new operator/Architect ruling that explicitly opens an implementation, experiment, dependency, CI, or deployment gate.

## COMPANION-L003 — Prior projects are not donors

### Learning

This project is independent ground zero. Prior companion, lifeform, monitoring, and assistant projects are not predecessors, donors, baselines, constraints, or default sources of code, design, models, schemas, tests, terminology, or decisions.

### Why it matters

Reusable governance procedure may be installed from the canonical Authority package, but project substance requires fresh evidence and explicit adoption through this project's Notion decision process.

### Recheck trigger

Any proposed reuse, migration, import, or comparison to a prior project.

## COMPANION-L004 — Identifier coverage is not semantic traceability

### Learning

A document can contain every required RQ, ADR, risk, pillar, and phase identifier while still mapping those identifiers to the wrong meaning. Structural presence, counts, JSON validity, and reference closure do not prove that a relationship is substantively correct.

### Why it matters

Future architecture, risk, and requirement traceability must verify exact ID-title-status pairs and manually review whether each cited record actually supports the statement. Automated crosswalks are supporting evidence, not a substitute for source-aware review.

### Recheck trigger

Every directive that creates or materially changes requirement, decision, risk, evidence, or roadmap traceability.

## COMPANION-L005 — Environment metadata does not qualify the companion workload

### Learning

The iteration-one host exposes ample general-purpose resources and accelerated OpenGL 4.6, but labels such as CPU model, RAM amount, GPU model, VRAM, and generic Godot requirements do not prove concurrent rendering, perception, speech, memory, model, or safety performance.

### Why it matters

Architecture and model sizing must be based on bounded integrated measurements with explicit latency, resource, thermal, power, and degradation criteria. Generic specifications only preserve options.

### Recheck trigger

Every renderer, model, camera mode, audio path, process-placement, and resource-budget decision.

## COMPANION-L006 — Source, runtime state, and backup need separate storage domains

### Learning

The Git repository is on network-backed SSHFS while the host provides local ext4/NVMe storage. These have different latency, availability, locking, and failure semantics.

### Why it matters

Canonical organism state, memory, caches, audit data, and recovery material must not inherit repository-volume assumptions. Source transport, runtime persistence, model cache, export, and backup require separate explicit policies.

### Recheck trigger

Architecture v1.0 storage design, persistence selection, backup/export planning, and any environment migration.

## COMPANION-L007 — Privacy filtering must begin at collection

### Learning

A hardware serial can appear in otherwise useful camera or audio metadata before a post-processing filter runs. In `COMPANION-P00-ENV-001` the value was immediately discarded and never entered durable artifacts, but the exposure shows that redaction after broad collection is weaker than field-limited collection.

### Why it matters

Future probes and runtime telemetry should use source-level field allowlists, bounded parsers, pre-reviewed command forms, and data minimization before persistence. Post-processing redaction is a secondary defense.

### Recheck trigger

Every machine inventory, sensor diagnostic, support bundle, telemetry design, biometric flow, and privacy review.

## COMPANION-L008 — Isolate by consequence, not by conceptual noun

### Learning

The Companion requires hard process boundaries around caregiving authority, raw sensors, models, rendering, secrets, and external transports, but splitting every tightly coupled organism and memory concept into an independent service would introduce distributed state reconciliation before evidence justifies it.

### Why it matters

A cohesive transactional companion truth owner plus consequence-driven edge isolation preserves deterministic personal continuity and testability while retaining future split seams.

### Recheck trigger

Measured resource isolation, privilege, independent upgrade/restart, database contention, second-device, or multi-owner evidence that makes a further split necessary.

## COMPANION-L009 — Persistence version is a safety and continuity input

### Learning

An embedded database's broad reputation or API is insufficient. Current SQLite documentation records a rare 2026 WAL-reset corruption issue across many releases and requires a fixed exact version/backport for the proposed multi-connection WAL use.

### Why it matters

Persistence selection must capture the exact embedded library, compile options, filesystem semantics, writer topology, checkpoint behavior, and crash/backup/restore evidence. The host binding and SSHFS checkout cannot be accepted by assumption.

### Recheck trigger

Every persistence shortlist, runtime/toolchain lock, database upgrade, writer-topology change, or migration/backup design.

## COMPANION-L010 — Safety independence requires independent ingress and persistence

### Learning

A separate care process is not architecturally independent if its qualifying inputs must be validated, forwarded, queued, or persisted by the companion authority. Independence requires an authenticated producer-to-care path, a care-owned receipt journal, and explicit common-mode input degradation.

### Why it matters

Companion failure, compromise, mood, memory, generated language, dreams, animation, or database availability must be unable to suppress or manufacture a care transition. Shared source identifiers are useful for reconciliation but cannot create shared mutable truth.

### Recheck trigger

Every sensor/speech topology, care scenario, queue, IPC authorization, persistence, degradation, and integration test design.

## COMPANION-L011 — Deterministic schemas require canonical bytes and reboot epochs

### Learning

JSON Schema constrains structure but does not make JSON bytes invariant. Repeatable hashes/replay require a pinned canonical encoding/digest scope and canonical numeric rules; monotonic time also requires a boot identifier and cannot order records across reboots by itself.

### Why it matters

Cross-language serialization, Unicode/numeric edge cases, signatures, wall-clock steps, and reboot resets otherwise create divergent history despite schema-valid content. Owner sequence and causation remain the durable cross-boot order.

### Recheck trigger

Every event schema, parser/canonicalizer, hash/signature, language/toolchain, migration, replay, clock, and cross-boot test decision.

## COMPANION-L012 — Numeric version floors can admit withdrawn releases

### Learning

An eligibility rule expressed only as a minimum version can admit a later withdrawn or incompatible release. SQLite 3.52.0 demonstrates that security/correctness fixes and compatibility/support disposition must be evaluated per exact build.

### Why it matters

Persistence approval requires exact source identity, binding, compile options, support/withdrawal/vulnerability status, topology, and reproduced recovery behavior—not lexical or numeric version comparison.

### Recheck trigger

Every dependency/toolchain/runtime upgrade and every exact-build qualification record.

## COMPANION-L013 — Same-UID pathname sockets are not a producer-authorization boundary

### Learning

A private mode-0600 AF_UNIX pathname socket accepted a structurally valid synthetic message from an unrelated same-user process. UID equality and message-declared producer identity therefore do not satisfy the adopted direct-care safety-ingress gate.

### Why it matters

Direct care ingress needs a supervisor-controlled private channel plus generation-bound capability/process controls, and must be target-tested before implementation.

### Recheck trigger

Any change to supervisor, OS identity, confinement, producer lifecycle, socket topology, or care authorization contract.

## COMPANION-L014 — Exact SQLite identity is necessary but not sufficient

### Learning

SQLite 3.53.4 source identity and bounded local WAL/backup tests can be reproduced, while deterministic kill placement inside commit/checkpoint remains unqualified without an intrusive fault mechanism.

### Why it matters

An exact release and several green tests cannot silently become persistence adoption; incomplete fault coverage is a material blocker rather than a tolerated gap.

### Recheck trigger

Before any persistence adoption, binding selection, fault-VFS authorization, or change in SQLite release/build/topology.

## COMPANION-L015 — Qualification claims require actual process boundaries

### Learning

Calling a care function from a single process does not qualify producer-to-care
IPC, descriptor ownership, kernel credentials, generation binding, restart
revocation, or same-user isolation. The correction required independent
supervisor, producer, care, and sibling processes exchanging real packets.

### Why it matters

Process identity and channel controls are properties of the live kernel/process
graph, not of an in-process mock. Exact syscall errors such as `pidfd_getfd`
`EPERM` must be retained as observed results rather than normalized to pass.

### Recheck trigger

Every direct-care ingress, supervisor, capability, descriptor, restart, or
same-user threat qualification.

## COMPANION-L016 — Canonicalization requires an oracle and edge vectors

### Learning

Sorted JSON output is not RFC 8785. Decoded duplicate names, UTF-16 property
ordering, non-BMP keys, number rendering, Unicode validity, and control
escaping require a maintained implementation or independently validated oracle
and retained vectors.

### Why it matters

Cross-language digest/replay agreement can be false on ASCII-only fixtures even
when implementations diverge on canonical bytes.

### Recheck trigger

Every event digest, schema/parser, language comparison, replay, or signature
decision.

## COMPANION-L017 — Storage fault evidence must prove post-reopen state

### Learning

Serial reader checks, guard errors, and row-count-only restores cannot qualify
SQLite atomicity. The corrected matrix overlaps independent readers with a
writer, rejects incompatible migration before mutation, compares schema and
ordered logical digests, and reopens after deterministic VFS failures.

### Why it matters

Returned errors alone do not prove whether a transaction partially committed;
integrity and whole-or-absent logical state after reopen are required.

### Recheck trigger

Every exact database/build/topology, migration, backup/restore, disk/I/O fault,
or crash-consistency decision.

## COMPANION-L — Committed evidence must be executable and fail closed

Qualification summaries are insufficient when a green process exit can coexist
with a false security, parity, or atomicity boolean. Commit sanitized result
records, provenance, and a validator whose exit status is derived from every
acceptance assertion. Preserve failed historical attempts, but make the
current result unambiguous and machine-checkable.

## COMPANION-L-001 — Evidence binding must be independent of self-attestation

Result files are not evidence merely because a validator reads their booleans.
Recompute manifest and fixture hashes, bind the checked-out evidence commit
through Git ancestry, generate validation output rather than consuming it, and
retain an explicit tamper-negative test. Date-only precision is more honest
than fabricated midnight timestamps when exact execution times were not kept.

## COMPANION-L-002 — Summaries preserve measured versus inspected facts

Process-boundary summaries label runtime and kernel observations separately from
code-inspected ownership facts. SQLite summaries derive claims from independent
before/after state and fixed expected counts rather than observed values or
hand-curated booleans.

## COMPANION-L-003 — Phase-sized foundations still preserve explicit ceilings

A runnable engineering foundation can be delivered without smuggling product
behavior across roadmap gates. Synthetic care packets, neutral Godot status,
development stores and deterministic cycle matrices are E3 engineering
evidence only; visible/long-duration and remote CI checks remain separately
identified when not executed.

## COMPANION-L-004 — Phase 01 evidence must distinguish bounded soak from residency

A phase-sized foundation can provide executable service shells, direct
synthetic care transport, isolated development stores, a neutral Godot habitat,
and deterministic message evidence without becoming a living companion. The
60-minute soak used repeated bounded supervisor invocations at a fixed interval;
its timestamps and failures are evidence of that harness only, not proof of a
continuous resident runtime, production reliability, safety efficacy, or SLA.

### Recheck trigger

Any future claim about continuous operation, restart durability, service
supervision, reliability, or production readiness.
## 2026-09-10 — Resident foundation continuation

- A resident supervisor must expose a stable control socket and keep child
  lifecycle state in memory; one-shot invocations cannot support health or soak
  claims.
- Capability bytes can be delivered through a private inherited pipe while the
  endpoint itself remains close-on-exec until the intended child handoff.
- Same-user care authentication requires kernel credentials and a MAC; a
  declared producer field or environment secret is not an authority source.
- Direct SQLite ABI binding removes PATH/subprocess ambiguity, but exact source
  identity still needs host-level verification before release claims.
- XDG defaults and missing runtime bases must fail closed; `/tmp` is never a
  canonical-state fallback.

## 2026-09-10 — Architect Review 02 integration hardening

- Readiness is only meaningful when emitted after store/channel initialization
  and cross-checked against a live child handle; a registry boolean is not
  health evidence.
- Direct-care replacement must close the old socketpair and rotate both the
  generation and capability; retaining a pidfd makes liveness observable but
  does not expand the documented threat ceiling.
- Exact SQLite source hashing in `build.rs` prevents a host-library fallback
  from silently entering acceptance builds; runtime version/source-id/options
  must still be recorded.
- Child dumpability hardening can make `/proc` census unavailable to a same
  user; that is a real observability failure to report, not permission to
  downgrade the security setting.

## 2026-09-10 — Evidence correction

- A hardened child may legitimately deny `/proc/<pid>/fd` traversal. Preserve
  that denial as an observation and use process-attributed `ss` output for the
  no-egress check; never reinterpret inaccessible descriptors as zero sockets.
- Resident producer and care roles must emit readiness only after their packet
  and store initialization, then remain alive until an explicit supervisor
  shutdown so health and recovery probes observe a real resident foundation.

## 2026-09-10 — Soak startup-race correction

- A long-running harness must wait for the supervisor control endpoint before
  its first health request; otherwise a legitimate bind race becomes a false
  soak failure. Preserve the failed run and rerun the full duration after the
  fix rather than relabeling it.
- The corrected resident run completed 3,600 seconds with 60 samples and four
  injections without claiming production reliability.

## 2026-09-10 — CI readiness race

- Local and pull-request timing can mask a supervisor startup race that fails
  a push workflow. Runtime checkers must wait for the control endpoint and
  retain a nonzero result when readiness is never observed.

- Fresh push run `34488896386` and pull-request run `34488902059` passed after
  the readiness correction, confirming the harness fix without expanding any
  product or security claim.

## 2026-09-10 — Review 03 evidence binding

- A resident matrix must make seeds alter deterministic category ordering and
  must assert every durable attempt, not only command acceptance.
- Readiness is an observed, role-bound acknowledgement; marker presence alone
  is insufficient. Runtime policy fields (such as network deny-by-default)
  must remain distinct from process-attributed census observations.
- Phase closeout summaries require committed hashes, fixture binding, Git
  ancestry, deterministic generation, and a tamper-negative validator. A
  generated validation file is output, never evidence input.

- A resident soak is only a clean target-host observation when the
  checkout-write sentinel remains false for the entire interval. Sanitization
must accept count-only runner summaries as well as detailed sample arrays.

## 2026-09-10 — Architect Review 04 evidence semantics

- Injection categories must be an exhaustive typed enum with a one-to-one
  mutation mapping; unknown values must fail before transport and no default
  branch may silently create a valid packet.
- A resident message matrix must assert requested/applied/status/reason and
  derive care-attempt, outcome, ordinary-event, and invalid-acceptance counts;
  category presence alone is not evidence.
- Scenario evidence is credible only when the named behavior is induced and a
  before/after invariant is observed. Control acknowledgments are not storage,
  display, migration, or recovery results.
- Result summaries need committed hashes, fixture identity, ancestry, and a
  validator that emits (rather than consumes) its own validation output.

- Phase 02 sprite work is safest when authored source parameters, full-canvas
  raster output, landmarks, clip metadata, and pack manifests are generated by
  one deterministic tool and checked independently for alpha, bounds, root
  drift, uniqueness, and checksums.
- Automated animation and headless Godot evidence cannot substitute for
  operator review of identity, diagonal construction, motion quality, or
  target-display behavior.

- ZIP archives are not reproducible by default: filesystem timestamps and
  platform metadata must be pinned before a clean-room pack hash can be used as
evidence. The Phase 02 pack now pins both and rebuilds byte-identically.

- Review derivatives must be checked visually, not only by path existence:
  corrected filenames restored the complete four-view diagonal sheet.
# Phase 02 correction learning — 2026-09-11

Direction must be a track-selection key, never a temporal frame index. Binding
construction to the exact native reference requires hashing the source before
each export and retaining the native file unchanged. Declared atlas gutters do
not count: trim rectangles, edge extrusion, reserved pixels, and reconstruction
metadata must be measured in the generated page. Generated frame/atlas blobs
belong in workflow artifacts; selected review derivatives and source manifests
belong in Git.

## 2026-09-11 — Canon before scale

Approved raster references are art direction, not an editable rig. Lock source
precedence, construction pivots, and a small real motion language before
generating direction or family counts. A direction is a selection axis; a
temporal track is the ordered drawings inside one facing. When a candidate
rasterizer is unavailable, record that limitation instead of silently adopting
another tool.

## 2026-09-11 — R03 motion semantics

An editable body requires independent part IDs, pivots, and replacement policy;
a flattened reference or global band warp cannot establish articulation. Keep
direction as a track-selection key, use 24 FPS with integer relative weights,
and derive contact evidence from rendered pixels as well as sidecars. A
headless dummy renderer may support actual `AnimatedSprite2D` signal playback
while exposing no readable SubViewport texture; record the deterministic raster
mirror limitation rather than claiming a Godot raster bake.

## 2026-09-11 — Hosted contract gates must cover new fixtures

Adding a new schema can break inherited gates when their fixture maps are
explicit. The v2 temporal-track fixture must be included in the shared
contract closeout; hosted Phase 02 and Phase 01 runs are the regression proof.

## 2026-09-11 — Immutable art authority beats procedural repair

Identity fidelity cannot be recovered by adding more metadata to a coding-
agent renderer. Keep Architect-authored full-frame PNG bytes immutable, make
approval an explicit manifest state, separate content-addressed sources from
derivatives, and acknowledge playback only after frame zero is actually
selected, loaded, and observed. Synthetic geometry is useful for protocol
tests precisely because it cannot be mistaken for production character art.

## 2026-09-11 — Scope private-data gates to the changed evidence surface

A repository-wide literal scan can fail on preserved historical evidence even
when the new intake/runtime boundary contains no private identifier. Keep the
gate fail-closed on every R04 source, result, workflow, and active-state file,
remove new hard-coded private paths, and preserve older records rather than
rewriting them to satisfy a new scope. Hosted run `34655914553` exposed this
distinction; `34656090767` verified the corrected gate.

## 2026-09-11 — Bind authored source before derivative runtime

An authored-frame landing contract must not require runtime content addresses,
must represent changing facing and occluded landmarks explicitly, and must
reject ambiguous reuse. Keep source bytes immutable and derive CAS/runtime
relationships only during staged intake. Synthetic geometry can test these
boundaries, but cannot stand in for Architect-authored character pixels.

## 2026-09-12 — Evidence bundle must be published after implementation

Bind provenance to the committed implementation ancestor, then regenerate and
commit sanitized results separately. This keeps source/runtime checks
reproducible while preserving the operator-owned Graft boundary and preventing
generated validation output from becoming its own authority.

## 2026-09-12 — Executable request must be tuple-keyed

When one family legitimately has several facing roles, family-only dictionaries
silently collapse requirements. Keep the human request and executable profile
as one tuple-keyed table, and make positive calibration packs cover every role,
endpoint, event, and reuse rule before any Architect-authored pixels land.

## 2026-09-12 — R04-C02 exact-tool rerun

The pinned Rust and Godot gates can be executed from private existing/tool
cache paths without modifying the host. Godot must run under a real X display
(Xvfb is sufficient for this synthetic boundary) for
`RenderingServer.frame_post_draw`; headless process-frame completion is not a
render-commit observation. The complete pack and result hashes must be
regenerated after semantic fixture changes.

## 2026-09-12 — Godot evidence must have one pass definition

Separate Godot invocations with different stdout/stderr policies can disagree
without identifying the cause. A canonical runner must retain application
stdout, stderr, `--log-file`, and Xvfb wrapper diagnostics independently, hash
each channel, preserve exact `ERROR:` lines, and be the only classifier used by
workflow and evidence generation. Wrapper warnings are diagnostic context, not
Godot errors; unknown Godot errors remain failures.

## 2026-09-12 — C03 hosted ALSA parity

A hosted Godot `ERROR:` can be a real backend initialization attempt even when
Godot later falls back successfully. Preserve the exact line and channel
context first. For non-audio qualification, selecting the documented Dummy
driver is an explicit environment boundary, not a whitelist; the application
classifier must continue to fail on all remaining Godot error channels.

## 2026-09-12 — Socket availability is not readiness

A control endpoint can exist while child initialization and care coverage are
still converging. A deterministic qualification gate must use the explicit
health contract, monotonic bounded polling, and a stability requirement across
separated samples. Synthetic delayed, never-ready, and early-exit cases should
exercise the waiter itself so a one-shot race cannot be mistaken for a service
regression.

## 2026-09-12 — Same-head stability closes the readiness race

A deterministic readiness predicate must survive repeated hosted execution on
one immutable SHA. The initial run plus two same-head reruns all passed after
the probe required two separated complete-health samples. The Phase 02 result
was rechecked on that same SHA; this supports the handoff status only and does
not promote any Phase 02 or production claim.

## 2026-09-12 — Candidate sprite generation needs truthful selection metadata

Reference conditioning can preserve a recognizable identity while still
producing unusable sheet cells: encoded checkerboards, reversed facing, stray
marks, and stance/contact variation all occurred. Rejecting those sources before
intake, generating a dedicated right-facing profile, and deriving contact spans
from selected pixels avoided laundering art defects into metadata. Reciprocal
orientation can truthfully reuse the same four poses in reverse, but occurrence
and unique-source counts must remain separate.

## 2026-09-12 — Accepting a control socket needs scheduling-safe framing

A nonblocking listener followed by a short blocking read can accept a client
before that client is scheduled to send. Ignoring the timeout converts the
absence of bytes into the wrong command and closes the peer, producing an
intermittent client-side broken pipe. Bound both frame size and wait time,
require explicit framing, and treat empty, timed-out, oversized, or malformed
requests as errors rather than health fallbacks.
