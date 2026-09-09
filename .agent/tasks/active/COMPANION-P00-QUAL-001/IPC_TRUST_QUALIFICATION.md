# Direct-Care IPC Trust Qualification

## Correction cycle 01 — real process-boundary result (2026-09-09)

Status: `CORRECTION SUBMITTED — E3 TARGET-TESTED; ARCHITECT REVIEW REQUIRED`

The prior Candidate 1/2 harness was invalid: its `exchange()` function called
the care decision function directly and never sent packets through a socket.
That result is retained below as a failed attempt, not as IPC evidence.

The replacement `ipc_trust_qualification.py --run` uses four independent
process roles: a supervisor, an authorized producer, a care receiver, and an
untrusted same-UID sibling. The supervisor creates a private `AF_UNIX`
`SOCK_SEQPACKET` socketpair, passes only the required endpoint to each child,
creates a producer pidfd, and uses private pipes for capability material and
control. The producer and care children each set `PR_SET_DUMPABLE=0`; care
enables `SO_PASSCRED`, reads `SCM_CREDENTIALS`, and checks the live producer
PID/UID, generation, candidate kind, and (Candidate 2) an HMAC capability.
Care owns the append-only synthetic receipt journal and idempotency set; no
companion database or decision function is in the path.

Observed correction results:

- Weak mode-0600 pathname baseline: same-user valid injection `accepted:new`
  (accepted evidence of insufficiency).
- Candidate 1 actual packet: accepted; duplicate was `accepted:duplicate`;
  spoofed producer field was rejected.
- Candidate 2 actual packet: accepted; duplicate remained idempotent; spoofed
  producer, stale generation, malformed schema, forbidden mood input, and old
  capability were rejected; a missing companion database did not block care.
- Care restart replayed the candidate as a duplicate. Sending on the revoked
  old channel returned `Broken pipe`. A replacement producer with generation
  `g-2` was accepted; stale `g-1` and the `g-1` capability were rejected.
- The sibling could not connect to a pathname/abstract endpoint, discover a
  capability in environment/argv, or open the producer descriptor through
  `/proc`. The direct Linux `pidfd_getfd` syscall probe returned the exact
  host result `errno=1 (EPERM)`; this is recorded as an observed kernel result,
  not translated into a generic pass.
- Common sensor/model outage is represented as required `degraded-coverage`,
  never false normality. Threat exclusions remain root, kernel compromise,
  full account compromise, and a fully compromised authorized producer.

The bounded result supports carrying Candidate 2 into a later implementation
experiment (`E3_TARGET_TESTED` under the stated threat model), but it does not
adopt an IPC mechanism or establish security/safety capability. The old
Candidate 1/2 result is explicitly superseded because it lacked actual
cross-process socket traffic.

Historical status at first submission: `SUPERSEDED — IN-PROCESS HARNESS DID NOT TEST IPC`

## Historical first submission (superseded; retained for audit)

The following original sections describe the invalid in-process attempt. They
are preserved to show the review trail and are not current IPC evidence.

## Threat model

The tested property is limited to an unrelated same-user sibling process, accidental local clients, malformed companion/model/Godot-like inputs, stale producer generations, replay, and unintended descriptor inheritance. It excludes root, kernel compromise, full account compromise, privileged debugging, and a fully compromised authorized producer. A safety receipt is represented only by an in-memory synthetic outcome; no care-core, incident, contact, or notification exists.

State the bounded same-user sibling-process threat, explicit exclusions, protected assets, process assumptions, and why message-declared identity/UID equality is insufficient.

## Candidate designs

| Candidate | Design | Result |
|---|---|---|
| Weak baseline | Mode-0600 pathname AF_UNIX socket; same UID; message-declared producer | **Failed as intended:** a separate same-user process connected and submitted a structurally valid candidate, yielding `accepted:new`. |
| Candidate 1 | Supervisor-created, unnamed AF_UNIX `SOCK_SEQPACKET` pair; only intended endpoints; non-inheritable descriptors; generation check | Synthetic valid candidate accepted; spoofed producer and stale generation rejected; duplicate yielded `accepted:duplicate`; no companion database path was used. The sibling had no inherited endpoint and the attempted `/proc` FD open returned `blocked:6` on this host. |
| Candidate 2 | Candidate 1 plus per-generation HMAC capability passed only over the private channel and `PR_SET_DUMPABLE=0` on the care process before probing | Valid capability accepted; missing capability and stale generation rejected; `/proc` FD open returned `blocked:13`; process non-dumpability call returned success. |

Candidate 2 is the narrower passing qualification recommendation because it adds a per-generation capability and a tested diagnostic-hardening control. Both candidates require a real future supervisor handoff design to prove descriptor ownership, close-on-exec, capability injection, restart replacement, and audit semantics in the actual process graph.

Document the weak baseline and at least two host-viable candidates, including lifecycle, authentication material, descriptor/socket ownership, peer verification, generation/restart, revocation, confinement, and failure behavior.

## Attack matrix

- same-user weak-path injection: `PASSED` as an expected insufficiency demonstration;
- spoofed producer and companion mood-like input: `REJECTED` before synthetic receipt;
- malformed/schema/replay tests: covered by frozen shell negatives and generation/capability rejection; duplicate valid candidate: `accepted:duplicate` with no second logical transition;
- descriptor inheritability: `false` for both private endpoints;
- available `/proc` FD duplication probes: blocked before and after hardening (`errno 6`, then `errno 13`);
- producer generation mismatch: rejected; valid new generation accepted;
- companion stopped/database absent: synthetic direct candidate accepted without a companion database reference;
- producer outage: represented as required `degraded-coverage` rather than normal coverage;
- care restart, pid reuse/pidfd, full concurrent malformed corpus, and a production supervisor handoff: `NOT RUN` / later implementation-gate work.

Record same-user connection/injection, producer-field spoofing, malformed schema, replay/duplicate, unintended FD inheritance, available `/proc`/pidfd duplication, PID/generation mismatch, producer/care restart, companion outage/database absence, common producer outage, and forbidden companion/model/dream/Godot inputs.

## Result

**Recommendation to Architect: carry Candidate 2 forward as the direct-care IPC implementation experiment**, not as an adopted mechanism. It prevents the observed unauthorized same-user connection before any synthetic safety receipt under this bounded threat model. It does not prove resistance to full user-account compromise, root, kernel compromise, or compromise of the authorized producer.

Recommend the narrowest passing design or report a blocker. State exactly what was proven, not proven, and which Phase 01 implementation gate remains.

## Final hardening status

The supervisor, authorized producer, care receiver and same-user sibling are
independent processes exchanging actual `SOCK_SEQPACKET` packets. The
supervisor is trusted for lifecycle and capability provisioning: its producer
copy is closed after handoff, while its care copy is retained only for care
restart and never read. Readiness, `PR_SET_DUMPABLE=0`, descriptor closure,
`SO_PASSCRED`, pidfd liveness, generation binding, replay/idempotency,
restart/revocation and degraded-outage assertions are fail-closed. The exact
host `pidfd_getfd` result is `EPERM`; no universal protection is claimed.
Candidate 1/2 remain unqualified implementation hypotheses pending Architect
selection and a later authorized Phase 01 experiment.
