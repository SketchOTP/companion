# Direct-Care IPC Trust Qualification

Status: `PENDING CODEX EXECUTION`

## Threat model

State the bounded same-user sibling-process threat, explicit exclusions, protected assets, process assumptions, and why message-declared identity/UID equality is insufficient.

## Candidate designs

Document the weak baseline and at least two host-viable candidates, including lifecycle, authentication material, descriptor/socket ownership, peer verification, generation/restart, revocation, confinement, and failure behavior.

## Attack matrix

Record same-user connection/injection, producer-field spoofing, malformed schema, replay/duplicate, unintended FD inheritance, available `/proc`/pidfd duplication, PID/generation mismatch, producer/care restart, companion outage/database absence, common producer outage, and forbidden companion/model/dream/Godot inputs.

## Result

Recommend the narrowest passing design or report a blocker. State exactly what was proven, not proven, and which Phase 01 implementation gate remains.
