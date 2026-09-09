# Direct-Care IPC Trust Qualification

Status: `COMPLETED — E3 TARGET-TESTED SYNTHETIC LOCAL THREAT CHECK`

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
