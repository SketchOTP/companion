# Architect Review 03 — COMPANION-P01-FOUNDATION-001

## Verdict

`CONTINUE — PHASE 01 NOT ACCEPTED; ONE EVIDENCE-DRIVEN CLOSEOUT RUN REQUIRED`

- Reviewed PR: `#7`
- Reviewed branch: `codex/p01-foundation-001`
- Reviewed head: `a96a152386b76c7aa133c6f7b478be1ddecbf472`
- Required PR state: `OPEN / DRAFT / UNMERGED`
- GitHub Issue: `#6 — OPEN`
- Architecture v1.0: `ADOPTED / UNCHANGED`
- Roadmap Phase 01: `ACTIVE / NOT ACCEPTED`
- Roadmap Phase 02 and later: `CLOSED`
- Product capability: `NOT ESTABLISHED`
- Canonical Notion review: https://app.notion.com/p/3d7833cb27ff8107ae2ae0078ea57718

## Review scope

The Architect independently re-synchronized GitHub and Notion, inspected PR #7
at `a96a152386b76c7aa133c6f7b478be1ddecbf472`, reviewed the post-Review-02
implementation range, both final green CI runs, committed Phase 01 evidence,
the resident supervisor and control plane, direct-care authentication and
persistence, exact SQLite build, XDG policy, nine contracts, Godot UDS
integration, runtime health/network checks, integration and failure drivers,
the resident soak driver, bootstrap, dependency policy, and SBOM output.

Current primary documentation was rechecked for Godot 4.7 socket polling and
screen selection, Rust dependency advisory/license policy, and the limits of
automated license evidence.

## Verdict basis

The continuation materially advanced the project. Retain the exact SQLite
3.53.4 fail-closed build, direct FFI and prepared statements, RustCrypto HMAC,
schema/wire alignment, role-specific binaries, retained producer pidfd,
direct-care channel rebuilding, corrected XDG defaults, real UDS direction,
improved SBOM, resident process control, green CI, and the completed
3,600-second synthetic host soak.

Phase 01 still does not meet its accepted contract because the automated
evidence does not yet exercise several claimed properties. The current resident
matrix sends only valid candidates plus one duplicate; its seeds do not alter
behavior. The control plane still defers injection and reconnect. The failure
matrix omits required invalid-input, store, vault, crash-loop, stale-channel,
and display scenarios. The soak verifies command acceptance but not the
complete post-failure recovery invariants. Contract tests and supply-chain
checks remain materially incomplete. These are phase-foundation defects, not
later product features.

## Retained implementation progress

Preserve and build on:

1. Rust 1.98.1 workspace and role-specific binaries.
2. Exact Godot 4.7.2 and SQLite 3.53.4 identities.
3. Fail-closed exact SQLite source build and runtime source-ID check.
4. Direct SQLite FFI, prepared-statement direction, committed migration roots,
   integrity/checkpoint/backup functions.
5. RustCrypto `hmac` 0.12.1 with verification API and a versioned domain
   separator.
6. Aligned public safety-candidate fields `auth_scheme` and `mac`, with secret
   capability material outside the wire contract.
7. Retained producer pidfd, sequenced-packet direct-care transport, private
   capability pipes, generation rotation, and care-owned store.
8. Specification-correct XDG default direction and network-filesystem refusal.
9. Post-initialization readiness markers, resident control socket, process
   liveness checks, signal shutdown, and direct-pair reconstruction.
10. All nine schema files and Rust contract types.
11. Godot `StreamPeerUDS` direction, display-topology helper, geometry
    persistence, and bounded habitat shell.
12. Completed 3,600-second synthetic resident soak as bounded historical
    evidence.
13. Improved exact-source CI, versioned SBOM, green final CI runs, and preserved
    negative results.

These assets are substantial implementation progress. They are not Phase 01
acceptance by themselves.

## Material acceptance failures

### 1. The resident integration matrix covers only the happy path and one duplicate

`scripts/cycle_matrix.py` starts one supervisor in `--once` mode, sends valid
candidates, observes one duplicate, and exits. It does not use the resident
control plane to submit replayed, malformed, unsupported-version,
stale-generation, invalid-MAC, or same-user unauthorized inputs. It does not
restart companion or care, rotate the producer during the message stream,
fault a store, or verify recovery. The configured seeds are listed but the
producer discards the selected seed, so the seeds do not change deterministic
scenario ordering or message content.

The control plane currently returns `accepted=false` for `inject` and
`reconnect`. Those commands may not remain deferred in the final Phase 01 gate.

### 2. Direct-care rejection and audit behavior is not fail-closed enough

The public schema and Rust type now agree, and the HMAC implementation is
retained. However:

- raw packets are parsed before decoded duplicate-key rejection;
- malformed JSON can terminate `care-core` instead of producing a durable
  rejected receipt and continuing;
- `replay` is type-checked but not rejected as an invalid live candidate;
- `observed_at` is not validated against the complete date-time/freshness
  contract;
- a duplicate attempt is represented through a unique candidate row, so
  repeated attempts are not preserved as a separate append-only attempt
  history;
- the current direct-care smoke verifies accepted plus duplicate traffic with
  companion absent, not the adversarial and restart matrix required by the
  architecture.

Create a durable append-only attempt journal distinct from the idempotent
candidate outcome. Every syntactically processable accepted or rejected attempt
must be recorded before a response. Malformed frames that cannot yield a trusted
candidate ID must still produce a bounded audit entry without inventing an
identity.

### 3. Supervisor health is not yet a complete observed health model

Health now uses child process handles and readiness marker existence, but it
still does not obtain role-specific health acknowledgments, care-store
integrity/availability, receipt-journal availability, direct-channel test state,
or a live Godot session state. The `network` field is a configured policy
string, not a runtime observation. Readiness marker files are not
generation-bound in their content, and the ordinary-child replacement path can
remove a newly written marker after spawn.

Replace marker presence with a versioned readiness acknowledgment containing
role, PID, generation, boot ID, and initialization result, or bind marker
content and lifecycle equivalently. Delete stale readiness state before spawn.
Health must expose observed state and explicitly distinguish policy from runtime
census.

### 4. The failure matrix and soak do not prove their full recovery claims

The current failure matrix tests resident startup, companion restart, producer
rotation, care process failure/recovery, bridge child restart, and shutdown. It
does not test readiness timeout, startup failure, crash-loop transition,
companion store corruption, care-store loss, vault denial, stale
endpoint/capability rejection, malformed contracts, unsafe storage,
incompatible migration, backup/restore, actual Godot client reconnect, or
display loss/restoration.

The 3,600-second soak is retained, but its pass condition checks that four
control commands were accepted, not that each system invariant recovered. It
does not run a real Godot client/window, assert generation and capability change
after producer replacement, verify care coverage degradation then restoration,
confirm post-restart receipt durability, sample store integrity/checkpoints,
record bridge session state, record log volume, or fail on process-resource
inspection errors.

Run a new closeout soak after the implementation corrections. Preserve the
earlier run as evidence history.

### 5. Contract tests remain too shallow

The Draft 2020-12 runner creates one generated valid instance and tests only one
missing field and one unknown field for each schema. The Rust crosswalk uses
regular expressions and coarse types. It does not compare all required/optional
fields, constants, enums, numeric bounds, formats, nullability, or actual wire
round trips.

Add a committed fixture corpus and machine-verifiable semantic mapping for all
nine domains. Include wrong type, bounds, invalid UUID/date-time, unsupported
major, duplicate decoded key, malformed framing where applicable, and
canonical-profile failures. Enforce the project integer boundary explicitly
rather than accepting all `i64`/`u64` JSON integers.

### 6. Godot connection and display recovery remain incomplete

Godot now uses `StreamPeerUDS`, but the client does not visibly poll the socket
state before relying on `get_status()` and available bytes. The screen policy
calculates geometry for a target index but does not explicitly move the window
to that screen. Topology policy is not reapplied when the display set changes.

The headless smoke starts a bridge, runs a short Godot process, stops the bridge,
then launches another Godot process. It does not keep the same Godot process
alive through bridge loss and restart or verify reconnect and state transitions.
Target-screen placement, simulated display loss, fallback, and restoration
remain unrun.

Godot 4.7 documents that `StreamPeerSocket.poll()` updates socket state and that
`Window.current_screen`/DisplayServer screen APIs control window placement.
Implement and test those semantics directly.

### 7. Bootstrap, CI, vulnerability, license, SBOM, and evidence binding remain incomplete

CI now uses exact SQLite and Godot source/artifacts and passes its configured
checks. It still does not execute the failure matrix, Godot bridge reconnect
test, storage recovery matrix, contract fixture corpus, or evidence-bundle
validator. The current security check is an offline package-name policy, not an
advisory database or license-policy check. `cargo-deny` supports advisory,
license, ban, and source checks; automated license discovery still requires an
explicit evidence ceiling and does not replace legal analysis.

The bootstrap still assumes the old Phase 00 private cache exists rather than
fetching missing exact artifacts into deterministic cache paths.
`verify_artifacts.py` retains the prior random Godot extraction path and only
substring-checks a SQLite executable. Reconcile these scripts into one
deterministic fetch-or-verify workflow.

The SBOM is materially improved, but Phase 01 evidence must also account for the
exact SQLite C source, Godot artifact, and Rust toolchain; distinguish declared
from concluded licenses; validate the generated document; use a unique
reproducible namespace; and publish a sanitized CI artifact.

# Final phase-closeout directive

This is one final phase-sized closeout run in the existing PR. Do not split it
into micro-directives. Do not return another partial result while the complete
gate remains feasible.

## A. Complete the resident control plane and observed health

- Implement versioned control commands for health, valid/invalid packet
  injection, controlled role failure, role restart, producer rotation, bridge
  disconnect/reconnect, test topology change, test store fault, and shutdown.
- Derive health from live process handles plus generation-bound
  post-initialization readiness acknowledgments.
- Verify role-specific store, channel, care receipt, and bridge-session health.
- Separate configured network policy from observed runtime socket census.
- Eliminate stale readiness marker races.
- Enforce bounded restart/backoff and observable crash-loop transitions for
  every required role.
- Preserve signal shutdown, orphan cleanup, and direct-pair atomic rebuilding.

## B. Make direct-care rejection, durability, and attack handling fail closed

- Reject decoded duplicate keys before ordinary deserialization can erase them.
- Apply the actual schema/typed contract to every packet.
- Reject replay, unsupported major, malformed frame, invalid UUID/time, stale
  generation, invalid/stale MAC, unknown fields, and unauthorized sender
  without terminating the care process.
- Persist an append-only receipt-attempt/audit row for every handled attempt,
  separate from the idempotent candidate outcome.
- Preserve idempotency across care restart.
- Make care-store loss visibly degrade coverage and reject durable acceptance.
- Port the accepted same-user attack and descriptor/capability census into the
  actual Phase 01 implementation tests.
- Verify stale channel and stale capability rejection after producer and care
  replacement.

## C. Build one real resident integration matrix

Drive one continuously resident supervisor through at least 3,000 actual
messages.

The retained seeds must deterministically alter scenario ordering, IDs, or
payload fixtures. Include measured counts for:

- valid ordinary observations;
- valid safety candidates;
- duplicates;
- replay attempts;
- malformed frames;
- unsupported schemas;
- stale generations;
- invalid and stale MACs;
- unauthorized sender attempts;
- producer replacement;
- care restart;
- companion restart;
- persisted idempotency;
- care-store failure and recovery;
- companion absence and corrupt-store behavior.

Every expected count and state transition must be asserted. No generated-label
counter or `--once` happy-path batch qualifies.

## D. Complete the Phase 01 failure/recovery matrix

Exercise and assert:

- startup failure and readiness timeout;
- bounded backoff and crash-loop state;
- restart of every required role;
- companion absence, store unavailable, and store corruption;
- care outage, care-store unavailable, degraded coverage, and recovery;
- vault outage and denied protected operation;
- producer replacement with generation/capability/channel rotation;
- stale endpoint and stale capability rejection;
- actual Godot client connection, bridge failure, bridge replacement, and
  client reconnect;
- simulated display loss, safe fallback, restoration, and geometry recovery;
- malformed contract and framing;
- unsafe storage refusal;
- incompatible migration;
- integrity, checkpoint, backup, and fresh restore;
- supervisor shutdown and orphan cleanup.

Every required scenario must fail the runner when its expected outcome is
absent.

## E. Complete contract and canonical-profile conformance

- Commit explicit valid and negative fixtures for all nine contract domains.
- Compare schema and Rust fields, requiredness, constants, enums, formats,
  bounds, nullability, and unknown-field policy.
- Round-trip each valid fixture through Rust.
- Exercise actual wire serialization for ordinary observation, safety
  candidate, care receipt, readiness, health, embodiment intent/result, vault
  decision, and backup manifest.
- Reject duplicate decoded keys, noncanonical numbers, out-of-profile integers,
  malformed framing, invalid date-time/UUID, and unsupported schema majors.
- Bind direct-care MAC input to canonical public fields and the versioned domain
  separator.

## F. Complete Godot UDS, target-screen, and recovery behavior

- Call socket polling as required by the Godot 4.7 socket state model.
- Maintain one Godot process through bridge connect, loss, bridge restart, and
  reconnect.
- Explicitly set the current screen for the selected output.
- Persist and restore output identity/index, position, and size.
- Reapply policy when display topology changes.
- Add deterministic headless topology loss/restore tests.
- Run a bounded target-host Openbox placement/recovery test without screenshots
  or media capture.
- Report actual bridge and habitat state through supervisor health.

## G. Complete deterministic bootstrap, supply-chain policy, SBOM, and CI evidence

- Create one idempotent fetch-or-verify artifact workflow for exact Rust, Godot,
  and SQLite inputs at deterministic private cache paths.
- Remove stale random-path assumptions from artifact verification.
- Pin and run one current `cargo-deny` configuration covering advisories,
  licenses, bans, and sources, or use an equivalently maintained locked toolset
  with the same coverage.
- Record the limitations of automated license evidence; full legal counsel
  review remains outside Phase 01.
- Generate and validate a complete SPDX or CycloneDX document that includes
  Rust crates, SQLite source, Godot artifact, and Rust toolchain with exact
  identities and relationships.
- Run the full contract, resident integration, failure, storage recovery, Godot
  UDS, exact artifact, qualification regression, vulnerability/license, SBOM,
  secret, and forbidden-data gates in CI where host-independent.
- Upload concise sanitized CI evidence artifacts.
- Add a committed Phase 01 closeout manifest that binds commands, final
  implementation commit, fixture hashes, result hashes, CI run IDs, host-soak
  result hash, evidence ceilings, and known deferrals.
- Add a fail-closed validator and a tamper-negative test for the closeout
  evidence bundle.

## H. Rerun the continuously resident target-host soak after corrections

Run one supervisor for at least 3,600 seconds and keep one Godot client active
where the target-host test permits.

During the same lifetime:

1. fail and recover `companion-core`;
2. replace the producer and verify generation, capability, channel, and pidfd
   state changed;
3. fail and restart `godot-bridge`, verifying the existing Godot client
   reconnects;
4. fail and recover `care-core`, verifying degraded coverage and restoration;
5. exercise at least one rejected invalid safety candidate before and after
   recovery.

Observe and bind:

- supervisor and child PIDs/generations/states;
- readiness and recovery deadlines;
- CPU and RSS with no unaccounted sampling errors;
- restart and crash-loop counters;
- store identity, integrity, schema, checkpoint, and receipt-journal
  availability;
- direct-care generation and pidfd liveness;
- bridge and habitat connection state;
- log count/volume and privacy scan;
- complete runtime socket census with explicit coverage limits;
- checkout and SSHFS write comparison;
- every degradation and recovery.

Preserve the previous soak as historical bounded evidence. The new soak must
exit nonzero unless every required invariant is demonstrated.

## Explicit deferrals beyond Phase 01

The following are not Phase 01 blockers and must remain scheduled for later
resilience, pilot, or release gates:

- broad SQLite VFS `xWrite`, `xTruncate`, shared-memory, compound-fault,
  realistic power-cut, lifetime, and endurance qualification;
- formal legal counsel review;
- production security certification and claims against root, kernel,
  complete-account compromise, or a fully compromised authorized producer;
- production reliability, availability, lifetime, and SLA evidence;
- organism, memory, learning, dreaming, production embodiment, media, speech,
  vision, biometrics, notifications, and qualified caregiving behavior.

## Acceptance criteria

Phase 01 passes only when:

1. The control plane implements every required test command and does not return
   deferred placeholders.
2. Health and readiness are generation-bound observations, not stale marker
   presence or registry assertions.
3. Every required role has bounded restart/backoff/crash-loop behavior and
   clean shutdown/orphan cleanup.
4. Direct-care packet validation is schema-aligned, canonical, duplicate-key
   safe, replay aware, and fail closed.
5. Accepted and rejected attempts are durably auditable; candidate idempotency
   survives care restart.
6. Care-store failure degrades coverage and prevents durable acceptance.
7. Producer/care replacement revokes old channel, generation, capability, and
   pidfd state.
8. The actual same-user attack and descriptor/capability matrix passes within
   the documented threat ceiling.
9. Exact SQLite 3.53.4 identity, committed migrations, prepared statements,
   integrity, checkpoint, backup, and restore remain passing.
10. All nine contracts pass explicit positive, negative, Rust round-trip,
    semantic drift, and actual-wire tests.
11. One resident system processes at least 3,000 messages across the complete
    valid/invalid/restart/recovery category matrix.
12. The complete Phase 01 failure/recovery matrix passes.
13. One Godot process proves UDS connect, disconnect, bridge restart,
    reconnect, target-screen selection, geometry restoration, simulated display
    loss, and safe fallback.
14. A bounded target-host Openbox placement/recovery test passes without media
    capture.
15. The 3,600-second corrected resident soak proves the four required failures
    and complete recovery invariants.
16. Resource, log, store, channel, network, and checkout-write observations are
    complete enough for every asserted conclusion.
17. Bootstrap can fetch or verify exact artifacts without undocumented prior
    cache layout.
18. Locked advisory, license, ban, and source checks pass with explicit evidence
    ceilings.
19. A validated complete component inventory and tamper-detecting closeout
    evidence bundle are published.
20. CI, host evidence, Notion, PR #7, Issue #6, commits, and current Authority
    state agree.
21. No Phase 02–10 capability or prohibited product claim is introduced.

## Publication rules

Continue only on `codex/p01-foundation-001`, PR #7, and Issue #6. Merge current
`origin/main` normally. Do not rebase, force-push, create a replacement PR,
merge PR #7, close Issue #6, or modify the protected primary worktree.

Use coherent subsystem commits. Do not return after individual commits. Return
only after the complete phase passes or one genuine stop-condition blocker is
demonstrated with attempted alternatives and exact evidence.

Update all active task records, `.agent/CURRENT.md`, `.agent/INDEX.md`,
append-only ledgers, the Notion coder report and parent directive, PR #7, and
Issue #6. Re-fetch mutable records, leave PR and issue open, and stop for
independent Architect review.

## Required Codex handoff

Return one complete `CODEX RESULT — COMPANION-P01-FOUNDATION-001` with exact
commits, changed paths, control-plane commands, child-state evidence,
direct-care accepted/rejected category counts, attack results, exact SQLite
identity, contract fixture coverage, Godot reconnect/display results, bootstrap
and supply-chain tool versions, SBOM/component hashes, CI run IDs/artifacts,
closeout-manifest validation and tamper-negative result, failure matrix,
corrected soak timestamps/resources/injections/recoveries, every non-pass,
Notion publication, PR/Issue state, and remote equality.

Explicitly confirm that Architecture v1.0 remains adopted, Phase 02 and product
implementation remain closed, and no security, safety, medical, reliability,
lifetime, or SLA capability is claimed.
